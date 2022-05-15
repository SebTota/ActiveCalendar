 #!/bin/sh
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output .github/scripts/secrets.sh .github/scripts/secrets.sh.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output private_key.pem private_key.pem.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output cert_key.pem cert_key.pem.gpg