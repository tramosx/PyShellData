#!/bin/bash

# Verifica se o arquivo foi informado
if [ -z "$1" ]; then
  echo "Usage: $0 <input_file> [-desc]"
  exit 1
fi

INPUT_FILE=$1
DESC_OPTION=$2

# Verifica se o arquivo existe
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File '$INPUT_FILE' not found."
  exit 1
fi

if [ "$DESC_OPTION" == "-desc" ]; then
  # Ordenar em ordem decrescente pelo campo de e-mail
  awk '{ print $0 }' "$INPUT_FILE" | sort -r -k1,1
else
  # Ordenar em ordem alfabética pelo campo de e-mail
  awk '{ print $0 }' "$INPUT_FILE" | sort -k1,1
fi
