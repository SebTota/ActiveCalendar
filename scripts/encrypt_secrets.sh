#!/bin/sh

if [ "$1" = "decrypt" ] || [ "$1" = "--decrypt" ] || [ "$1" = "d" ] || [ "$1" = "--d" ]; then
  echo "decrypting secret files"
  gpg --quiet --batch --yes --decrypt --passphrase="$2" --output .env .env.gpg
  gpg --quiet --batch --yes --decrypt --passphrase="$2" --output backend/client_secret.json backend/client_secret.json.gpg
else
  echo "encrypting secret files"
  gpg --quiet -c --armor --cipher-algo AES256 --no-symkey-cache --output .env.gpg .env
  gpg --quiet -c --armor --cipher-algo AES256 --no-symkey-cache --output backend/client_secret.json.gpg backend/client_secret.json
fi


