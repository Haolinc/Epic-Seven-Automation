import traceback
from datetime import datetime


def output_error_to_file(exception: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error.txt", "a") as f:  # 'a' for append mode
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"{exception}\n")
        f.write("Traceback:\n")
        traceback.print_exc(file=f)
        f.write("-" * 40 + "\n")
