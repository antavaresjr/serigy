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
    printf "config system sdwan\n"
    printf "    set status enable\n"
    printf "    config zone\n"
    printf "        edit \"virtual-wan-link\"\n"
    printf "        next\n"
    printf "    end\n"
    printf "    config members\n"
    if ($1 == "1") {
    printf "        edit 1\n"
    printf "            set interface \"%s\"\n", $2
    printf "            set gateway %s\n", $3
    printf "        next\n"
    } else {
    printf "        edit 1\n"
    printf "            set interface \"%s\"\n", $2
    printf "            set gateway %s\n", $3
    printf "        next\n"
    printf "        edit 2\n"
    printf "            set interface \"%s\"\n", $4
    printf "            set gateway %s\n", $5
    printf "        next\n"
    }
    printf "    config health-check\n"
    printf "        edit \"MONITOR_INTERNET\"\n"
    printf "            set server \"8.8.8.8\" \"1.1.1.1\"\n"
    printf "            set interval 1000\n"
    printf "            set failtime 10\n"
    printf "            set recoverytime 15\n"
    printf "            set update-static-route disable\n"
    if ($1 == "1") {
    printf "            set members 1\n"
    } else {
    printf "            set members 1 2\n"
    }
    printf "            config sla\n"
    printf "                edit 1\n"
    printf "                    set latency-threshold 73\n"
    printf "                    set jitter-threshold 13\n"
    printf "                    set packetloss-threshold 3\n"
    printf "                next\n"
    printf "            end\n"
    printf "        next\n"
    printf "    end\n"
    printf "    config service\n"
    printf "        edit 1\n"
    printf "            set name \"FortiGuard\"\n"
    printf "            set src \"all\"\n"
    printf "            set internet-service enable\n"
    printf "            set internet-service-name \"Fortinet-FortiGuard\" \"Fortinet-FortiGuard.Secure.DNS\" \"Fortinet-DNS\" \"Fortinet-FortiCloud\" \"Fortinet-Other\" \"Fortinet-Web\" \"Fortinet-NTP\"\n"
    printf "            set priority-zone \"virtual-wan-link\"\n"
    printf "        next\n"
    printf "        edit 2\n"
    printf "            set name \"SAIDA_INTERNET_GERAL\"\n"
    printf "            set mode sla\n"
    printf "            set dst \"all\"\n"
    printf "            set src \"all\"\n"
    printf "            config sla\n"
    printf "                edit \"MONITOR_INTERNET\"\n"
    printf "                    set id 1\n"
    printf "                next\n"
    printf "            end\n"
    if ($1 == "1") {
    printf "            set priority-members 1\n"
    } else {
    printf "            set priority-members 1 2\n"
    }
    # Loop para adicionar campos adicionais
    for (i = 6; i <= NF; i++) {
        printf "            set field%d %s\n", i-5, $i
    }
    printf "        next\n"
    printf "    end\n"
    printf "end\n"
}' "$TEMP_FILE" > "$UPLOAD_DIR/sdwan_file.txt"

# Ajusta as permissões do arquivo
chmod 644 "$UPLOAD_DIR/sdwan_file.txt"

# Remove o arquivo temporário
rm "$TEMP_FILE" 

# Define o conteúdo a ser exibido no <textarea>
TEXTAREA_CONTENT=$(cat "$UPLOAD_DIR/sdwan_file.txt")

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
echo "<p><a href='/uploads/sdwan_file.txt' download='sdwan_file.txt'>Baixar arquivo</a></p>"
echo "<textarea rows='10' cols='80'>$TEXTAREA_CONTENT</textarea>"
echo "<button class='retornar' onclick=\"window.top.location.href='/menu.html'\">Retornar</button>"
echo "</div>"
echo "</body>"
echo "</html>"

