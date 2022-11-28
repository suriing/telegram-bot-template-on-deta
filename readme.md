# Make Bot from BotFather

refer to [How Do I Create a Bot?](https://core.telegram.org/bots#how-do-i-create-a-bot)

save token to new text file. (It will be used later...)

# Create deta micro

> deta new --python <YOUR_DETA_MICRO_NAME>

# Download code to created folder

# Make .env file to created folder

```txt
TOKEN=<YOUR_BOT_TOKEN>
```

# Run bot & update .env file

> deta deploy
> deta update -e .env

# Connect webhook to bot

```sh
curl --header 'Content-Type: application/json' --data '{"url": "https://<YOUR_DETA_ENDPOINT>.deta.dev/webhook"}' 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook'
```