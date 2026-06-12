"""Environment-backed API key configuration for the anonymous artifact."""

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or GOOGLE_API_KEY
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
