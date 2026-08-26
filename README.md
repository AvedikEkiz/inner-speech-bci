# Inner Speech Dataset — Data Loading and Analysis

Code for working with an EEG inner speech dataset.  
Two language sets: **Russian** (12 subjects, 14 words) and **Spanish** (10 subjects, 12 words).

## Dataset Structure (v2)

```
<base>/
├── raw/
│   ├── russian/
│   │   ├── sub1/
│   │   │   └── sub1_session.edf
│   │   └── sub2/ ... sub12/
│   └── spanish/
│       └── sub0/ ... sub9/
├── preprocessed/
│   ├── russian/
│   │   ├── sub1/
│   │   │   ├── sub1_epochs.fif
│   │   │   └── sub1.xlsx
│   │   └── sub2/ ... sub12/
│   └── spanish/
│       └── sub0/ ... sub9/
├── metadata/
│   └── subject_metadata.json
├── manifest.csv
├── data_dictionary.md
└── readme.md
```

## Event Labels

Each word was recorded under two speech conditions:

| Suffix | Condition | Example |
|--------|-----------|---------|
| `1`    | overt (spoken aloud) | `BACK1`, `UP1` |
| `2`    | inner (imagined) | `BACK2`, `UP2` |

Service markers `GO` and `GZ` denote block onset and rest period respectively.  
Labels `NEXT1` / `NEXT2` are present only in the Russian set.

Full label reference: `utils.LABEL_INFO`.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import utils
from pathlib import Path

# Set dataset root once
utils.DEFAULT_BASE = Path('/path/to/inner_speech_v2')

from utils import load_epochs, load_all_languages, LABEL_INFO, ATYPICAL

# Single subject
epochs = load_epochs('sub2', 'Russian')
print(epochs)

# Select by condition
epochs_inner = epochs[[l for l in epochs.event_id if l.endswith('2')]]
epochs_overt = epochs[[l for l in epochs.event_id if l.endswith('1')]]

# All subjects, both languages
all_data = load_all_languages()
# → {'Russian': {'sub1': Epochs, ...}, 'Spanish': {...}}

# Label reference table
print(LABEL_INFO)

# Atypical subjects (alternative recording paradigm)
print(ATYPICAL)
```

See [example_usage.ipynb](example_usage.ipynb) for a detailed walkthrough.

## Atypical Subjects

A subset of Russian subjects (sub1, sub3, sub5, sub10) were recorded under an alternative paradigm: a single marker covered a block of repetitions (~10–15 s), with epochs cut post-hoc at 1 s intervals. These subjects are flagged in `utils.ATYPICAL`.

## Epoch Window

`tmin = -0.5 s`, `tmax ≈ 1.0 s` relative to marker onset. No baseline correction applied.

## Files

| File | Description |
|------|-------------|
| `utils/loader.py` | Functions for loading EDF, FIF, and XLSX files |
| `utils/labels.py` | Label reference table and constants |
| `example_usage.ipynb` | Data loading and usage examples |

## Citing

If you use this dataset in your work, please cite:

> Kostulin DV, Shaposhnikov PD, Ekizyan AK, Shevchenko IG, Shaposhnikov DG, Shcherban IV, Kiroy VN. EEG-based brain-computer interface (BCI) dataset for directional word recognition. *Sci Data*. 2026 Aug 17;13(1):1195. doi: 10.1038/s41597-026-07809-9. PMID: 42608413; PMCID: PMC13482365.

BibTeX:
```bibtex
@article{Kostulin2026,
  author  = {Kostulin, D. V. and Shaposhnikov, P. D. and Ekizyan, A. K. and
             Shevchenko, I. G. and Shaposhnikov, D. G. and Shcherban, I. V. and
             Kiroy, V. N.},
  title   = {EEG-based brain-computer interface (BCI) dataset for directional word recognition},
  journal = {Scientific Data},
  year    = {2026},
  volume  = {13},
  number  = {1},
  pages   = {1195},
  doi     = {10.1038/s41597-026-07809-9},
  url     = {https://doi.org/10.1038/s41597-026-07809-9},
  note    = {PMID: 42608413; PMCID: PMC13482365}
}
```
