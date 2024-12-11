#!/bin/bash

# Verifica se o arquivo foi informado
if [ -z "$1" ]; then
  echo "Usage: $0 <input_file> [-min]"
  exit 1
fi

INPUT_FILE=$1
MIN_OPTION=$2

# Verifica se o arquivo existe
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File '$INPUT_FILE' not found."
  exit 1
fi

if [ "$MIN_OPTION" == "-min" ]; then
  # Encontrar o menor size
  awk '{
    size = $NF;
    gsub("size", "", size);
    if (min == "" || size + 0 < min) {
      min = size + 0;
      min_line = $0;
    }
  } END { print min_line }' "$INPUT_FILE"
else
  # Encontrar o maior size
  awk '{
    size = $NF;
    gsub("size", "", size);
    if (max == "" || size + 0 > max) {
      max = size + 0;
      max_line = $0;
    }
  } END { print max_line }' "$INPUT_FILE"
fi
