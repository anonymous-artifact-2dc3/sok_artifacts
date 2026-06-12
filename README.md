# PromptSecurity Anonymous Artifact

This repository contains the anonymous artifact for a systematic evaluation of
jailbreak attacks, defenses, target models, and independent safety judgers. It
is intended to let reviewers reproduce the evaluation workflow, inspect the
collected prompt corpus, browse the leaderboard, and contribute additional
completed runs without exposing author identity.

Interactive leaderboard:

https://anonymous-artifact-2dc3.github.io/sok_artifacts/

## What Is Included

| Path | Purpose |
| --- | --- |
| `attacks/` | Implemented jailbreak attack modules and attack configs. |
| `defenses/` | Implemented defense modules and defense configs. |
| `models/` | API and local target-model wrappers plus runnable model configs. |
| `judgers/` | Independent safety judgers used by experiments and the leaderboard. |
| `dataset_loaders/` | Dataset adapters, including the balanced challenge split. |
| `jailbreakdb/` | Collected jailbreak prompt corpus, organized for anonymous release. |
| `experiments/` | Experiment launcher, config handling, and placeholder result schema. |
| `leaderboard_site/` | Static leaderboard site, data builder, and local preview script. |
| `ANONYMIZATION.md` | Anonymization notes for this public review artifact. |

## Quick Tutorial

### 1. Clone the artifact

```bash
git clone git@github.com:anonymous-artifact-2dc3/sok_artifacts.git
cd sok_artifacts
```

### 2. Install the Python dependencies

Use a fresh virtual environment if possible.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Some attacks and local model wrappers may require optional packages or a local
serving stack. If a component has extra requirements, keep those changes local
unless they are needed for a reproducible result contribution.

### 3. Configure credentials only when needed

Copy the template and fill only the providers or local paths you plan to run.
Never commit `.env` or provider account metadata.

```bash
cp .env.example .env
```

Common keys include:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
DEEPINFRA_API_KEY=
DOUBAO_API_KEY=
```

### 4. Inspect available components

Most runnable components are configured through JSON files.

```bash
find attacks -name "*.json" | sort
find defenses -name "*.json" | sort
find judgers/configs judgers/usage_examples/configs -name "*.json" | sort
find models/usage_examples/configs -name "*.json" | sort
```

The complete implemented attack, defense, model, and judger lists are also
included below in [Implemented Components](#implemented-components).

### 5. Run a small experiment

The experiment CLI writes completed or resumable placeholder JSON files under
`experiments/placeholders/`. The exact command depends on which model provider
and local serving stack are available in your environment.

Example smoke-test shape:

```bash
python -m experiments \
  --model gpt-4.1 \
  --attack ArtPrompt \
  --defense no_defense \
  --dataset balanced_challenge \
  --judger gpt_judger_harmful_binary \
  --sample-limit 5 \
  --seed 0
```

For paper-compatible leaderboard runs, use the balanced challenge dataset and
record the three independent judgers listed in the leaderboard section.

### 6. Build and preview the leaderboard locally

```bash
mkdir -p leaderboard_site/data/runs
python leaderboard_site/scripts/build_leaderboard_data.py \
  --input-dir experiments/placeholders \
  --utility-input-dir experiments/placeholders_utility \
  --bundle-runs-dir leaderboard_site/data/runs \
  --output leaderboard_site/data/leaderboard.json
cd leaderboard_site
python -m http.server 8080
```

Open `http://localhost:8080/` in a browser.

## Data: JailbreakDB

The collected prompt corpus is provided in `jailbreakdb/`. It contains a
normalized metadata index, source-grouped prompt files, and a machine-readable
manifest for the anonymous release. See:

[`jailbreakdb/README.md`](jailbreakdb/README.md)

The corpus is included as a static artifact. Do not add source URLs, account
identifiers, local paths, or any private collection notes when contributing
changes.

## Leaderboard

The static leaderboard is built from completed placeholder result files and is
served from `leaderboard_site/`.

Public anonymous page:

