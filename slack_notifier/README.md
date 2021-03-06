# Slack Notifier
Sends notification to slack when a process is done.

## Preparation

Go to https://api.slack.com/apps and *Create New App*. Then, go to *Incoming Webhooks* in settings and turn on *Activate Incoming Webhooks*. Finally, generate **Webhook URL** from *Add New Webhook to Workspace*.

To use the webhook URL you just generated, you can either 

1. Set an enviroment variable (in, for example, .bash_profile or .zprofile)

   ```
   export WEBHOOK_URL='Webhook URL you generated'
   ```

2. Replace `URL=${WEBHOOK_URL}` in the code with `URL='Webhook URL you generated' ` 

## Usage

* Just notifies you when your job is finished

   ```
   COMMAND | ./slack_webhook.sh
   ```

* Gives you more info on your job when it is finished

   ```
   ./run_command.sh 'COMMAND'
   ```

* Mannually integrate the notification script to your script like below

   ```
   if [ $? -ne 0 ]; then
     echo "Your job returned non-zero status." | slack_webhook.sh
   else
     echo "Your job was successfully done." | slack_webhook.sh
   fi
   ```
