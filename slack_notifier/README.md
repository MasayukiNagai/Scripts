# Slack Notifier
Sends notification to slack when a process is done.

## Usage

1. Just notifies you when your job is finished

   ```
   COMMAND | ./slack_webhook.sh
   ```

2. Gives you more info on your job when it is finished

   ```
   ./run_command.sh 'COMMAND'
   ```

3. Mannually integrate the notification script to your script like below

   ```
   if [ $? -ne 0 ]; then
     echo "Your job returned non-zero status." | slack_webhook.sh
   else
     echo "Your job was successfully done." | slack_webhook.sh
   fi
   ```