https://anonymous-artifact-2dc3.github.io/sok_artifacts/

Paper-compatible leaderboard scope:

| Dimension | Scope |
| --- | --- |
| Target models | 11 paper main models. |
| Attack settings | 20 paper attack settings, separated into black-box and white-box views. |
| Defense settings | 9 defense methods plus the `no_defense` baseline where applicable. |
| Judgers | `harmbench_judger`, `gpt_judger_harmful_binary`, `rejection_prefix_judger`. |
| Primary ASR | Computed with `gpt_judger_harmful_binary`. |
| Harmful dataset | `balanced_challenge`. |

The comparison page also exposes results by independent judger. The overview
and main ranked tables intentionally use the GPT HarmBench-style binary judger
for ASR consistency.

## Contributing New Leaderboard Results

Do not edit `leaderboard_site/data/leaderboard.json` by hand. Contribute the
completed placeholder result files and rebuild the static leaderboard.

### Accepted harmful-run placeholders

Place completed harmful-run JSON files in:

```text
experiments/placeholders/
```

A paper-compatible harmful run must include:

- `status` set to `success`, `completed`, or `complete`.
- `dataset_name` or `config.dataset` set to `balanced_challenge`.
- A paper-compatible model, attack, and defense name.
- Sample-level outputs in `sample_results`.
- `sample_index` for each evaluated sample.
- `judger_individual_results` containing `gpt_judger_harmful_binary`.
- Preferably all three judgers: `harmbench_judger`, `gpt_judger_harmful_binary`, and `rejection_prefix_judger`.

Minimal harmful placeholder shape:

```json
{
  "status": "success",
  "target_llm_name": "gpt-4.1",
  "attack_method": "ArtPrompt",
  "defense_method": "no_defense",
  "dataset_name": "balanced_challenge",
  "judger_name": [
    "harmbench_judger",
    "gpt_judger_harmful_binary",
    "rejection_prefix_judger"
  ],
  "total_samples": 100,
  "successful_samples": 100,
  "failed_samples": 0,
  "sample_results": [
    {
      "status": "success",
      "sample_index": 0,
      "judger_individual_results": {
        "harmbench_judger": 0,
        "gpt_judger_harmful_binary": 0,
        "rejection_prefix_judger": 1
      },
      "attack_query_count": 1,
      "llm_response_time_under_defense": 1.23
    }
  ]
}
```

The leaderboard builder accepts both top-level fields and nested `config`
fields for `model`, `attack`, `defense`, `dataset`, and `judger`.

### Accepted utility placeholders

Place completed utility-run JSON files in:

```text
experiments/placeholders_utility/
```

Utility runs are associated with the corresponding defense and should contain
sample-level utility metrics such as accuracy or refusal rate.

Minimal utility placeholder shape:

```json
{
  "status": "success",
  "target_llm_name": "gpt-4.1",
  "defense_method": "smooth_llm",
  "dataset_name": "utility_mcq",
  "total_samples": 100,
  "successful_samples": 100,
  "sample_results": [
    {
      "status": "success",
      "sample_index": 0,
      "judger_result": {
        "acc": 1,
        "rr": 0,
        "ppl": 12.4,
        "rl": 54
      }
    }
  ]
}
```

### Rebuild before opening a pull request

```bash
mkdir -p leaderboard_site/data/runs
python leaderboard_site/scripts/build_leaderboard_data.py \
  --input-dir experiments/placeholders \
  --utility-input-dir experiments/placeholders_utility \
  --bundle-runs-dir leaderboard_site/data/runs \
  --output leaderboard_site/data/leaderboard.json
```

Then preview:

```bash
cd leaderboard_site
python -m http.server 8080
```

Contribution checklist:

