# serigy

Software de Criação de Configuração para Fortigate FOS 7.2.X

## Instalação

### apache

```bash
sudo apt update
sudo apt install -y apache2
sudo a2enmod cgid

# Copie os arquivos
cp cgi-bin/* /usr/lib/cgi-bin/

# modifique o /usr/lib/cgi-bin/login.cgi
# de
# AUTHENTICATED=$(echo "SELECT IF(password = PASSWORD('$PASSWORD'), 'authenticated', 'denied') FROM users WHERE username = '$USERNAME';" | mysql -h db -u webapp_user -pwebapp_password webapp -s -N)
# para
# AUTHENTICATED=$(echo "SELECT IF(password = PASSWORD('$PASSWORD'), 'authenticated', 'denied') FROM users WHERE username = '$USERNAME';" | mysql -u webapp_user -pwebapp_password webapp -s -N)

cp -r html/ /var/www/html/

```

### mariadb

```bash
sudo apt install -y mariadb-server

# rode o script
mariadb-secure-installation
# ou
mysql-secure-installation
# para definir a senha de root

# crie database webapp e usuario webapp_user
mysql -uroot -p
MariaDB [(none)]> CREATE DATABASE webapp;
MariaDB [(none)]> GRANT ALL PRIVILEGES ON webapp.* to 'webapp_user'@'localhost' IDENTIFIED BY 'webapp_password';
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> \q

# importe o docker\images\db\webapp.sql

mysql -uroot -p webapp < docker\images\db\webapp.sql

# Esse .sql já tem um usuário criado:
# usuário: serigy
# senha: cabrunco

# caso queira inserir outro usuário
mysql -uroot -p
MariaDB [(none)]> use webapp;
MariaDB [(none)]> INSERT INTO users (username, password) VALUES ('NOME_DO_SEU_USUARIO', PASSWORD('SENHA_DO_SEU_USUARIO'));

```

## Docker

Usando via docker

```bash
cd docker
# iniciando os containers
docker-compose docker-compose.yml up -d

# parando os containers
docker-compose docker-compose.yml down

# miscs
# para forçar o rebuild da imagem
docker-compose docker-compose.yml up --build -d
```

Obs.: Na primeira vez que for executado o **compose up**, será gerado as imagens do webserver e do banco de dados. A imagem do banco de dados vai subir e criar a base webapp automaticamente.

