#!/bin/bash

#======== verificação de autenticação ==============

# Verifica o cookie de sessão
#COOKIE=$(echo "$HTTP_COOKIE" | grep -o 'session=authenticated')

#if [ "$COOKIE" != "session=authenticated" ]; then
    # Sessão inválida, redirecionar para login
#    echo "Location: /login.html"
#    echo "Content-type: text/html"
#    echo ""
#    exit 0
#fi

#===================================================

# Define o caminho para o arquivo temporário
TEMP_FILE=$(mktemp)

# Lê o conteúdo enviado pelo formulário e salva no arquivo temporário
CONTENT_LENGTH="${CONTENT_LENGTH:-0}"
if [ "$CONTENT_LENGTH" -gt 0 ]; then
    # Escrevendo diretamente no arquivo temporário
    awk 'NR > 4 && !/--WebKitFormBoundary/ {print}' > "$TEMP_FILE"
fi

# Define o diretório de upload
UPLOAD_DIR="/var/www/html/uploads/"

# Verifica se o diretório de uploads existe, senão cria
mkdir -p "$UPLOAD_DIR"

# Gera o novo arquivo TXT manipulando o arquivo temporário
awk -F';' '{
    printf "config firewall ippool\n"
    printf "    edit \"%s\"\n", $1
    printf "        set startip %s\n", $2
    printf "        set endip %s\n", $2
    for (i=3; i<=NF; i++) {
        printf "        set field%d %s\n", i, $i
    }
    printf "    next\n"
    printf "end\n"
}' "$TEMP_FILE" > "$UPLOAD_DIR/pool_file.txt"

# Ajusta as permissões do arquivo
chmod 644 "$UPLOAD_DIR/pool_file.txt"

# Remove o arquivo temporário
rm "$TEMP_FILE"

# Define o conteúdo a ser exibido no <textarea>
TEXTAREA_CONTENT=$(cat "$UPLOAD_DIR/pool_file.txt")

# Redireciona para uma página de confirmação
echo "Content-Type: text/html"
echo ""
echo "<!DOCTYPE html>"
echo "<html lang='en'>"
echo "<head>"
echo "<meta charset='UTF-8'>"
echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
echo "<link href='/bootstrap/bootstrap-5.3.3-dist/css/bootstrap-grid.min.css' rel='stylesheet'>"
echo "<link href='/bootstrap/css/estilo-cgi.css' rel='stylesheet'>"
echo "<title>Upload Concluído</title>"
echo "</head>"
echo "<body>"
echo "<div class='conteudo'>"
echo "<h1>Upload Concluído</h1>"
echo "<p>O arquivo foi enviado com sucesso e está disponível para download abaixo:</p>"
echo "<p><a href='/uploads/pool_file.txt' download='pool_file.txt'>Baixar arquivo</a></p>"
echo "<textarea rows='10' cols='80'>$TEXTAREA_CONTENT</textarea>"
echo "<button class='retornar' onclick=\"window.top.location.href='/menu.html'\">Retornar</button>"
echo "</div>"
echo "</body>"
echo "</html>"

