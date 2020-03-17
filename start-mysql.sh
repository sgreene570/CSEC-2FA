docker run -p 3306:3306 --name mysql-container -e MYSQL_DATABASE=2fa -e MYSQL_USER=demo -e MYSQL_PASSWORD=password -e MYSQL_ROOT_PASSWORD=root -d mysql:latest
