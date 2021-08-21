#!/bin/bash

set -eu

# Temporarilly store the msg
MSGFILE=$(mktemp -t webhooksXXXX)
# Delete the msg file when completed
trap "rm ${MSGFILE}" 0

# Check if sth is in stdin
if [ -p /dev/stdin ]; then
    cat - | tr '\n' '\\' | sed 's/\\/\\n/g' > ${MSGFILE}
else
    echo "nothing stdin"
    exit 1
fi

# URL of WEBHOOK
URL='WEBHOOK_URL'
# Channel that you want to send the msg to
CHANNEL=${CHANNEL:-'#CHANNEL_NAME'}
# Name of your bot
BOTNAME=${BOTNAME:-'BOT_NAME'}
# Emoji
EMOJI=${EMOJI:-':new_moon_with_face:'}
# Title
HEAD=${HEAD:-"[TITLE]\n"}

# Get msg with syntax highlight
MESSAGE='```'`cat ${MSGFILE}`'```'

# Covert everything in the json format
payload="payload={
    \"channel\": \"${CHANNEL}\",
    \"username\": \"${BOTNAME}\",
    \"icon_emoji\": \"${EMOJI}\",
    \"text\": \"${HEAD}${MESSAGE}\"
}"

# Send
curl -s -S -X POST --data-urlencode "${payload}" ${URL} > /dev/null
