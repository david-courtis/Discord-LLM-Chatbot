# cGPT Discord Bot v1.0

A discord bot that uses cGPT-3.5 to generate responses to messages.

## Capabilities:

* Will reply to a message mentioning the bot.
* Will reply to any message that has a "why", "what", "how", "?", "wtf", "idk", "huh".
* Has 2000 characters of memory per channel.
* Will reply every 5000 characters in a channel.
* Uses cGPT-3.5 to generate responses.

### Setup instructions:

* Create a discord bot and add it to your server.
* Create a .env file with the following contents:

```
DISCORD_TOKEN=<your discord bot token>
API_KEY=<your openai api key>
```

* Run the bot with the command above.

#### Notes:

* This bot is not meant to be used in a production environment, it's just a 2 hour fun coding project
