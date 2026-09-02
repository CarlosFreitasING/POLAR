import csv
from datetime import datetime
import glob
import math

def compute_features(window):
    if not window:
        return []
    
    first_row = window[0]
    first_timestamp = first_row[0]
    first_datetime = first_row[1]
    
    ecg_values = []
    for row in window:
        try:
            ecg = float(row[2])  # ECG is column 2
            ecg_values.append(ecg)
        except (ValueError, IndexError):
            continue  # Skip invalid values
    
    if not ecg_values:
        return [first_timestamp, first_datetime, 0, 0, 0, 0]
    
    N = len(ecg_values)
    mean = sum(ecg_values) / N
    variance = sum((x - mean) ** 2 for x in ecg_values) / (N - 1) if N > 1 else 0
    std = math.sqrt(variance)
    range_ = max(ecg_values) - min(ecg_values)
    energy = sum(x ** 2 for x in ecg_values) / N
    
    return [first_timestamp, first_datetime, mean, std, range_, energy]

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