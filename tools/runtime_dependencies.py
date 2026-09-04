from importlib.metadata import PackageNotFoundError, version


RUNTIME_PACKAGES = [
    "pymupdf",
    "sentence-transformers",
]


def get_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "NOT INSTALLED"


def main() -> None:
    print("LocalDoc Runtime Dependencies")
    print("=" * 40)

    for package in RUNTIME_PACKAGES:
        print(f"{package}=={get_version(package)}")


if __name__ == "__main__":
    main()
