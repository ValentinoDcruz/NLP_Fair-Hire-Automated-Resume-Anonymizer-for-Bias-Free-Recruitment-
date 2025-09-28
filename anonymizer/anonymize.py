import spacy
import re
from collections import defaultdict

# Load spaCy model (custom NER training can be plugged here)
nlp = spacy.load("en_core_web_sm")

# Smart placeholders for entities
ENTITY_MAP = {
    "PERSON": "[NAME]",
    "ORG": "[COMPANY]",
    "GPE": "[LOCATION]",
    "LOC": "[LOCATION]",
    "DATE": "[DATE]",
    "EMAIL": "[EMAIL]",
    "PHONE": "[PHONE]",
    "NORP": "[GROUP]",
}

# Whitelist for technical skills/certifications
SKILL_WHITELIST = [
    "Python", "SQL", "Tableau", "Power BI", "Machine Learning",
    "Data Visualization", "Coursera", "English", "Hindi",
]

# Define additional PII regex patterns
PATTERNS = [
    # Emails
    (re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"), "[EMAIL]"),
    # Phones (international + local)
    (re.compile(r"\+?\d{1,3}[-\s]?\d{10,}"), "[PHONE]"),
    (re.compile(r"\b\d{10,}\b"), "[PHONE]"),
    # Street names
    (re.compile(r"\b[A-Za-z]+\s(?:Street|Avenue|Road|Lane|Boulevard|Colony|Nagar|Marg)\b", re.IGNORECASE), "[ADDRESS]"),
    # Common social profiles
    (re.compile(r"\bLinkedIn\b|\bGitHub\b|\bInstagram\b|\bFacebook\b|\bTwitter\b"), "[SOCIAL]"),
    # Gendered titles
    (re.compile(r"\b(Mr\.|Mrs\.|Ms\.|Miss|Sir|Madam)\b", re.IGNORECASE), "[TITLE]"),
    # Add regex for LinkedIn/GitHub URLs
    (re.compile(r"(linkedin\.com[^\s]*)", re.IGNORECASE), "[LINKEDIN]"),
    (re.compile(r"(github\.com[^\s]*)", re.IGNORECASE), "[GITHUB]"),
]

def whitelist_entities(ents, whitelist):
    # Return only those entities NOT matching whitelist exactly
    return [ent for ent in ents if not any(ent.text.lower() == w.lower() for w in whitelist)]

def audit_log(log_list):
    print("=== Audit Log ===")
    for item in log_list:
        print(item)
    print("=== End Audit ===\n")

def anonymize_text(text):
    doc = nlp(text)
    anonymized = text
    offset = 0
    audit_items = []
    redaction_summary = defaultdict(int)

    # Regex-based masking for extra PII
    for pattern, holder in PATTERNS:
        for match in pattern.finditer(anonymized):
            start, end = match.span()
            anonymized = anonymized[:start] + holder + anonymized[end:]
            audit_items.append(f"Masked (Regex): {holder} -> {match.group()}")
            redaction_summary[holder] += 1

    # NER: Mask only entities NOT on whitelist
    ents_to_mask = whitelist_entities(doc.ents, SKILL_WHITELIST)
    ents_to_mask = sorted(ents_to_mask, key=lambda x: x.start_char)

    for ent in ents_to_mask:
        label = ENTITY_MAP.get(ent.label_, "[REDACTED]")
        start = ent.start_char + offset
        end = ent.end_char + offset
        anonymized = anonymized[:start] + label + anonymized[end:]
        audit_items.append(f"Masked (NER): {label} -> {ent.text}")
        redaction_summary[label] += 1
        offset += len(label) - (end - start)

    # Optional: print audit log for debugging
    # audit_log(audit_items)

    return anonymized, dict(redaction_summary)
