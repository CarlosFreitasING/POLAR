import csv
import math
from datetime import datetime
from pathlib import Path

from antropy import sample_entropy
from scipy.signal import find_peaks


ROOT_DIR = Path(__file__).resolve().parent
WINDOW_SECONDS = 60
SAMPLE_RATE_HZ = 130
WORKER_DIRECTORIES = sorted(ROOT_DIR.glob("Worker * - *"))

FEATURE_HEADER = [
    "UNIX Timestamp",
    "DateTime",
    "Actividad",
    "HR_valid",
    "ECG_mean",
    "ECG_std",
    "ECG_range",
    "ECG_energy",
    "ECG_samp_ent",
    "ECG_missing_peaks",
    "SDNN",
    "RMSSD",
    "pNN50",
    "HR_mean",
    "HR_max",
    "HR_min",
]


def classify_activity(date_time):
    """Return a placeholder until the new day's schedule is provided."""
    return "No especificada"


def parse_float(value):
    """Return a numeric value or None for blank/invalid measurements."""
    try:
        if value is None or value.strip() == "":
            return None
        return float(value)
    except (AttributeError, ValueError):
        return None


def process_row(row):
    """Keep timestamp and measurements, adding a time-only DateTime value."""
    if not row or len(row) < 2:
        return None

    try:
        timestamp_ns = int(row[0])
    except (TypeError, ValueError):
        return None

    timestamp_datetime = datetime.fromtimestamp(timestamp_ns / 1e9)
    date_time = timestamp_datetime.strftime("%H:%M:%S")
    return {
        "timestamp": timestamp_ns,
        "datetime": date_time,
        "activity": classify_activity(timestamp_datetime),
        "ecg": parse_float(row[1]),
        "hr": parse_float(row[2]) if len(row) > 2 else None,
        "rr": parse_float(row[3]) if len(row) > 3 else None,
    }


def compute_features(window):
    """Calculate the same ECG, peak, HRV and HR variables for one window."""
    first_row = window[0]
    ecg_values = [row["ecg"] for row in window if row["ecg"] is not None]
    hr_values = [row["hr"] for row in window if row["hr"] is not None]
    rr_values = [row["rr"] for row in window if row["rr"] is not None and row["rr"] > 0]

    if not ecg_values:
        return [
            first_row["timestamp"],
            first_row["datetime"],
            first_row["activity"],
            0,
        ] + [""] * 12

    sample_count = len(ecg_values)
    ecg_mean = sum(ecg_values) / sample_count
    variance = (
        sum((value - ecg_mean) ** 2 for value in ecg_values) / (sample_count - 1)
        if sample_count > 1
        else 0
    )
    ecg_std = math.sqrt(variance)
    ecg_range = max(ecg_values) - min(ecg_values)
    ecg_energy = sum(value ** 2 for value in ecg_values) / sample_count

    try:
        ecg_samp_ent = sample_entropy(ecg_values)
        if not math.isfinite(ecg_samp_ent):
            ecg_samp_ent = 0
    except Exception:
        ecg_samp_ent = 0

    hr_mean_input = sum(hr_values) / len(hr_values) if hr_values else 0
    if hr_values:
        expected_beats = (hr_mean_input / 60) * WINDOW_SECONDS
        try:
            threshold = ecg_mean + 0.5 * ecg_std if ecg_std > 0 else 0
            minimum_distance = int(SAMPLE_RATE_HZ / (hr_mean_input / 60))
            peaks, _ = find_peaks(
                ecg_values,
                height=threshold,
                distance=max(1, minimum_distance),
            )
            missing_peaks = max(0, int(expected_beats) - len(peaks))
        except Exception:
            missing_peaks = ""
    else:
        missing_peaks = ""

    if rr_values:
        rr_mean = sum(rr_values) / len(rr_values)
        sdnn = math.sqrt(
            sum((value - rr_mean) ** 2 for value in rr_values) / len(rr_values)
        )
        differences = [
            rr_values[index + 1] - rr_values[index]
            for index in range(len(rr_values) - 1)
        ]
        if differences:
            rmssd = math.sqrt(sum(value ** 2 for value in differences) / len(differences))
            pnn50 = 100 * sum(abs(value) > 50 for value in differences) / len(differences)
        else:
            rmssd = 0
            pnn50 = 0
        hr_mean = 60000 / rr_mean
        hr_max = max(60000 / value for value in rr_values)
        hr_min = min(60000 / value for value in rr_values)
        hr_valid = int(all(
            math.isfinite(value)
            for value in [sdnn, rmssd, pnn50, hr_mean, hr_max, hr_min]
        ))
    else:
        sdnn = ""
        rmssd = ""
        pnn50 = ""
        hr_mean = ""
        hr_max = ""
        hr_min = ""
        hr_valid = 0

    return [
        first_row["timestamp"],
        first_row["datetime"],
        first_row["activity"],
        hr_valid,
        ecg_mean,
        ecg_std,
        ecg_range,
        ecg_energy,
        ecg_samp_ent,
        missing_peaks,
        sdnn,
        rmssd,
        pnn50,
        hr_mean,
        hr_max,
        hr_min,
    ]


def read_worker_rows(worker_dir):
    rows = []
    csv_files = sorted(
        csv_file
        for csv_file in worker_dir.rglob("*.csv")
        if not csv_file.stem.endswith("_with_datetime")
        and "PROCESSED" not in csv_file.parts
    )
    for csv_file in csv_files:
        print(f"  Leyendo {csv_file.name}")
        with csv_file.open("r", newline="", encoding="utf-8-sig") as input_file:
            reader = csv.reader(input_file)
            next(reader, None)
            for row in reader:
                processed_row = process_row(row)
                if processed_row is not None:
                    rows.append(processed_row)
    rows.sort(key=lambda row: row["timestamp"])
    return rows


def make_windows(rows):
    windows = []
    current_window = []
    start_timestamp = None
    window_duration_ns = WINDOW_SECONDS * 1_000_000_000

    for row in rows:
        if start_timestamp is None:
            start_timestamp = row["timestamp"]
            current_window = [row]
        elif row["timestamp"] - start_timestamp < window_duration_ns:
            current_window.append(row)
        else:
            windows.append(compute_features(current_window))
            start_timestamp = row["timestamp"]
            current_window = [row]

    if current_window:
        windows.append(compute_features(current_window))
    return windows


def write_features(output_path, feature_rows):
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(FEATURE_HEADER)
        writer.writerows(feature_rows)


def process_worker(worker_dir):
    worker_name = worker_dir.name
    rows = read_worker_rows(worker_dir)
    feature_rows = make_windows(rows)
    output_dir = worker_dir / "PROCESSED"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "combined_features_1min.csv"
    write_features(output_path, feature_rows)
    print(f"{worker_name}: {len(rows)} registros -> {len(feature_rows)} ventanas")
    print(f"  Guardado en {output_path}")


if __name__ == "__main__":
    print(f"Procesamiento de trabajadores en: {ROOT_DIR}")
    print(f"Ventanas temporales: {WINDOW_SECONDS} segundos")
    for worker_dir in WORKER_DIRECTORIES:
        process_worker(worker_dir)
    print("Procesamiento terminado.")