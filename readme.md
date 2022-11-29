# Make Bot from BotFather

refer to [How Do I Create a Bot?](https://core.telegram.org/bots#how-do-i-create-a-bot)

save token to new text file. (It will be used later...)

# Create deta micro

> deta new --python <YOUR_DETA_MICRO_NAME>

# Download & Extract code to created folder

[Download ZIP](https://github.com/suriing/telegram-bot-template-on-deta/archive/refs/heads/main.zip)

# Modify .env file

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

### deta.sh limitation

- deta micro has **512 MB of RAM** for each execution.
- deta micro has **Read-only** file system. Only **/tmp** can be written to. It has a **512 MB** storage limit.
- deta micro doesn't have SSH access.
- deta micros do not support connecting to MongoDB at the moment. Recommend using Deta Base instead.
- deta micros will doesn't work well with RDMBS like PostgreSQL and MySQL unless you use a pool manager.
- deta micros only support read-only SQLite, which you could deploy with your code.
- The total upload size of your source code and assets is limited to **250 MB**. Dependencies (pip, npm, etc) also can't exceed a combined size of 250mb.