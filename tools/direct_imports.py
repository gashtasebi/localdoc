import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILES_TO_SCAN = [
    PROJECT_ROOT / "main.py",
    PROJECT_ROOT / "src",
]


def collect_python_files() -> list[Path]:
    files = []

    for target in FILES_TO_SCAN:
        if target.is_file() and target.suffix == ".py":
            files.append(target)

        elif target.is_dir():
            files.extend(target.rglob("*.py"))

    return sorted(files)


def extract_imports(file_path: Path) -> set[str]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def main() -> None:
    all_imports = set()

    for file_path in collect_python_files():
        imports = extract_imports(file_path)

        print(f"\n{file_path.relative_to(PROJECT_ROOT)}")

        for name in sorted(imports):
            print(f"  - {name}")

        all_imports.update(imports)

    print("\n" + "=" * 40)
    print("ALL DIRECT IMPORTS")
    print("=" * 40)

    for name in sorted(all_imports):
        print(name)


if __name__ == "__main__":
    main()
