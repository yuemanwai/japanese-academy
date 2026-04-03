#!/usr/bin/env bash

set -euo pipefail

# Run with: ./compile_requirements.sh
# Run this from the repository root after editing requirements.in or requirements-dev.in.
# It regenerates both compiled lockfiles so the demo stays in sync.

uv pip compile --python 3.10 requirements.in -o requirements.txt
uv pip compile --python 3.10 requirements-dev.in -o requirements-dev.txt
