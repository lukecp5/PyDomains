# Py‑Domains

**Enrich domain datasets with content-category insights—via curated lists or predictive LSTM models.**

A Python package for classifying domain content using curated data sources (e.g. DMOZ, Shallalist, PhishTank) and LSTM-based models trained on them.

---

## 🔹 Installation

```bash
pip install pydomains
```

---

## 🔹 Quick Start

```python
import pandas as pd
from pydomains import *

# Load sample data
df = pd.DataFrame({'url': ['topshop.com', 'beyondrelief.com']})

# Lookup via curated lists
df = dmoz_cat(df, domain_names='url')     # DMOZ categories
df = phish_cat(df, domain_names='url')    # Phishtank (known phishing domains)

# Predict via LSTM models
df = pred_shalla(df, domain_names='url')      # Shallalist-based model
df = pred_toulouse(df, domain_names='url')    # Malware prediction model
```

---

## 🔹 API Overview

### Curated‑list lookups

| Function       | Source & Year       | Description                              |
|----------------|----------------------|------------------------------------------|
| `dmoz_cat`     | DMOZ (2016)          | Assigns categories from DMOZ listings    |
| `phish_cat`    | PhishTank (2017)     | Flags known phishing domains             |
| `shalla_cat`   | Shallalist (2017)    | Assigns categories from Shallalist       |

### LSTM‑based predictions

| Function         | Model Source         | Output                                      |
|------------------|----------------------|---------------------------------------------|
| `pred_shalla`    | Shallalist (2017)    | Category label + probability distribution   |
| `pred_toulouse`  | Malware dataset      | Malware prediction + probability            |
| `pred_phish`     | Curated + Alexa      | Phishing probability & label                |
| `pred_malware`   | Malware + Alexa      | Malware probability & label                 |

Each function appends new columns to the DataFrame with predicted labels and/or probabilities.

---

## 🔹 Why Use Py‑Domains?

- Quickly enrich domain datasets with topical or security categories.
- Integrates multiple sources: curated lists and machine learning models.
- Ideal for:
  - Web usage analytics
  - Threat intelligence enrichment
  - Academic or industry research
- Used in published research linking domain content to demographics.

---

## 🔹 Example: Full Workflow

```python
df = pd.read_csv("my_domains.csv")

# Annotate with category predictions
df = pred_shalla(df, domain_names='domain')

# Check phishing risk
df = pred_phish(df, domain_names='domain')

df.to_csv("domains_with_labels.csv", index=False)
```

---

## 🔹 Caveats & Notes

- List-based data is from 2016–2017 and may not reflect current trends.
- Classifiers are trained on historic data—accuracy may vary.
- Domain-level classification may not fully reflect webpage intent.
- Future improvements may include scraping, WHOIS, geolocation.

---

## 🔹 Contributing

Pull requests, issues, and suggestions are welcome!

- License: MIT

---

## 🔹 Credits

Originally created by [Luke Poirrier](https://github.com/lukecp5)

GitHub: [github.com/lukecp5](https://github.com/lukecp5)

---
