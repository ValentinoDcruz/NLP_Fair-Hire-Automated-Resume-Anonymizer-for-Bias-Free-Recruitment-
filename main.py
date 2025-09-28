from anonymizer.anonymize import anonymize_text
import pandas as pd

def main():
    import sys
    import os
    # Command line usage: python main.py data/sample_resume.txt
    resume_file = "data/sample_resume.txt"
    if len(sys.argv) > 1:
        resume_file = sys.argv[1]
    if not os.path.isfile(resume_file):
        print(f"File not found: {resume_file}")
        return

    with open(resume_file, "r", encoding="utf-8") as f:
        resume_text = f.read()

    anonymized_text, summary = anonymize_text(resume_text)
    out_file = resume_file.replace(".txt", "_anonymized.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(anonymized_text)
    print(f"\nAnonymized resume saved to {out_file}")

    # Save redaction summary as CSV
    if summary:
        df = pd.DataFrame(list(summary.items()), columns=["Entity Type", "Count"])
        summary_file = resume_file.replace(".txt", "_redaction_report.csv")
        df.to_csv(summary_file, index=False)
        print(f"Redaction summary saved to {summary_file}")
        print("\nRedaction Summary:")
        print(df.to_string(index=False))
    else:
        print("No entities were redacted.")

if __name__ == "__main__":
    main()
