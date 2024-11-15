# json-diff-checker

## Table of Contents

- [Description](#description)
- [Usage](#usage)
  - [Locally](#locally)
  - [Docker](#docker)
- [Example Usage](#example-usage)
- [Contributions](#contributions)
- [License](#license)

## Description

This script compares JSON files in two directories corresponding to different versions of a project. It uses `json-diff` to find differences between JSON files from the current version and the next version. The results are saved to a specified output file.

**The script assumes that directory names and file names are consistent, differing only by version number.**

The project has been dockerized to simplify usage and ensure a consistent environment. You can [run the script within a Docker container](#docker), which includes all necessary dependencies.

## Usage

- Clone the repository:

    ```bash
    git clone https://github.com/idb_antonioalanis/json-diff-checker.git
    ```

- Navigate to the project directory:

    ```bash
    cd json-diff-checker/json-diff-checker
    ```

You can use the script [locally](#locally) or via [Docker](#docker).

### Locally

To use the script locally, follow these steps:

- Make sure you have Python 3.6 or higher installed. You can install it via `apt`:

    ```bash
    sudo apt update && \
    sudo apt install -y python3
    ```

- Make sure you have `json-diff` installed. You can install it via `npm`:

    ```bash
    npm install -g json-diff
    ```

- Finally, run the script:

    ```bash
    python3 json_diff_checker.py \
      --version <version> \
      --next_version <next_version> \
      --version_folder_path <version_folder_path> \
      [--output_filename <output_filename>]
    ```

    - `--version` (required): The current version to compare.
    - `--next_version` (required): The next version to compare.
    - `--version_folder_path` (required): The name of the folder for the first version. The folder name for the next version will be automatically generated by replacing the version number.
    - `--output_filename` (optional): The name of the output file (default: `output.txt`).

    Replace `<version>`, `<next_version>`, `<version_folder_path>`, and `<output_filename>` with the appropriate values for your case.

### Docker

If you prefer to use Docker to run the script, follow these steps:

- Make sure you have Docker installed on your machine. You can install it via `apt`:

    ```bash
    sudo apt update && \
    sudo apt install docker.io
    ```

- Finally, run [build-and-run-image.sh](build-and-run-image.sh) script:

    ```bash
    ./build_and_run_image.sh \
        --version <version> \
        --next_version <next_version> \
        --version_folder_path <version_folder_path> \
        --next_version_folder_path <next_version_folder_path> \
        [--output_filename <output_filename>]
    ```

    - `--version` (required): The current version to compare.
    - `--next_version` (required): The next version to compare.
    - `--version_folder_path` (required): The local path to the first version folder.
    - `--next_version_folder_path` (required): The local path to the second version folder.
    - `--output_filename` (optional): The name of the output file (default: `output.txt`).

    Replace <version>, <next_version>, <version_folder_path>, <next_version_folder_path>, and <output_filename> with the appropriate values for your case.

## Example Usage

Suppose you have two directories: `/v1` and `/v2`. Each of these directories has three `.json` files:

```
/v1
  ├── file_1_v1.json
  ├── file_2_v1.json
  └── file_3_v1.json

/v2
  ├── file_1_v2.json
  ├── file_2_v2.json
  └── file_3_v2.json
```

After running the script, the output file captures the key differences between the `v1` and `v2` versions of each of the three `.json` files, clearly highlighting the changes made between versions.

```
file_1_v1.json | file_1_v2.json

  {
+   "property": "new_value"
  }

---

file_2_v1.json | file_2_v2.json

  {
+   "property": "updated_value",
-   "property2": "old_value",
  }

---

file_3_v1.json | file_3_v2.json

  {
+   "property1": "new_value1",
-   "property2": "value2"
+   "property3": "new_value2"
  }
```

- For `file_1_v1.json`, a new property has been added in version `v2`.
- In `file_2_v1.json`, an existing property has been updated from "old_value" to "updated_value", and another property has been removed.
- For `file_3_v1.json`, one property has been updated, one has been removed, and a new one has been added in version `v2`.

## Contributions

If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/new-feature`).
3. Make your changes and commit them following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format (`git commit -m 'feat: add new feature'` or `fix: correct a bug`).
4. Push your branch to the remote repository (`git push origin feature/new-feature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