- Include completed placeholder JSON files needed to reproduce the aggregate.
- Include the rebuilt `leaderboard_site/data/leaderboard.json`.
- Include bundled run payloads under `leaderboard_site/data/runs/` if row-level inspection should work.
- Do not include `.env`, API keys, local absolute paths, cache directories, raw debug logs, or provider account metadata.
- Keep result descriptions anonymous: describe component names and sample counts, not who ran them.
- If adding a new model, attack, defense, or judger beyond the paper-compatible scope, include its config and implementation files. To appear in ranked paper-compatible tables, the component must also be added to the leaderboard builder allow-lists with its access setting documented.

## Implemented Components

### Paper-Compatible Main Models

These 11 model settings are used by the main paper-compatible leaderboard.

- `claude-sonnet-4-20250514`
- `gemini-3-flash-preview`
- `gpt-5.2`
- `gpt-4.1`
- `deepseek-v3`
- `doubao-seed-1-6-flash-250615`
- `mistralai_Ministral-8B-Instruct-2410`
- `microsoft_Phi-4-instruct`
- `Qwen_Qwen3-8B`
- `meta-llama_Llama-3.1-8B-Instruct`
- `01-AI_Yi-1.5-6B-Chat`

### Paper-Compatible Attack Settings

Black-box attack settings:

- `ABJAttack`
- `CodeChameleon`
- `ReNeLLM`
- `GPTFUZZER`
- `TapAttack`
- `FlipAttack`
- `PAIR`
- `PastTense`
- `InceptionAttack`
- `DRA`
- `CodeAttack`
- `DrAttack`
- `MultilingualJailbreakAttack`
- `ArtPrompt`
- `ResponseAttack`
- `PersuasiveInContext`

White-box attack settings:

- `IFSJAttack`
- `AutoDANAttack`
- `COLDAttack`
- `GCGAttack`

### Implemented Attack Modules

Configured attack modules present in `attacks/`:

- `no_attack`
- `ABJAttack`
- `ArtPrompt`
- `AutoDAN`
- `COLD`
- `CodeAttack`
- `CodeChameleon`
- `DRA`
- `DrAttack`
- `FlipAttack`
- `GCGAttack`
- `GPTFUZZER`
- `IFSJ`
- `InceptionAttack`
- `MultilingualJailbreak`
- `PAIR`
- `PastTense`
- `PersuasiveInContext`
- `ReNeLLM`
- `TapAttack`

Some implementation config names are shorter than the canonical leaderboard
names. The leaderboard builder normalizes to the paper-compatible names listed
above.

### Implemented Defenses

Baseline:

- `no_defense`

Black-box-compatible defenses:

- `back_translation`
- `input_filter_defense`
- `jailguard_defense`
- `output_filter_defense`
- `smooth_llm`

White-box defenses:

- `gradsafe_defense`
- `perplexity_filter`
- `prime_guard`
- `rpo`

### Implemented Judgers

Paper-compatible leaderboard judgers:

- `harmbench_judger`
- `gpt_judger_harmful_binary`
- `rejection_prefix_judger`

Additional implemented judger configs:

- `gpt_judger_contextual_harmbench`
- `gpt_judger_harmbench_style`
- `gpt_judger_openai_policy`
- `gpt_judger_tap_style`

### Implemented API Model Configs

The repository includes 103 API model configs under
`models/usage_examples/configs/api/`.

<details>
<summary>Show API model config names</summary>

