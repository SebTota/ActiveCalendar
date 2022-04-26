 #!/bin/sh
    
mkdir $GITHUB_WORKSPACE/secrets

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $GITHUB_WORKSPACE/.github/scripts/secrets.sh $GITHUB_WORKSPACE/.github/scripts/secrets.sh.gpg

. ./$GITHUB_WORKSPACE/.github/scripts/secrets.sh
