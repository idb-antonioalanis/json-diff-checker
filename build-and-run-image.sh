#!/bin/bash

# This script builds the Docker image and runs the Docker container with the specified parameters.

usage() {
    # Display usage information for the script.
    echo "$0 --first_directory <first_directory> --second_directory <second_directory> --first_prefix <first_prefix> --second_prefix <second_prefix> [--output_file <output_file>]"
    echo
    echo "  --first_directory       Path to first directory containing schemas"
    echo "  --second_directory      Path to second directory containing schemas"
    echo "  --first_prefix          File name prefix for schemas in first directory"
    echo "  --second_prefix         File name prefix for schemas in second directory"
    echo "  --output_file           Path for output results file (default: schema_comparison_results.txt)"
    exit 1
}

parse_arguments() {
    # Process command-line arguments, assign them to variables,
    # and checks if the required arguments are provided.
    #
    # Exit the script if required arguments are missing.

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --first_directory) FIRST_DIRECTORY="$2"; shift ;;
            --second_directory) SECOND_DIRECTORY="$2"; shift ;;
            --first_prefix) FIRST_PREFIX="$2"; shift ;;
            --second_prefix) SECOND_PREFIX="$2"; shift ;;
            --output_file) OUTPUT_FILE="$2"; shift ;;
            *) usage ;;
        esac
        shift
    done

    if [ -z "$FIRST_DIRECTORY" ] || [ -z "$SECOND_DIRECTORY" ] || [ -z "$FIRST_PREFIX" ] || [ -z "$SECOND_PREFIX" ]; then
        usage
    fi

    OUTPUT_FILE=${OUTPUT_FILE:-"schema_comparison_results.txt"}
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
    # This function constructs the `docker run` command with mounted volumes
    # The output file will be created in the current directory

    echo "Running the Docker container..."

    local docker_cmd="docker run --rm \
        -v \"$(pwd)/$FIRST_DIRECTORY:/app/$FIRST_DIRECTORY\" \
        -v \"$(pwd)/$SECOND_DIRECTORY:/app/$SECOND_DIRECTORY\" \
        -v \"$(pwd):/app/output\" \
        json-diff-checker \
        --first_directory \"$FIRST_DIRECTORY\" \
        --second_directory \"$SECOND_DIRECTORY\" \
        --first_prefix \"$FIRST_PREFIX\" \
        --second_prefix \"$SECOND_PREFIX\" \
        --output_file \"/app/output/$OUTPUT_FILE\""

    eval "$docker_cmd"
}

main() {
    # Main function to execute the script.

    parse_arguments "$@"
    build_docker_image
    run_docker_container
}

main "$@"