- `01-ai-Yi-34B-Chat`
- `Austism-chronos-hermes-13b-v2`
- `Gryphe-MythoMax-L2-13b`
- `Gryphe-MythoMax-L2-13b-turbo`
- `HuggingFaceH4-zephyr-orpo-141b-A35b-v0.1`
- `NousResearch-Hermes-3-Llama-3.1-405B`
- `Qwen-QwQ-32B-Preview`
- `Qwen-Qwen2-72B-Instruct`
- `Qwen-Qwen2-7B-Instruct`
- `Qwen-Qwen2.5-7B-Instruct`
- `Sao10K-L3-70B-Euryale-v2.1`
- `Sao10K-L3.1-70B-Euryale-v2.2`
- `claude-2.0`
- `claude-2.1`
- `claude-3-5-haiku-20241022`
- `claude-3-5-sonnet-20240620`
- `claude-3-5-sonnet-20241022`
- `claude-3-5-sonnet-latest`
- `claude-3-haiku-20240307`
- `claude-3-opus-20240229`
- `claude-3-opus-latest`
- `claude-3-sonnet-20240229`
- `claude-4`
- `claude-haiku-4-5-20251001`
- `claude-instant-1.2`
- `claude-sonnet-4-20250514`
- `cognitivecomputations-dolphin-2.6-mixtral-8x7b`
- `cognitivecomputations-dolphin-2.9.1-llama-3-70b`
- `deepinfra-airoboros-70b`
- `deepseek-ai-DeepSeek-R1-0528-Turbo`
- `deepseek-ai-DeepSeek-V2.5`
- `deepseek-ai-DeepSeek-V3`
- `deepseek-ai-deepseek-chat`
- `deepseek-ai-deepseek-coder`
- `deepseek-r1`
- `deepseek-v3`
- `doubao-1-5-pro-32k-250115`
- `doubao-seed-1-6-250615`
- `doubao-seed-1-6-flash-250615`
- `gemini-1.0-pro`
- `gemini-1.0-pro-latest`
- `gemini-1.5-flash`
- `gemini-1.5-flash-002`
- `gemini-1.5-flash-8b`
- `gemini-1.5-flash-8b-latest`
- `gemini-1.5-flash-latest`
- `gemini-1.5-pro`
- `gemini-1.5-pro-002`
- `gemini-1.5-pro-latest`
- `gemini-2.0-flash`
- `gemini-2.0-flash-exp`
- `gemini-2.0-flash-thinking-exp-1219`
- `gemini-2.5-flash`
- `gemini-2.5-pro`
- `gemini-3-flash-preview`
- `gemini-3.0-flash`
- `gemini-3.0-pro`
- `google-gemma-1.1-7b-it`
- `google-gemma-2-27b-it`
- `google-gemma-2-9b-it`
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-0125`
- `gpt-3.5-turbo-1106`
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4.1`
- `gpt-4.1-mini`
- `gpt-4.1-nano`
- `gpt-4o`
- `gpt-4o-latest`
- `gpt-4o-mini`
- `gpt-5`
- `gpt-5-codex`
- `gpt-5.2`
- `gpt-5.2-codex`
- `gpt-5.2-codex-mini`
- `gpt-5.2-mini`
- `gpt-5.2-nano`
- `gpt-o3`
- `meta-llama-Llama-2-13b-chat-hf`
- `meta-llama-Llama-2-70b-chat-hf`
- `meta-llama-Llama-2-7b-chat-hf`
- `meta-llama-Llama-3.2-11B-Vision-Instruct`
- `meta-llama-Llama-3.2-90B-Vision-Instruct`
- `meta-llama-Llama-3.3-70B-Instruct`
- `meta-llama-Llama-4-405B-Instruct`
- `meta-llama-Meta-Llama-3.1-405B-Instruct`
- `meta-llama-Meta-Llama-3.1-70B-Instruct`
- `meta-llama-Meta-Llama-3.1-8B-Instruct`
- `microsoft-Phi-3-medium-4k-instruct`
- `microsoft-WizardLM-2-7B`
- `microsoft-WizardLM-2-8x22B`
- `mistralai-Mistral-7B-Instruct-v0.3`
- `mistralai-Mistral-Large-Instruct-2407`
- `mistralai-Mixtral-8x22B-Instruct-v0.1`
- `nvidia-Llama-3.1-Nemotron-70B-Instruct`
- `nvidia-Nemotron-4-340B-Instruct`
- `o1`
- `o1-mini`
- `o1-preview`
- `openchat-openchat-3.6-8b`
- `qwen-Qwen2.5-72B-Instruct`
- `qwen-Qwen2.5-Coder-32B-Instruct`

</details>

### Implemented Local Model Configs

The repository includes 60 local model configs under
`models/usage_examples/configs/local/`.

<details>
<summary>Show local model config names</summary>

