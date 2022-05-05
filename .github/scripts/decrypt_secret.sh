 #!/bin/sh
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output .github/scripts/secrets.sh .github/scripts/secrets.sh.gpg
