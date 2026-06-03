#!/bin/bash

# Exit on error
set -e

# Get directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Configuration
DEFAULT_OUTPUT_DIR="$PROJECT_ROOT/data"
URL_FILE="$PROJECT_ROOT/data/url.txt"

# Allow overriding output directory
OUTPUT_DIR="${1:-$DEFAULT_OUTPUT_DIR}"

# Check if URL file exists
if [ ! -f "$URL_FILE" ]; then
    echo "Error: URL file not found at $URL_FILE" >&2
    exit 1
fi

# Read and trim the URL
URL=$(cat "$URL_FILE" | tr -d '\r\n[:space:]')

if [ -z "$URL" ]; then
    echo "Error: URL file is empty or contains only whitespace." >&2
    exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Define temporary zip file path
ZIP_PATH="$OUTPUT_DIR/temp_data.zip"

echo "Reading URL from: $URL_FILE"
echo "Target URL: $URL"
echo "Downloading to: $ZIP_PATH"

# Download with curl
# -L: follow redirects
# -f: fail silently on server errors
if ! curl -L -f -o "$ZIP_PATH" "$URL"; then
    echo "Error: Failed to download the file from $URL" >&2
    exit 1
fi

echo "Download complete. Unzipping to: $OUTPUT_DIR"

# Unzip the file
# -o: overwrite existing files without prompting
# -d: specify target directory
if ! unzip -o "$ZIP_PATH" -d "$OUTPUT_DIR"; then
    echo "Error: Failed to unzip $ZIP_PATH" >&2
    # Clean up the zip file even on failure to avoid leaving junk
    rm -f "$ZIP_PATH"
    exit 1
fi

echo "Unzip complete. Deleting temporary zip file..."
rm -f "$ZIP_PATH"

echo "Data updated successfully in: $OUTPUT_DIR"
