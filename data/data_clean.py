import csv


def remove_duplicates(input_file, output_file):
    """
    去除 csv 中重复的行，只保留第一次出现的行
    """
    with open(input_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        seen = set()
        for row in rows:
            if tuple(row) not in seen:
                seen.add(tuple(row))
                writer.writerow(row)
            else:
                print(f"重复行：{row}")


if __name__ == "__main__":
    remove_duplicates("", "")
