import csv
import pathlib

README_PATH = pathlib.Path("README.md")
CSV_PATH = pathlib.Path("results.csv")
START_MARKER = "<!-- leaderboard:start -->"
END_MARKER = "<!-- leaderboard:end -->"

def read_csv_data(csv_path):
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows

def format_markdown_table(rows):
    table = [
        START_MARKER,
        "## Leaderboard",
        "| Name       | Weight | Volume | Value |",
        "|------------|--------|--------|-------|"
    ]
    for row in rows:
        name = row["name"]
        weight = float(row["weight"])
        volume = float(row["volume"])
        value = float(row["value"])
        table.append(f"| {name} | {weight:.2f} | {volume:.2f} | {value:.2f} |")
    table.append(END_MARKER)
    return "\n".join(table)

def update_readme(readme_path, new_table):
    with open(readme_path, "r") as f:
        content = f.read()

    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Markers not found in README.md")

    updated = (
        content[:start_idx].rstrip() + "\n" +
        new_table + "\n" +
        content[end_idx + len(END_MARKER):].lstrip()
    )

    with open(readme_path, "w") as f:
        f.write(updated)

def main():
    if not CSV_PATH.exists():
        print(f"❌ Archivo no encontrado: {CSV_PATH}")
        return
    if not README_PATH.exists():
        print(f"❌ Archivo no encontrado: {README_PATH}")
        return

    rows = read_csv_data(CSV_PATH)
    new_table = format_markdown_table(rows)
    update_readme(README_PATH, new_table)
    print("✅ Leaderboard actualizado en README.md")

if __name__ == "__main__":
    main()
