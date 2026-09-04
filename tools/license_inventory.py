from importlib.metadata import distributions


def get_license(metadata) -> str:
    license_expression = metadata.get("License-Expression")

    if license_expression:
        return license_expression.strip()

    license_name = metadata.get("License")

    if license_name:
        return license_name.strip()

    classifiers = metadata.get_all("Classifier") or []

    license_classifiers = [
        classifier
        for classifier in classifiers
        if classifier.startswith("License ::")
    ]

    if license_classifiers:
        return " | ".join(license_classifiers)

    return "UNKNOWN"


def main():
    packages = []

    for distribution in distributions():
        metadata = distribution.metadata

        name = metadata.get("Name")

        if not name:
            continue

        version = metadata.get("Version", "UNKNOWN")
        license_name = get_license(metadata)

        packages.append(
            (
                name.lower(),
                name,
                version,
                license_name,
            )
        )

    packages.sort()

    print(
        f"{'Package':35} "
        f"{'Version':15} "
        f"License"
    )

    print("-" * 120)

    for _, name, version, license_name in packages:
        print(
            f"{name:35} "
            f"{version:15} "
            f"{license_name}"
        )


if __name__ == "__main__":
    main()
