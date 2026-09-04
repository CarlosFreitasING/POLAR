#& ".\.venv\Scripts\python.exe" ".\new\process_wcarlos_exercise_pc_tempvar.py"
"""Process the Wcarlos EXERCISE and PC datasets using the worker pipeline."""

import csv
import math
from pathlib import Path

from process_all_workers_tempvar import (
    BASE_FEATURES,
    BASELINE_HEADER,
    BASELINE_WINDOW_COUNT,
    FEATURE_HEADER,
    NORMALIZATION_FEATURES,
    OUTPUT_HEADER,
    add_temporal_features,
    calculate_fatigue_index,
    make_windows,
    normalize_features,
    process_row,
    write_baseline,
    write_features,
)

ROOT_DIR = Path(__file__).resolve().parent / "Wcarlos"
DATASET_NAMES = ("EXERCISE", "PC")


def read_dataset_rows(dataset_dir):
    """Read all raw CSV files from one Wcarlos dataset directory."""
    rows = []
    csv_files = sorted(
        csv_file
        for csv_file in dataset_dir.glob("*.csv")
        if not csv_file.stem.endswith("_with_datetime")
    )
    for csv_file in csv_files:
        print(f"  Leyendo {csv_file.name}")
        with csv_file.open("r", newline="", encoding="utf-8-sig") as input_file:
            reader = csv.reader(input_file)
            next(reader, None)
            for raw_row in reader:
                processed_row = process_row(raw_row)
                if processed_row is not None:
                    processed_row["activity"] = dataset_dir.name
                    rows.append(processed_row)
    rows.sort(key=lambda row: row["timestamp"])
    return rows


def process_dataset(dataset_name):
    """Process one dataset and keep its output separate from the other dataset."""
    dataset_dir = ROOT_DIR / dataset_name
    if not dataset_dir.is_dir():
        print(f"{dataset_name}: carpeta no encontrada, se omite")
        return

    rows = read_dataset_rows(dataset_dir)
    if not rows:
        print(f"{dataset_name}: no se encontraron registros válidos, se omite")
        return

    feature_rows = add_temporal_features(make_windows(rows))
    normalized_rows, baseline = normalize_features(feature_rows)
    output_rows = []
    for row in normalized_rows:
        output_row = [dataset_name] + row
        output_row.append(calculate_fatigue_index(row))
        output_rows.append(output_row)

    output_dir = dataset_dir / "PROCESSED"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "combined_features_1min.csv"
    write_features(output_path, output_rows)
    baseline_path = output_dir / "baseline_statistics.csv"
    write_baseline(baseline_path, dataset_name, baseline)

    complete_baseline_count = len([
        row
        for row in feature_rows
        if row[3] == 1
        and all(
            row[FEATURE_HEADER.index(feature)] != ""
            for feature in NORMALIZATION_FEATURES
        )
    ][:BASELINE_WINDOW_COUNT])
    print(f"{dataset_name}: {len(rows)} registros -> {len(feature_rows)} ventanas")
    print(f"  Baseline: {complete_baseline_count} ventanas completas")
    print(f"  Guardado en {output_path}")


if __name__ == "__main__":
    print(f"Procesamiento de Wcarlos en: {ROOT_DIR}")
    print("Conjuntos: EXERCISE y PC")
    print("Ventanas temporales: 60 segundos")
    for dataset in DATASET_NAMES:
        process_dataset(dataset)
    print("Procesamiento terminado.")
