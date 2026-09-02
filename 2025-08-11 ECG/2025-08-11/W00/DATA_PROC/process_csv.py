import csv
from datetime import datetime

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header
        header = next(reader)
        # Insert the new column header after UNIX Timestamp
        header.insert(1, 'DateTime')
        writer.writerow(header)
        
        # Process each row
        for row in reader:
            # Get the UNIX timestamp in nanoseconds
            timestamp_ns = int(row[0])
            # Convert to seconds
            timestamp_s = timestamp_ns / 1e9
            # Convert to datetime
            dt = datetime.fromtimestamp(timestamp_s)
            # Insert the datetime after the timestamp
            row.insert(1, dt.isoformat())
            writer.writerow(row)

# Process first file
input_file1 = 'W00/11-08-2025, 07_24_02-1.csv'
output_file1 = 'processed1.csv'
process_file(input_file1, output_file1)
print(f"Processing complete for {input_file1}. Output saved to {output_file1}")

# Process second file
input_file2 = 'W00/11-08-2025, 07_24_02-2.csv'
output_file2 = 'processed2.csv'
process_file(input_file2, output_file2)
print(f"Processing complete for {input_file2}. Output saved to {output_file2}")

# Combine both processed files
combined_file = 'combined.csv'
with open(combined_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write header from first file
    with open(output_file1, 'r') as infile1:
        reader1 = csv.reader(infile1)
        header = next(reader1)
        writer.writerow(header)
        
        # Write rows from first file
        for row in reader1:
            writer.writerow(row)
    
    # Write rows from second file (skip header)
    with open(output_file2, 'r') as infile2:
        reader2 = csv.reader(infile2)
        next(reader2)  # Skip header
        for row in reader2:
            writer.writerow(row)

print(f"Combined file created: {combined_file}")