#!/bin/bash

# This script builds the Docker image and runs the Docker container with the specified parameters.

# Default output path.
OUTPUT_PATH="output"

usage() {
    # Display usage information for the script and exit.
    echo "$0 --version <version> --next_version <next_version> --version_folder_path <version_folder_path> --next_version_folder_path <next_version_folder_path> [--output_filename <output_filename>]"
    echo
    echo "  --version                        The current version to compare"
    echo "  --next_version                   The next version to compare"
    echo "  --version_folder_path            The local path to the first version folder"
    echo "  --next_version_folder_path       The local path to the second version folder"
    echo "  --output_filename                The name of the output file (default: output.txt)"
    exit 1
}

parse_arguments() {
    # Processe command-line arguments, assign them to variables,
    # and checks if the required arguments are provided.
    #
    # Exit the script if required arguments are missing.

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --version) VERSION="$2"; shift ;;
            --next_version) NEXT_VERSION="$2"; shift ;;
            --version_folder_path) VERSION_FOLDER_PATH="$2"; shift ;;
            --next_version_folder_path) NEXT_VERSION_FOLDER_PATH="$2"; shift ;;
            --output_filename) OUTPUT_FILENAME="$2"; shift ;;
            *) usage ;;
        esac
        shift
    done

    if [ -z "$VERSION" ] || [ -z "$NEXT_VERSION" ] || [ -z "$VERSION_FOLDER_PATH" ] || [ -z "$NEXT_VERSION_FOLDER_PATH" ]; then
        usage
    fi
}

build_docker_image() {
    # Execute the `docker build` command to create a Docker image tagged as `json-diff-checker`.

    echo "Building the Docker image..."
    
    docker build -t json-diff-checker .

    if [ "$?" -ne 0 ]; then
        echo "ERROR - Failed to build the Docker image"
        exit 1
    fi
}

run_docker_container() {
    # Run the Docker container with the specified parameters.
    #
    # This function constructs the `docker run` command with mounted volumes and
    # optional output filename. It then executes the command to run the container.
    #
    # The output file name is appended to the command if specified by the user.

    echo "Running the Docker container..."

    local docker_cmd="docker run --rm \
        -v \"$(pwd)/$VERSION_FOLDER_PATH:/app/$VERSION_FOLDER_PATH\" \
        -v \"$(pwd)/$NEXT_VERSION_FOLDER_PATH:/app/$NEXT_VERSION_FOLDER_PATH\" \
        -v \"$(pwd)/$OUTPUT_PATH:/app/$OUTPUT_PATH\" \
        json-diff-checker \
        --version \"$VERSION\" \
        --next_version \"$NEXT_VERSION\" \
        --version_folder_path \"$VERSION_FOLDER_PATH\""

    if [ -n "$OUTPUT_FILENAME" ]; then
        docker_cmd="$docker_cmd --output_filename \"$OUTPUT_FILENAME\""
    fi

    eval "$docker_cmd"
}

main() {
    # Main function to execute the script.

    parse_arguments "$@"
    build_docker_image
    run_docker_container
}

main "$@"
