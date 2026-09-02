import csv
from datetime import datetime
import glob
import math
from antropy import sample_entropy
from scipy.signal import find_peaks
import statistics

def compute_features(window):
    if not window:
        return []
    
    first_row = window[0]
    first_timestamp = first_row[0]
    first_datetime = first_row[1]
    
    ecg_values = []
    hr_values = []
    rr_values = []
    for row in window:
        try:
            ecg = float(row[2])  # ECG is column 2
            ecg_values.append(ecg)
            if len(row) > 3:
                hr = float(row[3])  # HR is column 3
                hr_values.append(hr)
            if len(row) > 4:
                rr = float(row[4])  # RR is column 4
                rr_values.append(rr)
        except (ValueError, IndexError):
            continue  # Skip invalid values
    
    if not ecg_values:
        return [first_timestamp, first_datetime, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    N = len(ecg_values)
    mean = sum(ecg_values) / N
    variance = sum((x - mean) ** 2 for x in ecg_values) / (N - 1) if N > 1 else 0
    std = math.sqrt(variance)
    range_ = max(ecg_values) - min(ecg_values)
    energy = sum(x ** 2 for x in ecg_values) / N
    
    # Sample Entropy
    try:
        samp_ent = sample_entropy(ecg_values)
    except Exception as e:
        samp_ent = 0  # Default value if calculation fails
    
    # Missing peaks / artifacts
    hr_mean = sum(hr_values) / len(hr_values) if hr_values else 0
    expected_beats = (hr_mean / 60) * 30  # Expected beats in 30 seconds
    try:
        # Use a threshold for peak detection: mean + 0.5 * std to detect significant R-peaks
        threshold = mean + 0.5 * std if std > 0 else 0
        peaks, _ = find_peaks(ecg_values, height=threshold, distance=int(130 / (hr_mean / 60)) if hr_mean > 0 else 50)  # Min distance based on HR
        detected_peaks = len(peaks)
        missing_peaks = max(0, int(expected_beats) - detected_peaks)
    except Exception as e:
        missing_peaks = 0
    
    # HRV features
    if rr_values:
        rr_mean = sum(rr_values) / len(rr_values)
        sdnn = math.sqrt(sum((r - rr_mean)**2 for r in rr_values) / len(rr_values))
        differences = [rr_values[i+1] - rr_values[i] for i in range(len(rr_values)-1)]
        if differences:
            rmssd = math.sqrt(sum(d**2 for d in differences) / len(differences))
            n_diff50 = sum(1 for d in differences if abs(d) > 50)
            pnn50 = 100 * n_diff50 / len(differences)
        else:
            rmssd = 0
            pnn50 = 0
        hr_mean_calc = 60000 / rr_mean  # Assuming RR in ms
        hr_max = max(60000 / r for r in rr_values)
        hr_min = min(60000 / r for r in rr_values)
    else:
        sdnn = 0
        rmssd = 0
        pnn50 = 0
        hr_mean_calc = 0
        hr_max = 0
        hr_min = 0
    
    return [first_timestamp, first_datetime, mean, std, range_, energy, samp_ent, missing_peaks, sdnn, rmssd, pnn50, hr_mean_calc, hr_max, hr_min]

def process_row(row):
    # Get the UNIX timestamp in nanoseconds
    timestamp_ns = int(row[0])
    # Convert to seconds
    timestamp_s = timestamp_ns / 1e9
    # Convert to datetime
    dt = datetime.fromtimestamp(timestamp_s)
    # Insert the datetime after the timestamp
    row.insert(1, dt.isoformat())
    # Keep only the first 5 columns: UNIX Timestamp, DateTime, ECG, HR, RR
    return row[:5]

# Find all files in W01 matching the pattern
files = glob.glob('../11-08-2025, 07_50_22-*.csv')
# Sort by the number after the dash
files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))

print("Starting processing files")
combined_file = 'combined_features.csv'
all_rows = []

