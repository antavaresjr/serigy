#!/bin/bash

# Script para leitura de csv de dois campos com hostname;mac_addr
# onde o awk delimita os campos, OFS separa os campos para $1, $2 e $3
# o printf substitui no campo de configuração e a saída $1 é redirecionada
# para o novo arquivo $2

# Verifica se o arquivo CSV foi fornecido como argumento de linha de comando
# onde se "$#" (args) -ne (diferente de) 2, imprime echo orientação
if [ $# -ne 2 ]; then
  echo "Uso: $0 arquivo_csv arquivo_saida"
  exit 1
fi

# Lê o arquivo CSV e gera o script awk dinamicamente
# onde o delimitador é ";" e o -v OFS=' ' separa $1, $2 e $3
# e o printf "\%s\n", $1 ou $2, substitui o valor da linha
# o $1 fora do {} recebe o printf inteiro e envia para o segundo argumento
# que é o arquivo final no uso "./script.sh arq_csv arq_config"
awk -F';' -v OFS=' ' ' {
  printf "config firewall address\n"
  printf "    edit \"%s\"\n", $1
  printf "        set subnet %s\n", $2
  printf "    next\n"
  printf "end\n"
}' "$1" > "$2"

