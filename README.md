# FairHire: Automated Resume Anonymizer for Bias-Free Recruitment


## Overview

**FairHire** is a robust web application and command-line utility for anonymizing resumes, designed to support bias-free candidate screening in recruitment processes. The system automatically detects and redacts personally identifiable information (PII) from resumes—including names, addresses, emails, phone numbers, social media links, and more—across multiple document formats (TXT, DOCX, PDF, JPG, PNG).

Built with **Python** and leveraging state-of-the-art NLP (spaCy), regex PII detection, and OCR (pytesseract/pdfplumber), FairHire helps hiring teams minimize bias by ensuring all screening is based solely on skills and experience.

---

## Features

- 🚀 **Multi-format Support:** TXT, DOCX, PDF, JPG, PNG, including scanned/image-based resumes via OCR
- 🔍 **Automated PII Redaction:** Smart masking using named entity recognition (NER) and regex
- 📝 **Redaction Summary:** Transparent reporting on all redacted entities
- 🎨 **Intuitive Streamlit UI:** Upload, preview, anonymize, and download in-browser
- ⏱️ **Fast Processing:** Bulk file support with progress feedback
- 📊 **CLI Utility:** For batch processing via command line
- 🔒 **Your data never leaves your machine!**

---




