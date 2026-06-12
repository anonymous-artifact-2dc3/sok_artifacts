# JailbreakDB

This directory contains the JailbreakDB data bundled with the anonymous
artifact. It includes two data layers:

- Prompt corpus records under `prompt_corpus/`.
- PromptSecurity-Eval measurement records under `promptsecurity_eval/`.

Large CSV files are split into GitHub-safe gzip-compressed CSV shards. Each
shard repeats the CSV header, and shards can be concatenated by split name.

## Collected Prompt Corpus

The prompt corpus is a consolidated collection assembled from public
prompt-security, jailbreak, defense, and survey resources, then normalized into
a shared five-column schema. It contains 445,752 jailbreak/adversarial prompt
records from 48 sources and 1,094,122 benign prompt records from 14 sources.

The collection preserves source-level provenance through the `source` field
while using a common `system_prompt` / `user_prompt` representation for model
execution. The `jailbreak` field is the binary prompt label: `1` denotes a
jailbreak/adversarial prompt record and `0` denotes a benign prompt record. The
`tactic` field records whether the prompt text includes an evasion tactic such
as rewriting, wrapping, role-play, encoding, translation, or template-based
framing when this distinction is available; `0` denotes prompts without such a
marked tactic. Duplicate prompt records were removed before sharding.

## Contents

| Path | Records | Description |
|---|---:|---|
| `prompt_corpus/text_jailbreak_unique_parts/part-*.csv.gz` | 445,752 | Jailbreak/adversarial prompt corpus records. |
| `prompt_corpus/text_regular_unique_parts/part-*.csv.gz` | 1,094,122 | Benign prompt corpus records. |
| `promptsecurity_eval/data/sample_records/harmful_main_parts/part-*.csv.gz` | 167,200 | Main harmful-query sample-level evaluation records. |
| `promptsecurity_eval/data/sample_records/benign_utility.csv.gz` | 9,200 | Normal-question utility sample-level records. |
| `promptsecurity_eval/data/sample_records/baseline_calibration.csv.gz` | 8,700 | Baseline-calibration sample-level records. |
| `promptsecurity_eval/data/run_records/harmful_main.csv.gz` | 1,672 | Run-level metadata for the main harmful-query evaluation. |
| `promptsecurity_eval/data/run_records/benign_utility.csv.gz` | 92 | Run-level metadata for normal-question utility evaluation. |
| `promptsecurity_eval/data/run_records/baseline_calibration.csv.gz` | 87 | Run-level metadata for baseline calibration. |
| `promptsecurity_eval/data/prompt_samples/balanced_challenge.csv.gz` | 100 | Selected harmful-query prompt subset used by the main evaluation. |
| `manifest.json` | - | Shard-level counts and file layout. |
| `schema.json` | - | Compact schema description. |

## Loading

```python
from pathlib import Path

import pandas as pd

base = Path("jailbreakdb")

jailbreak_prompts = pd.concat(
    [
        pd.read_csv(path)
        for path in sorted((base / "prompt_corpus/text_jailbreak_unique_parts").glob("part-*.csv.gz"))
    ],
    ignore_index=True,
)

regular_prompts = pd.concat(
    [
        pd.read_csv(path)
        for path in sorted((base / "prompt_corpus/text_regular_unique_parts").glob("part-*.csv.gz"))
    ],
    ignore_index=True,
)

harmful_main = pd.concat(
    [
        pd.read_csv(path)
        for path in sorted(
            (base / "promptsecurity_eval/data/sample_records/harmful_main_parts").glob("part-*.csv.gz")
        )
    ],
    ignore_index=True,
)

benign_utility = pd.read_csv(base / "promptsecurity_eval/data/sample_records/benign_utility.csv.gz")
baseline_calibration = pd.read_csv(base / "promptsecurity_eval/data/sample_records/baseline_calibration.csv.gz")
```

To reconstruct the original single-file CSV layout for a sharded split:

```python
jailbreak_prompts.to_csv("text_jailbreak_unique.csv", index=False)
regular_prompts.to_csv("text_regular_unique.csv", index=False)
harmful_main.to_csv("harmful_main.csv", index=False)
```

## Prompt Corpus Schema

The prompt corpus CSV shards use:

| Field | Meaning |
|---|---|
| `system_prompt` | Optional system-side instruction associated with the prompt. |
| `user_prompt` | User-side prompt text. |
| `jailbreak` | Binary prompt label; `1` denotes jailbreak/adversarial prompt and `0` denotes benign prompt. |
| `source` | Source corpus or collection from which the prompt was collected. |
| `tactic` | Prompt tactic or category when available. |

## Safety Notice

The records may contain harmful, offensive, or disturbing prompts and model
outputs. They are released strictly for research on model safety, jailbreak
robustness, defense evaluation, and judger behavior.
