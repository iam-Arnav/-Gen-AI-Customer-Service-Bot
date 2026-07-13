import json
import csv

INPUT_FILE = r"C:\Users\arnav\OneDrive\Desktop\archive\arxiv-metadata-oai-snapshot.json"
OUTPUT_FILE = "knowledge/cs_arxiv.csv"

LIMIT = 20000

count = 0

with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    writer = csv.writer(outfile)
    writer.writerow(["title", "content"])

    for line in infile:
        paper = json.loads(line)

        categories = paper.get("categories", "")

        if "cs." not in categories:
            continue

        title = paper.get("title", "").replace("\n", " ").strip()
        abstract = paper.get("abstract", "").replace("\n", " ").strip()

        content = f"{title}\n\n{abstract}"

        writer.writerow([title, content])

        count += 1

        if count % 1000 == 0:
            print(f"{count} papers processed")

        if count >= LIMIT:
            break

print(f"\nDone! Saved {count} Computer Science papers.")
print(f"Output: {OUTPUT_FILE}")