import os
import subprocess
import argparse


BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_files_in_folder(folder):
    """
    Get a list of files in a folder.

    Args:
        folder (str): The folder path.

    Returns:
        list: A list of files in the folder.
    """
    files = [
        file
        for file in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, file))
    ]
    return files


def run_json_diff(file1, file2):
    """
    Run json-diff on two JSON files.

    Args:
        file1 (str): The path to the first JSON file.
        file2 (str): The path to the second JSON file.

    Returns:
        str: The differences between the two JSON files.
    """
    result = subprocess.run(["json-diff", file1, file2], capture_output=True, text=True)
    return result.stdout


def output_to_file(output, filename):
    """
    Write the output to a file.

    Args:
        output (str): The output to write to the file.
        filename (str): The name of the file.
    """
    str_output = "".join(output)

    with open(f"{filename}.txt", "w") as f:
        f.write(str_output)


def process(version, next_version, folder_name, output_filename):
    """
    Compare the JSON files in the version folder with the JSON files in the next version folder and output the differences to a file.

    Args:
        version (str): The current version to compare.
        next_version (str): The next version to compare.
        folder_name (str): The base name of the folder for versions.
        output_filename (str): The name of the output file.
    """
    version_folder_name = folder_name
    next_version_folder_name = folder_name.replace(version, next_version)

    version_folder_path = os.path.join(BASE_DIRECTORY, version_folder_name)
    next_version_folder_path = os.path.join(BASE_DIRECTORY, next_version_folder_name)

    if not os.path.isdir(version_folder_path):
        print(
            f"Error: The folder '{version_folder_path}' does not exist or is not a directory."
        )
        return

    if not os.path.isdir(next_version_folder_path):
        print(
            f"Error: The folder '{version_folder_path}' does not exist or is not a directory."
        )
        return

    version_files = get_files_in_folder(version_folder_path)

    if not version_files:
        print("Files not found.")
        return

    output_lines = []

    for version_filename in version_files:
        next_version_filename = version_filename.replace(version, next_version)

        version_file_path = os.path.join(version_folder_path, version_filename)
        next_version_file_path = os.path.join(
            next_version_folder_path, next_version_filename
        )

        if not (
            os.path.exists(version_file_path) or os.path.exists(next_version_file_path)
        ):
            output_lines.append(
                f"{version_filename} | {version_filename}\n\nFiles not found.\n---\n\n"
            )
            continue

        output = run_json_diff(version_file_path, next_version_file_path)
        output_lines.append(
            f"{version_filename} | {next_version_filename}\n\n{output}\n---\n\n"
        )

    output_to_file(output_lines, output_filename)

    print(f"Output saved to {output_filename}.")


def start():
    """
    Parse the command line arguments and run the script.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Compare the JSON files in the version folder with the JSON files in the next version folder and output the differences to a file.\n\n"
            "The folder names should be named equally except for the version number.\n"
            "The names of the files within these folders be named equally except for the version number."
        )
    )

    parser.add_argument(
        "--version",
        help="The current version to compare.",
    )
    parser.add_argument(
        "--next_version",
        help="The next version to compare.",
    )
    parser.add_argument(
        "--first_version_folder_name",
        help="The name of the folder for the first version. No worries! For generating the next version folder name, the version number will be automatically replaced with the next version number.",
    )
    parser.add_argument(
        "--output_filename",
        default="output",
        help="The name of the output file (default: output.txt).",
    )

    arguments = parser.parse_args()

    if any(value is None for value in vars(arguments).values()):
        parser.print_help()
        return

    process(
        arguments.version,
        arguments.next_version,
        arguments.first_version_folder_name,
        arguments.output_filename,
    )


def main():
    start()


if __name__ == "__main__":
    main()
