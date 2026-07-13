import os
import csv
import xml.etree.ElementTree as ET

# Change this path if needed
MEDQUAD_FOLDER = r"C:\Users\arnav\OneDrive\Desktop\MedQuAD-master\MedQuAD-master"

OUTPUT_FILE = "medical_dataset.csv"


def clean(text):
    if text:
        return " ".join(text.split())
    return ""


rows = []

for root_dir, dirs, files in os.walk(MEDQUAD_FOLDER):
    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root_dir, file)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                source = root.attrib.get("source", "")
                url = root.attrib.get("url", "")

                focus = clean(root.findtext("Focus"))

                for qa in root.findall(".//QAPair"):

                    question = qa.find("Question")
                    answer = qa.find("Answer")

                    if question is None or answer is None:
                        continue

                    question_text = clean(question.text)
                    answer_text = clean(answer.text)

                    rows.append([
                        question_text,
                        answer_text,
                        focus,
                        source,
                        url
                    ])

            except Exception as e:
                print(f"Skipped {file}: {e}")

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Question",
        "Answer",
        "Disease",
        "Source",
        "URL"
    ])

    writer.writerows(rows)

print("=" * 60)
print(f"Finished!")
print(f"Total Q&A pairs : {len(rows)}")
print(f"Saved to        : {OUTPUT_FILE}")
print("=" * 60)