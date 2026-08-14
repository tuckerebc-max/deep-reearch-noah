#!/usr/bin/env python3
"""Report configured providers and the five-role assignment without exposing secrets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config


def main():
    paths = config.default_toml_paths()
    env = config.load_env_files()
    providers, agents = config.load_config(paths, env)
    print("Config files:", ", ".join(map(str, paths)) if paths else "none")
    if not providers:
        print("API providers: none")
        print("Consumer subscriptions alone do not supply API keys; use report-import mode or add keys.")
        return 0
    assignments, warnings = config.resolve_assignments(agents, providers)
    print("API providers:", ", ".join(sorted(providers)))
    print("Assignments:")
    for role, provider in assignments.items():
        print(f"  {role}: {provider} ({providers[provider].model})")
    print(f"Independent providers: {len(set(assignments.values()))}; strategies: {len(assignments)}")
    for warning in warnings:
        print("WARNING:", warning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
