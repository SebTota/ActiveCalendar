 #!/bin/sh
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" --output nginx/bundle.pem nginx/bundle.pem.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" --output client_secret.json client_secret.json.gpg
