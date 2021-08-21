# Slack Notifier
Sends notification to slack when a process is done.

## Usage
```
COMMAND | ./slack_webhook.sh
```
or you can add this to the end of your shell script like below
```
if [ $? -ne 0 ]; then
  echo "Your job returned non-zero status." | slack_webhook.sh
else
  echo "Your job was successfully done." | slack_webhook.sh
fi
```
## Reference
http://vdeep.net/shellscript-slack
