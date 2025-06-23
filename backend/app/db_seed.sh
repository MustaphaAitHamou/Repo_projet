#!/bin/sh
set -e

# Attendre que le serveur MySQL soit prêt
until mysqladmin ping -h "$MYSQL_HOST" --silent; do
  echo "⏳ Waiting for MySQL to be available…"
  sleep 2
done

# Créer la table user si besoin
mysql --user="$MYSQL_ROOT_USER" --password="$MYSQL_ROOT_PASSWORD" --database="$MYSQL_DATABASE" <<-EOSQL
CREATE TABLE IF NOT EXISTS user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  hashed_pwd VARCHAR(128) NOT NULL,
  is_admin BOOL DEFAULT FALSE
);
EOSQL

# Seed de l’administrateur
mysql --user="$MYSQL_ROOT_USER" --password="$MYSQL_ROOT_PASSWORD" --database="$MYSQL_DATABASE" <<-EOSQL
INSERT INTO user (email, hashed_pwd, is_admin)
VALUES (
  '$ADMIN_EMAIL',
  SHA2('$ADMIN_PASSWORD', 256),
  TRUE
)
ON DUPLICATE KEY UPDATE email = email;
EOSQL
