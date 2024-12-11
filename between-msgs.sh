#!/bin/bash

# Verifica se o arquivo e os parâmetros foram informados
if [ $# -lt 3 ]; then
  echo "Usage: $0 <input_file> <min_msgs> <max_msgs>"
  exit 1
fi

INPUT_FILE=$1
MIN_MSGS=$2
MAX_MSGS=$3

# Verifica se o arquivo existe
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File '$INPUT_FILE' not found."
  exit 1
fi

# Verifica se os valores mínimo e máximo são números
if ! [[ "$MIN_MSGS" =~ ^[0-9]+$ ]] || ! [[ "$MAX_MSGS" =~ ^[0-9]+$ ]]; then
  echo "Error: Both <min_msgs> and <max_msgs> must be numeric values."
  exit 1
fi

# Filtra os usuários dentro da faixa de mensagens especificada
awk -v min="$MIN_MSGS" -v max="$MAX_MSGS" '{
  msgs = $3 + 0; # Converte para número removendo zeros à esquerda automaticamente
  if (msgs >= min && msgs <= max) {
    print $0;
  }
}' "$INPUT_FILE"
