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
URL=${WEBHOOK_URL}

# Title
HEAD=${HEAD:-"[TITLE]\n"}

# Get msg with syntax highlight
MESSAGE='```'`cat ${MSGFILE}`'```'

# Covert everything in the json format
payload="payload={
    \"text\": \"${HEAD}${MESSAGE}\"
}"

# Send
curl -s -S -X POST --data-urlencode "${payload}" ${URL} > /dev/null
