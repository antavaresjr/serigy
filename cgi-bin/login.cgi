#!/bin/bash

# Define o conteúdo da resposta HTTP
echo "Content-type: application/json"
echo ""

# Lê a entrada do formulário
read -n "$CONTENT_LENGTH" INPUT_DATA

# Extrai as credenciais do formulário
USERNAME=$(echo "$INPUT_DATA" | grep -oP 'username=\K[^&]+')
PASSWORD=$(echo "$INPUT_DATA" | grep -oP 'password=\K[^&]+')

# Decodifica URL
USERNAME=$(echo -e "${USERNAME//%/\\x}")
PASSWORD=$(echo -e "${PASSWORD//%/\\x}")

# Conectar ao banco de dados e verificar as credenciais
AUTHENTICATED=$(echo "SELECT IF(password = PASSWORD('$PASSWORD'), 'authenticated', 'denied') FROM users WHERE username = '$USERNAME';" | mysql -h db -u webapp_user -pwebapp_password webapp -s -N)

if [ "$AUTHENTICATED" == "authenticated" ]; then
    # Login bem-sucedido
    echo "{\"success\": true}"
else
    # Login falhou
    echo "{\"success\": false, \"error\": \"Usuário ou senha incorretos. Por favor, tente novamente.\"}"
fi