- `01-AI-Yi-1.5-34B-Chat`
- `01-AI-Yi-1.5-6B-Chat`
- `01-AI-Yi-1.5-9B-Chat`
- `Qwen-QwQ-32B-Preview`
- `Qwen-Qwen2-0.5B-Instruct`
- `Qwen-Qwen2-1.5B-Instruct`
- `Qwen-Qwen2-72B-Instruct`
- `Qwen-Qwen2-7B-Instruct`
- `Qwen-Qwen2.5-0.5B-Instruct`
- `Qwen-Qwen2.5-1.5B-Instruct`
- `Qwen-Qwen2.5-14B-Instruct`
- `Qwen-Qwen2.5-32B-Instruct`
- `Qwen-Qwen2.5-3B-Instruct`
- `Qwen-Qwen2.5-72B-Instruct`
- `Qwen-Qwen2.5-7B-Instruct`
- `Qwen-Qwen2.5-Coder-1.5B-Instruct`
- `Qwen-Qwen2.5-Coder-32B-Instruct`
- `Qwen-Qwen2.5-Coder-7B-Instruct`
- `Qwen-Qwen3-0.6B`
- `Qwen-Qwen3-1.7B`
- `Qwen-Qwen3-14B`
- `Qwen-Qwen3-32B`
- `Qwen-Qwen3-4B`
- `Qwen-Qwen3-8B`
- `google-gemma-2-27b-it`
- `google-gemma-2-2b-it`
- `google-gemma-2-9b-it`
- `google-gemma-3-1b-it`
- `internlm-internlm2-5-1.8b-chat`
- `internlm-internlm2-5-7b-chat`
- `internlm-internlm2.5-20b-chat`
- `meta-llama-Llama-2-13b-chat-hf`
- `meta-llama-Llama-2-70b-chat-hf`
- `meta-llama-Llama-2-7b-chat-hf`
- `meta-llama-Llama-3-70B-Instruct`
- `meta-llama-Llama-3-8B-Instruct`
- `meta-llama-Llama-3.1-405B-Instruct`
- `meta-llama-Llama-3.1-405B-Instruct-FP8`
- `meta-llama-Llama-3.1-70B-Instruct`
- `meta-llama-Llama-3.1-8B-Instruct`
- `meta-llama-Llama-3.2-11B-Vision-Instruct`
- `meta-llama-Llama-3.2-1B-Instruct`
- `meta-llama-Llama-3.2-3B-Instruct`
- `meta-llama-Llama-3.2-90B-Vision-Instruct`
- `meta-llama-Llama-3.3-70B-Instruct`
- `meta-llama-Llama-4-Scout-17B-16E-Instruct`
- `microsoft-Phi-2-instruct`
- `microsoft-Phi-3-medium-128k-instruct`
- `microsoft-Phi-3-medium-4k-instruct`
- `microsoft-Phi-3-mini-128k-instruct`
- `microsoft-Phi-3-mini-4k-instruct`
- `microsoft-Phi-3-small-128k-instruct`
- `microsoft-Phi-3-small-4k-instruct`
- `microsoft-Phi-3-small-8k-instruct`
- `microsoft-Phi-3.5-MoE-instruct`
- `microsoft-Phi-3.5-mini-instruct`
- `microsoft-Phi-4-instruct`
- `mistralai-Ministral-8B-Instruct-2410`
- `mistralai-Mistral-7B-Instruct-v0.3`
- `mistralai-Mistral-Nemo-Instruct-2407`

</details>

## Anonymity Requirements

When using or extending this artifact during review:

- Do not commit secrets, `.env`, provider account identifiers, or local absolute paths.
- Do not add institution names, author names, internal repository URLs, or non-anonymous project links.
- Do not describe datasets as mirrors or exports from a named hosting account.
- Keep contributed result files limited to reproducible configs, aggregate metrics, and sample-level fields needed by the leaderboard.
- Prefer generic descriptions such as "anonymous artifact", "collected prompt corpus", and "leaderboard contribution".
