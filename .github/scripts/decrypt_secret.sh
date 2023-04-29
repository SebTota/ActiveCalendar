#!/bin/sh
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" --output .env .env.gpg
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" --output backend/client_secret.json backend/client_secret.json.gpg