# PII Anonymizer

> A command-line tool to detect and anonymize Personally Identifiable Information (PII) in text files, built on top of [Microsoft Presidio](https://microsoft.github.io/presidio/).

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)](#prerequisites)
[![Tests](https://img.shields.io/badge/tests-6%20passed-brightgreen.svg)](#testing)

---

## 📖 Overview

**PII Anonymizer** is a lightweight CLI tool that scans text for Personally Identifiable Information (PII) and replaces it with safe placeholders. It is designed for developers, data scientists, and anyone who needs to sanitize datasets before sharing, publishing, or feeding them into machine learning models or third-party services.

The tool leverages the powerful NLP and pattern-recognition capabilities of **Microsoft Presidio** to identify entities such as names, emails, phone numbers, credit card numbers, IP addresses, and more. Each entity is then anonymized using a configurable operator (`replace`, `mask`, `redact`, or `hash`).

### Why this tool?

- **Privacy-first**: Runs entirely on your machine. No data is ever sent to external servers.
- **Compliance-oriented**: Built with GDPR in mind, with a clear distinction between anonymization and pseudonymization.
- **Simple**: A single command to sanitize a file. No configuration required to get started.
- **Extensible**: Add custom recognizers for domain-specific entities with just a few lines of code.

---

## ✨ Features

- **Wide entity coverage**: Names, emails, phone numbers, credit cards, SSNs, IP addresses, dates, locations, URLs, and more.
- **Configurable operators**: Choose how each entity type is anonymized (`replace`, `mask`, `redact`, `hash`).
- **Simple CLI**: One command to anonymize a file, with optional output redirection.
- **Stdout-friendly**: Prints to stdout by default, so you can pipe results into other tools.
- **Tested**: Comes with a pytest suite covering the core anonymization logic.
- **Cross-platform**: Works on Windows, macOS, and Linux.
- **Extensible**: Add custom recognizers for domain-specific entities (e.g., national IDs, tax codes).

---

## 📋 Prerequisites

Before installing PII Anonymizer, make sure your system meets the following requirements.

### Required software

| Requirement | Minimum version | Notes |
| :--- | :--- | :--- |
| **Python** | 3.9 | 3.11 or 3.12 recommended for best compatibility. |
| **pip** | 21.0 | Usually bundled with Python. |
| **Git** | 2.30 | Only needed if you install from source. |

### System requirements

| Resource | Minimum | Recommended |
| :--- | :--- | :--- |
| **Disk space** | ~1.5 GB | ~2.5 GB (includes spaCy models and dependencies) |
| **RAM** | 2 GB | 4 GB or more |
| **OS** | Windows 10, macOS 11, Ubuntu 20.04 | Latest versions |

> **Note**: The largest disk usage comes from the spaCy NLP model (`en_core_web_lg` is ~600 MB). If you're short on space, you can use the smaller `en_core_web_sm` model (~12 MB), at the cost of slightly lower accuracy on some entities.

### Verify your Python installation

Open a terminal and run:

```bash
python --version
```

You should see something like `Python 3.11.5`. If Python is not installed or the version is older than 3.9, download it from [python.org](https://www.python.org/downloads/).

> **Windows users**: During Python installation, make sure to check **"Add Python to PATH"**. If you forget this step, `python` won't be recognized in the terminal.

### Verify your pip installation

```bash
pip --version
```

If pip is not installed, follow the [official pip installation guide](https://pip.pypa.io/en/stable/installation/).

### Verify your Git installation (only if installing from source)

```bash
git --version
```

If Git is not installed, download it from [git-scm.com](https://git-scm.com/downloads).

---

## 🚀 Installation

### Option 1: From source (recommended for now)

#### Step 1 — Clone the repository

```bash
git clone https://github.com/Sahkaara/pii-anonymizer.git
cd pii-anonymizer
```

#### Step 2 — Create a virtual environment

A virtual environment keeps the project's dependencies isolated from your global Python installation. This is a best practice and strongly recommended.

**Windows (cmd):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **PowerShell note**: If you get an execution policy error, run this once in the current session:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your prompt should show `(venv)` at the beginning of the line.

#### Step 3 — Install the package

```bash
pip install -e .
```

The `-e` flag installs the package in "editable" mode, meaning changes to the source code take effect immediately without reinstalling.

#### Step 4 — Download a spaCy language model

Presidio uses spaCy under the hood for NLP-based entity recognition. You need at least one language model installed.

```bash
python -m spacy download en_core_web_lg
```

> **Alternative**: If you're short on disk space or want a faster download, use `en_core_web_sm` instead. It's much smaller but less accurate for entities like `PERSON` and `LOCATION`.

### Option 2: From PyPI (when available)

Once published to PyPI, you'll be able to install it with:

```bash
pip install pii-anonymizer
```

> **Status**: Not yet published. Use Option 1 for now.

---

## 🛠️ Usage

### Basic usage

Anonymize a file and print the result to the terminal:

```bash
pii-anonymizer input.txt
```

### Save the result to a file

```bash
pii-anonymizer input.txt --output output.txt
```

Or, using the short form:

```bash
pii-anonymizer input.txt -o output.txt
```

### Specify the language

```bash
pii-anonymizer input.txt --lang en
```

> **Note**: Currently, only English (`en`) is fully supported out of the box. Additional languages can be added by registering more spaCy models (see [Configuration](#️-configuration)).

### Pipe the result

Because the tool writes the anonymized text to `stdout` (and logs to `stderr`), you can pipe it directly:

**macOS / Linux:**
```bash
cat input.txt | pii-anonymizer - > output.txt
```

**Windows (PowerShell):**
```powershell
Get-Content input.txt | pii-anonymizer - > output.txt
```

### Get help

```bash
pii-anonymizer --help
```

---

## 📚 Example

Given a file `input.txt` with the following content:

```
Hi, my name is John Smith and my email is john.smith@example.com.
You can reach me at 212-555-1234. My card number is 4095-2609-9393-4932.
```

Running:

```bash
pii-anonymizer input.txt
```

Produces:

```
Hi, my name is [NAME] and my email is [EMAIL].
You can reach me at [PHONE]. My card number is ************4932.
```

---

## 🧩 Supported Entities

The tool detects and anonymizes the following PII entity types out of the box:

| Entity | Example | Default Operator |
| :--- | :--- | :--- |
| `PERSON` | John Smith | `replace` → `[NAME]` |
| `EMAIL_ADDRESS` | john@example.com | `replace` → `[EMAIL]` |
| `PHONE_NUMBER` | 212-555-1234 | `replace` → `[PHONE]` |
| `CREDIT_CARD` | 4095-2609-9393-4932 | `mask` → `************4932` |
| `US_SSN` | 123-45-6789 | `redact` (removed) |
| `IP_ADDRESS` | 192.168.1.1 | `replace` → `[IP_ADDRESS]` |
| `DATE_TIME` | January 1, 2026 | `replace` → `[DATE_TIME]` |
| `LOCATION` | New York | `replace` → `[LOCATION]` |
| `URL` | https://example.com | `replace` → `[URL]` |
| `US_BANK_NUMBER` | 123456789 | `mask` |
| `US_DRIVER_LICENSE` | D1234567 | `replace` |
| `US_PASSPORT` | 123456789 | `replace` |
| `US_ITIN` | 912-90-1234 | `replace` |
| `US_NATIONAL_ID` | — | `replace` |
| `US_VISA` | — | `replace` |

To customize how an entity is anonymized, see [Configuration](#️-configuration).

---

## ⚙️ Configuration

### Changing the anonymization operators

The default operators are defined in `src/pii_anonymizer/core.py` in the `OPERATORS` dictionary. Each key is a PII entity type, and the value is an `OperatorConfig` that specifies how to anonymize it.

Available operators:

| Operator | Description | Example parameters |
| :--- | :--- | :--- |
| `replace` | Replaces the entity with a fixed placeholder. | `{"new_value": "[NAME]"}` |
| `mask` | Masks characters with a masking character. | `{"masking_char": "*", "chars_to_mask": 12, "from_end": False}` |
| `redact` | Removes the entity entirely. | — |
| `hash` | Replaces the entity with a hash (pseudonymization). | `{"hash_type": "sha256"}` |
| `encrypt` | Encrypts the entity with a key (pseudonymization). | `{"key": "..."}` |

Example — to replace credit cards entirely instead of masking them:

```python
"CREDIT_CARD": OperatorConfig("replace", {"new_value": "[CARD]"}),
```

### Adding custom recognizers

You can add custom recognizers for domain-specific entities (e.g., Italian codice fiscale, IBAN, national IDs). Example:

```python
from presidio_analyzer import Pattern, PatternRecognizer

codice_fiscale_recognizer = PatternRecognizer(
    supported_entity="IT_CODICE_FISCALE",
    patterns=[
        Pattern(
            name="codice_fiscale",
            regex=r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b",
            score=0.9,
        )
    ],
)
analyzer.registry.add_recognizer(codice_fiscale_recognizer)
```

Then add a corresponding operator in `OPERATORS`:

```python
"IT_CODICE_FISCALE": OperatorConfig("replace", {"new_value": "[CODICE_FISCALE]"}),
```

### Adding more languages

To support another language, install the corresponding spaCy model and register it with a custom `NlpEngineProvider`:

```python
from presidio_analyzer.nlp_engine import NlpEngineProvider

configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "en", "model_name": "en_core_web_lg"},
        {"lang_code": "it", "model_name": "it_core_news_lg"},
    ],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
```

Then pass `supported_languages=["en", "it"]` to `AnalyzerEngine`.

---

## ⚖️ Anonymization vs. Pseudonymization

It is important to understand the difference between **anonymization** and **pseudonymization**, especially under the GDPR:

- **Anonymization**: The data is irreversibly transformed so that the individual can no longer be identified. Truly anonymized data is **not** subject to the GDPR.
- **Pseudonymization**: The data is replaced with a token or hash that can be reversed with additional information (a key). Pseudonymized data **is still considered personal data** under the GDPR and remains within its scope.

This tool supports both:

- The default operators (`replace`, `mask`, `redact`) perform **anonymization**.
- The `hash` and `encrypt` operators (available via Presidio but not enabled by default) perform **pseudonymization**.

**If you use hashing or encryption, you are pseudonymizing, not anonymizing.** Make sure your use case and legal documentation reflect this distinction.

---

## 🧑‍💻 Development

### Setup

```bash
git clone https://github.com/Sahkaara/pii-anonymizer.git
cd pii-anonymizer
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -e .
pip install pytest
```

### Run the tests

```bash
pytest tests/ -v
```

Or, on Windows, to avoid PATH issues:

```cmd
python -m pytest tests/ -v
```

### Project structure

```
pii-anonymizer/
├── src/
│   └── pii_anonymizer/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface (Typer)
│       └── core.py         # Detection + anonymization logic (Presidio)
├── tests/
│   └── test_core.py        # Unit tests for the core logic
├── pyproject.toml          # Project metadata and dependencies
├── LICENSE
├── README.md
└── .gitignore
```

### Code style

The project follows [PEP 8](https://peps.python.org/pep-0008/) and uses type hints throughout. Docstrings follow the [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

---

## 🐛 Troubleshooting

### `pytest` is not recognized as an internal or external command

On Windows, the `pytest` executable may not be added to your `PATH`. Use the module form instead:

```cmd
python -m pytest tests/ -v
```

This works reliably and bypasses `PATH` issues.

### `AttributeError: 'AnalyzerEngine' object has no attribute 'get_supported_languages'`

The API of Presidio changed between versions. Use the attribute `analyzer.supported_languages` (without parentheses, without `get_`).

### `InvalidParamError: Expected parameter from_end`

Recent versions of Presidio require the `from_end` parameter for the `mask` operator. Add it to your operator configuration:

```python
OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 12, "from_end": False})
```

### `OSError: [E050] Can't find model 'en_core_web_lg'`

The spaCy model is not installed. Download it with:

```bash
python -m spacy download en_core_web_lg
```

### PowerShell: execution of scripts is disabled

If activating the virtual environment gives an execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then try activating the venv again.

### UnicodeDecodeError when reading a file

The tool assumes UTF-8 encoding. If your file uses a different encoding, convert it first:

```bash
iconv -f ISO-8859-1 -t UTF-8 input.txt > input_utf8.txt
```

On Windows, you can use PowerShell:

```powershell
Get-Content input.txt | Set-Content -Encoding UTF8 input_utf8.txt
```

---

## ❓ FAQ

### Is my data sent anywhere?

No. The tool runs entirely on your machine. No data is sent to any external server.

### Does it work with languages other than English?

Out of the box, only English. You can add support for other languages by registering additional spaCy models (see [Configuration](#️-configuration)).

### Can I use this in production?

The tool is functional and tested, but it's still an early-stage project. For production use, review the code, run extensive tests on your data, and consult a legal professional for compliance questions.

### How accurate is the detection?

Accuracy depends on the entity type and the spaCy model used. Pattern-based entities (emails, credit cards, IPs) are highly accurate. NLP-based entities (names, locations) are less accurate and may produce false positives or miss some occurrences.

### Can I use this to anonymize PDFs or CSVs?

Not yet. Currently, only plain text files are supported. Support for CSV, JSON, and PDF is on the [roadmap](#️-roadmap).

### Is this GDPR-compliant?

The tool helps you comply with GDPR by providing anonymization capabilities, but **it does not constitute legal advice**. Compliance depends on your specific use case, the nature of the data, and how you handle the anonymized output. Always consult a qualified legal professional.

---

## ⚠️ Known Limitations

While `pii-anonymizer` is effective for many common use cases, it relies on Microsoft Presidio and its underlying NLP models, which have some inherent limitations. Below are the currently known issues and edge cases:

- **Entity Confusion**: Presidio's recognizers for certain entities (e.g., `US_NATIONAL_ID`, `US_VISA`, `US_DRIVER_LICENSE`) use overlapping regex patterns. This can cause a visa number to be incorrectly classified as a driver's license, or vice versa. The tool uses the first match it finds, which may not always be the most precise one.
- **Contextual Misses**: In text with a very high density of PII (e.g., a line with multiple different entities), the analyzer may occasionally miss an entity. For example, a Social Security Number might be detected in one section of a document but missed in another if the surrounding context differs.
- **False Positives**: Common words or number sequences can sometimes be misclassified. For instance, the word "Annual" might be flagged as a `DATE_TIME`, or a long numeric string might be split into multiple incorrect entities.
- **PERSON Boundary Issues**: The `PERSON` recognizer sometimes includes trailing whitespace or newlines in its match. While this tool includes a post-processing step to restore lost newlines, the boundary detection is not perfect and may occasionally produce unexpected results.
- **Language Support**: Out of the box, only English (`en`) is fully supported. Support for other languages requires manual configuration of additional spaCy models.

These limitations are not bugs in the tool itself, but rather characteristics of the underlying NLP and pattern-matching engines. Future updates to Presidio or the addition of custom recognizers may mitigate some of these issues.

---

## 🗺️ Roadmap

Planned features and improvements:

- [ ] Support for additional file formats (CSV, JSON, JSONL, PDF, DOCX)
- [ ] Custom recognizers for non-US entities (Italian codice fiscale, IBAN, etc.)
- [ ] Configurable operators via a YAML/JSON config file
- [ ] Audit report (JSON/HTML) summarizing detected entities and actions taken
- [ ] "LLM-ready" mode: sanitize text before sending it to an external LLM
- [ ] REST API and/or web UI
- [ ] GitHub Actions CI pipeline
- [ ] Publishing to PyPI

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Sahkaara/pii-anonymizer/issues) if you want to contribute.

### How to contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Write clear commit messages.
- Add tests for new features.
- Update the README if you change user-facing behavior.
- Follow PEP 8 and use type hints.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is provided as-is, without any warranty. It is intended to assist with the anonymization of text data, but **it does not constitute legal advice**. The authors are not responsible for any misuse or for any legal consequences arising from the use of this software. Always consult a qualified legal professional for compliance questions, especially regarding the GDPR and other data protection regulations.

---

## 🙏 Acknowledgements

- [Microsoft Presidio](https://microsoft.github.io/presidio/) — the engine that powers PII detection and anonymization
- [spaCy](https://spacy.io/) — the NLP backbone behind Presidio
- [Typer](https://typer.tiangolo.com/) — for the elegant CLI framework

---

## 📬 Contact

- **Author**: [Francesco_Dinisi](https://github.com/Sahkaara)
- **Issues**: [GitHub Issues](https://github.com/Sahkaara/pii-anonymizer/issues)
