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

# Função para obter os valores de Netmask, HostMin e HostMax
get_ip_info() {
    local ip_info
    ip_info=$(ipcalc "$1" | grep -E 'Netmask:|HostMin:|HostMax:')
    mask=$(echo "$ip_info" | awk '/Netmask:/ {gsub(/[[:blank:]]+/," ",$2); print $2}')
    ip_min=$(echo "$ip_info" | awk '/HostMin:/ {gsub(/[[:blank:]]+/," ",$2); print $2}')
    ip_max=$(echo "$ip_info" | awk '/HostMax:/ {gsub(/[[:blank:]]+/," ",$2); print $2}')
}

# Trata o endereço IP para remover o CIDR
parse_ip() {
    ip=$1
    parsed_ip=$(echo "$ip" | cut -d '/' -f1)
}

# Arquivo CSV de entrada
input_file="$TEMP_FILE"
# Arquivo de saída
output_file="$UPLOAD_DIR/interface_file.txt"

# Loop sobre as linhas do arquivo CSV
while IFS=';' read -r field1 field2 field3 field4 field5 field6; do
    # Tratar o campo IP removendo o CIDR
    parse_ip "$field2"
    # Obter informações do IP
    get_ip_info "$field2"

    # Saída formatada para cada linha
    printf "config system interface\n"
    printf "    edit \"%s\"\n" "$field1"
    printf "        set vdom \"root\"\n"
    printf "        set ip %s\n" "$parsed_ip $mask"
    printf "        set allowaccess ping https ssh\n"
    printf "        set type %s\n" "$field3"
    printf "        set device-identification enable\n"
    printf "        set lldp-transmission enable\n"

    # Condição para o tipo VLAN
    if [ "$field3" == "vlan" ]; then
        printf "        set interface \"%s\"\n" "$field4"
        printf "        set vlanid %s\n" "$field5"
    fi
    printf "        set role lan\n"
    printf "    next\n"
    printf "end\n"

    # Condição para o tipo DHCP
    if [ "$field6" == "dhcp" ]; then
        printf "config system dhcp server\n"
        printf "    edit 0\n"
        printf "        set dns-service default\n"
        printf "        set default-gateway %s\n" "$parsed_ip"
        printf "        set netmask %s\n" "$mask"
        printf "        set interface \"%s\"\n" "$field1"
        printf "        config ip-range\n"
        printf "            edit 1\n"
        printf "                set start-ip %s\n" "$ip_min"
        printf "                set end-ip %s\n" "$ip_max"
        printf "            next\n"
        printf "        end\n"
        printf "    next\n"
        printf "end\n"
    fi
done < "$input_file" > "$output_file"


# Ajusta as permissões do arquivo
chmod 644 "$UPLOAD_DIR/interface_file.txt"

# Remove o arquivo temporário
rm "$TEMP_FILE"

# Define o conteúdo a ser exibido no <textarea>
TEXTAREA_CONTENT=$(cat "$UPLOAD_DIR/interface_file.txt")

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
echo "<p><a href='/uploads/interface_file.txt' download='interface_file.txt'>Baixar arquivo</a></p>"
echo "<textarea rows='10' cols='80'>$TEXTAREA_CONTENT</textarea>"
echo "<button class='retornar' onclick=\"window.top.location.href='/menu.html'\">Retornar</button>"
echo "</div>"
echo "</body>"
echo "</html>"