# Process each file
for input_file in files:
    print(f"Processing {input_file}")
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip header for data rows
        for row in reader:
            processed_row = process_row(row)
            all_rows.append(processed_row)

# Sort all rows by timestamp (first column)
all_rows.sort(key=lambda x: int(x[0]))

print(f"Total rows: {len(all_rows)}")

# Now, create 30-second windows and compute features
window_duration_ns = 30 * 1e9  # 30 seconds in nanoseconds
features_rows = []

current_window = []
start_timestamp = None

for i, row in enumerate(all_rows):
    timestamp_ns = int(row[0])
    if start_timestamp is None:
        start_timestamp = timestamp_ns
        current_window = [row]
    elif timestamp_ns - start_timestamp < window_duration_ns:
        current_window.append(row)
    else:
        # Process the current window
        if current_window:
            features_rows.append(compute_features(current_window))
        # Start new window
        start_timestamp = timestamp_ns
        current_window = [row]
    
    if i % 100000 == 0:
        print(f"Processed {i} rows")

# Process the last window
if current_window:
    features_rows.append(compute_features(current_window))

print(f"Features rows: {len(features_rows)}")

# Calculate global statistics for z-score normalization
features_indices = {
    'ECG_energy': 5,
    'ECG_samp_ent': 6,
    'ECG_missing_peaks': 7,
    'SDNN': 8,
    'RMSSD': 9,
    'pNN50': 10,
    'HR_mean': 11
}

global_stats = {}
for name, idx in features_indices.items():
    values = [row[idx] for row in features_rows if row[idx] != 0 or name in ['ECG_energy', 'ECG_samp_ent', 'ECG_missing_peaks']]  # Include all for global stats
    if values:
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0
    else:
        mean = 0
        std = 1  # Avoid division by zero
    global_stats[name] = {'mean': mean, 'std': std}

# Add FatigueIndex to each row
for row in features_rows:
    z_scores = {}
    for name, idx in features_indices.items():
        val = row[idx]
        mean = global_stats[name]['mean']
        std = global_stats[name]['std']
        z_scores[name] = (val - mean) / std if std != 0 else 0
    
    fatigue_index = (
        1.2 * z_scores['HR_mean'] -
        1.0 * z_scores['RMSSD'] -
        0.8 * z_scores['SDNN'] -
        0.8 * z_scores['pNN50'] +
        0.6 * z_scores['ECG_energy'] +
        0.4 * z_scores['ECG_samp_ent'] +
        0.5 * z_scores['ECG_missing_peaks']
    )
    row.append(fatigue_index)

# Write to combined features file
with open(combined_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write header
    header = ['UNIX Timestamp', 'DateTime', 'ECG_mean', 'ECG_std', 'ECG_range', 'ECG_energy', 'ECG_samp_ent', 'ECG_missing_peaks', 'SDNN', 'RMSSD', 'pNN50', 'HR_mean', 'HR_max', 'HR_min', 'FatigueIndex']
    writer.writerow(header)
    
    # Write features rows
    for row in features_rows:
        writer.writerow(row)

print(f"Combined features file created: {combined_file} with {len(features_rows)} rows")

# Split the combined features file into smaller chunks
chunk_size = 100000  # Smaller chunks since fewer rows
chunk_num = 1

try:
    with open(combined_file, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        current_chunk = []
        for row in reader:
            current_chunk.append(row)
            if len(current_chunk) >= chunk_size:
                # Write chunk
                chunk_file = f'features_part_{chunk_num}.csv'
                with open(chunk_file, 'w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    writer.writerows(current_chunk)
                print(f"Created {chunk_file} with {len(current_chunk)} rows")
                current_chunk = []
                chunk_num += 1
        
        # Write remaining rows
        if current_chunk:
            chunk_file = f'features_part_{chunk_num}.csv'
            with open(chunk_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(current_chunk)
            print(f"Created {chunk_file} with {len(current_chunk)} rows")

    print("Splitting complete.")
except PermissionError:
    print("Permission denied for combined_features.csv. Please close any programs using it and try again.")