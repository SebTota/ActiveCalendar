 #!/bin/sh
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output .github/scripts/secrets.sh .github/scripts/secrets.sh.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output key.pem key.pem.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output cert.pem cert.pem.gpg