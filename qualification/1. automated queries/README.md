[← Back to Qualification](../README.md)

## 1. Definition and Generation of Search Strings

This step consists of translating the search strategy defined in the Scoping Review (Step 0) into the specific syntax required by scientific databases (ACM, IEEE, Scopus, Web of Science, etc.).

The process is automated via a Python script to ensure consistency and facilitate rapid iterations on search terms.

### 📂 File Structure

- **`config.ini`**: Central configuration file. Defines key terms grouped by concepts and exclusion criteria.
- **`generateQueries.py`**: Script that reads the configuration file and compiles formatted search strings for each database.
- **`generated_queries/`**: Output directory where the ready-to-use queries are saved.

### ⚙️ Search Configuration (`config.ini`)

The search strategy is based on the intersection of four main domains, configured in the `config.ini` file. The applied logic is: `(PROBLEM) AND (TECHNOLOGY) AND (AI) AND (DOMAIN)`.

The defined term groups are:

- **`[PROBLEM_CONCEPTS]`** (Problem Concepts): _collision avoidance, detect and avoid, conflict resolution_, etc.
- **`[TECHNOLOGY_CONCEPTS]`** (Technology Concepts): _radar, synthetic aperture radar (SAR)_, etc.
- **`[AI_CONCEPTS]`** (AI Concepts): _machine learning, neural networks, deep learning_, etc.
- **`[DOMAIN_CONCEPTS]`** (Domain Concepts): _UAV, drone, aircraft, UAM_, etc.

Exclusion filters (`NOT`) are also applied to metadata and titles (e.g., _camera, image-based, marine_).

### 🚀 Execution

To generate or update the search strings after modifying `config.ini`, run:

```bash
python generateQueries.py
```

This will produce formatted search strings for each target database in the `generated_queries/` directory, these text files containing the exact query to copy and paste into each search engine:

- ACM: ACM.query
- AIAA: AIAA.query
- IEEE: IEEE.query
- NASA RTL: NASA.query
- Scopus: SCOPUS.query
- Web of Science: WOS.query

> Reproducibility Note: Using the script ensures that any changes to inclusion/exclusion terms are propagated identically to all database syntaxes (automatically adjusting parentheses and logical operators).
