import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def get_schema_names(files, prefix):
    return [
        file_name[len(prefix) :].replace("_schema.json", "")
        for file_name in files
        if file_name.startswith(prefix)
    ]


def find_common_schemas(first_directory, second_directory, first_prefix, second_prefix):
    if not first_directory.exists():
        raise FileNotFoundError(f"Directory '{first_directory}' not found.")
    if not second_directory.exists():
        raise FileNotFoundError(f"Directory '{second_directory}' not found.")

    first_directory_files = {
        file.name for file in first_directory.iterdir() if file.is_file()
    }
    second_directory_files = {
        file.name for file in second_directory.iterdir() if file.is_file()
    }

    first_directory_schema_names = set(
        get_schema_names(first_directory_files, first_prefix)
    )
    second_directory_schema_names = set(
        get_schema_names(second_directory_files, second_prefix)
    )

    common_schemas = first_directory_schema_names & second_directory_schema_names
    first_directory_unique_schemas = (
        first_directory_schema_names - second_directory_schema_names
    )
    second_directory_unique_schemas = (
        second_directory_schema_names - first_directory_schema_names
    )

    first_directory_file_mapping = {
        get_schema_names([file.name], first_prefix)[0]: file
        for file in first_directory.iterdir()
        if file.is_file() and file.name.startswith(first_prefix)
    }

    second_directory_file_mapping = {
        get_schema_names([file.name], second_prefix)[0]: file
        for file in second_directory.iterdir()
        if file.is_file() and file.name.startswith(second_prefix)
    }

    return (
        common_schemas,
        first_directory_unique_schemas,
        second_directory_unique_schemas,
        first_directory_file_mapping,
        second_directory_file_mapping,
    )


def compare(first_file, second_file):
    try:
        result = subprocess.run(
            ["json-diff", str(first_file), str(second_file)],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
            return error.stdout.strip()
        return error.stderr.strip()
    except FileNotFoundError:
        raise SystemExit(
            "'json-diff' tool not found. Please install it using 'npm install -g json-diff'."
        )


def write_to_file(file_path, content):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compare JSON schemas between two directories"
    )
    parser.add_argument(
        "--first_directory",
        required=True,
        help="Path to first directory containing schemas",
    )
    parser.add_argument(
        "--second_directory",
        required=True,
        help="Path to second directory containing schemas",
    )
    parser.add_argument(
        "--first_prefix",
        required=True,
        help="File name prefix for schemas in first directory",
    )
    parser.add_argument(
        "--second_prefix",
        required=True,
        help="File name prefix for schemas in second directory",
    )
    parser.add_argument(
        "--output_file",
        default="schema_comparison_results.txt",
        help="Path for output results file",
    )

    arguments = parser.parse_args()

    output_file_path = Path(arguments.output_file)
    if output_file_path.exists():
        output_file_path.unlink()

    try:
        first_directory = Path(arguments.first_directory)
        second_directory = Path(arguments.second_directory)

        write_to_file(
            output_file_path,
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        )
        write_to_file(
            output_file_path,
            f"First directory - /{first_directory} (prefix '{arguments.first_prefix}')",
        )
        write_to_file(
            output_file_path,
            f"Second directory - /{second_directory} (prefix '{arguments.second_prefix}')\n",
        )

        (
            common_schemas,
            first_directory_unique_schemas,
            second_directory_unique_schemas,
            first_directory_file_mapping,
            second_directory_file_mapping,
        ) = find_common_schemas(
            first_directory,
            second_directory,
            arguments.first_prefix,
            arguments.second_prefix,
        )

        if first_directory_unique_schemas:
            message = f"Found the next {len(first_directory_unique_schemas)} unique schemas in /{first_directory}."
            write_to_file(output_file_path, message)
            schemas_list = "\n".join(
                [f"  · {schema}" for schema in sorted(first_directory_unique_schemas)]
            )
            write_to_file(output_file_path, schemas_list + "\n")

        if second_directory_unique_schemas:
            message = f"Found the next {len(second_directory_unique_schemas)} unique schemas in /{second_directory}."
            write_to_file(output_file_path, message)
            schemas_list = "\n".join(
                [f"  · {schema}" for schema in sorted(second_directory_unique_schemas)]
            )
            write_to_file(output_file_path, schemas_list + "\n")

        if not common_schemas:
            message = "No matching schemas found between the directories."
            write_to_file(output_file_path, message)
            print(message)
            return

        common_schemas = sorted(common_schemas)

        message = f"Found the next {len(common_schemas)} matching schemas."
        write_to_file(output_file_path, message)
        schemas_list = "\n".join([f"  · {schema}" for schema in common_schemas])
        write_to_file(output_file_path, schemas_list)

        for index, schema_name in enumerate(common_schemas):
            first_file_path = first_directory_file_mapping[schema_name]
            second_file_path = second_directory_file_mapping[schema_name]

            header = f"💠 Comparing schema '{schema_name}'..."
            files_information = f"    First directory file - {os.path.basename(first_file_path)}\n    Second directory file - {os.path.basename(second_file_path)}"

            write_to_file(output_file_path, f"\n{header}\n{files_information}")

            comparison_result = compare(first_file_path, second_file_path)

            if not comparison_result:
                write_to_file(output_file_path, "  Schemas are identical.")
            else:
                write_to_file(output_file_path, comparison_result)

            if index < len(common_schemas) - 1:
                write_to_file(output_file_path, f"\n{'-' * 75}")

        print(f"\nResults saved to '{output_file_path}'.")
    except Exception as error:
        error_message = str(error)
        print(error_message)
        write_to_file(output_file_path, error_message)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nComparison interrupted by user.")
