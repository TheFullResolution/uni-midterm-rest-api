#!/bin/bash

# Ensure dasel is installed
if ! command -v dasel &> /dev/null
then
    echo "Dasel is not installed. Install it using 'brew install dasel' and try again."
    exit 1
fi

# Directory containing JSON files
INPUT_DIR="./jsonSeed"
OUTPUT_DIR="./csvSeed"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through each JSON file in the input directory
for file in "$INPUT_DIR"/*.json; do
    if [ -f "$file" ]; then
        # Extract the base name (filename without extension)
        base_name=$(basename "$file" .json)

        # Convert JSON to CSV using dasel
        dasel -r json -w csv < "$file" > "$OUTPUT_DIR/$base_name.csv"

        echo "Converted $file to $OUTPUT_DIR/$base_name.csv"
    else
        echo "No JSON files found in $INPUT_DIR"
    fi

done

# Completion message
echo "Conversion completed. CSV files are in $OUTPUT_DIR."
