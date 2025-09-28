from anonymizer.anonymize import anonymize_text

def test_basic():
    example = "Mr. John Doe works at Facebook. Contact: john.doe@email.com or +91-9876543210. Excellent in Python and Tableau."
    result = anonymize_text(example)
    print("Test Result:\n", result)
    assert "[NAME]" in result
    assert "[COMPANY]" in result
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "Python" in result          # Should NOT be masked
    assert "Tableau" in result         # Should NOT be masked
    print("Test passed!")

if __name__ == "__main__":
    test_basic()
