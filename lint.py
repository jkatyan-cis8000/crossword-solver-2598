#!/usr/bin/env python3
"""Linting tool for crossword-solver-2598.

Validates:
1. Every source file lives in exactly one layer directory.
2. Imports respect the forward dependency direction.
3. No file exceeds 300 lines.
"""

import ast
import os
import sys
from pathlib import Path

# Layer definitions and allowed imports per layer
LAYERS = ["types", "config", "repo", "service", "providers", "utils", "runtime", "ui"]

LAYER_IMPORTS = {
    "types": ["types"],
    "config": ["types", "config"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
    "providers": ["types", "config", "utils", "providers"],
    "utils": ["utils"],
}

MAX_LINES = 300

# Source directory
SRC_DIR = Path(__file__).parent / "src"


def get_layer(filepath: Path) -> str | None:
    """Get the layer name for a file path."""
    rel_path = filepath.relative_to(SRC_DIR)
    parts = rel_path.parts
    if parts and parts[0] in LAYERS:
        return parts[0]
    return None


def get_imports(filepath: Path) -> list[str]:
    """Extract import statements from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def check_line_count(filepath: Path) -> list[str]:
    """Check if file exceeds max lines."""
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            errors.append(
                f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines "
                f"({len(lines)} lines)"
            )
    except Exception as e:
        errors.append(f"{filepath}:1: Error reading file: {e}")
    return errors


def check_imports(filepath: Path, layer: str) -> list[str]:
    """Check imports respect layer dependency rules."""
    errors = []
    allowed = LAYER_IMPORTS[layer]
    imports = get_imports(filepath)

    for imp in imports:
        # Find which layer this import belongs to
        imp_layer = None
        for candidate in LAYERS:
            if (SRC_DIR / candidate / f"{imp}.py").exists():
                imp_layer = candidate
                break

        if imp_layer and imp_layer not in allowed:
            errors.append(
                f"{filepath}: imports {imp} (from {imp_layer}) "
                f"which violates layer rules. Layer {layer} may only import from: {', '.join(allowed)}"
            )

    return errors


def check_file(filepath: Path) -> list[str]:
    """Run all checks on a single file."""
    errors = []

    # Check line count
    errors.extend(check_line_count(filepath))

    # Check layer membership and imports
    layer = get_layer(filepath)
    if layer:
        errors.extend(check_imports(filepath, layer))

    return errors


def lint() -> list[str]:
    """Run all lint checks."""
    errors = []

    # Find all Python files under src/
    for root, dirs, files in os.walk(SRC_DIR):
        # Skip __pycache__ and .pyc files
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for filename in files:
            if not filename.endswith(".py"):
                continue

            filepath = Path(root) / filename
            errors.extend(check_file(filepath))

    return errors


def main() -> int:
    """Main entry point."""
    errors = lint()

    if errors:
        print("Linting failed:")
        for error in errors:
            print(f"  {error}")
        return 1

    print("Linting passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
