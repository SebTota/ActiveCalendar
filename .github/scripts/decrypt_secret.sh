 #!/bin/sh
    
# Decrypt the file
mkdir $GITHUB_WORKSPACE/secrets
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $GITHUB_WORKSPACE/strava_calendar_summary_web_service/config.py strava_calendar_summary_web_service/config.py.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $GITHUB_WORKSPACE/strava_calendar_summary_web_service/client_secret.json strava_calendar_summary_web_service/client_secret.json.gpg