import csv
from datetime import datetime
from pathlib import Path


INPUT_PATH = Path(
    r"C:\Users\Carlo\Desktop\owncloud 2025-08-11 ECG\new\W02\11-08-2025, 13_59_38-1.csv"
)
OUTPUT_PATH = INPUT_PATH.with_name(f"{INPUT_PATH.stem}_with_datetime.csv")


def convert_timestamp(timestamp_text):
    """Convert a UNIX timestamp in nanoseconds to a time-only string."""
    timestamp_ns = int(timestamp_text)
    return datetime.fromtimestamp(timestamp_ns / 1_000_000_000).strftime("%H:%M:%S")


with INPUT_PATH.open("r", newline="", encoding="utf-8-sig") as input_file:
    reader = csv.reader(input_file)
    header = next(reader)

    try:
        timestamp_index = header.index("UNIX Timestamp")
    except ValueError as error:
        raise ValueError("No se encontro la columna 'UNIX Timestamp'.") from error

    output_header = header[:]
    output_header.insert(timestamp_index + 1, "DateTime")

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_header)

        for row_number, row in enumerate(reader, start=2):
            if not row:
                continue

            try:
                date_time = convert_timestamp(row[timestamp_index])
            except (IndexError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Timestamp invalido en la fila {row_number}: {row}"
                ) from error

            output_row = row[:]
            output_row.insert(timestamp_index + 1, date_time)
            writer.writerow(output_row)

print(f"Archivo original: {INPUT_PATH}")
print(f"Archivo generado: {OUTPUT_PATH}")