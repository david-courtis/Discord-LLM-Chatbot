# Discord LLM Chatbot

A discord bot that uses LLM API calls to generate responses to messages.

## Capabilities:

* Will reply to a message mentioning the bot in any channel.
* Will reply to any message in designated channels that has a "why", "what", "how", "?", "wtf", "idk", "huh".
* Has 2000 characters of memory per channel.
* Will reply every 5000 characters in a channel.
* Uses OpenAI's completion API to generate responses.

## Requirements
* [Python 3.11+](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/)
* Make
    * [Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
    * Linux: `apt-get install make` or similar.
* [Discord](https://discord.com/download)

## Setup instructions:

### Discord Bot
* Create a new Discord application at https://discord.com/developers/applications
* On the Discord application settings, navigate to the Installation settings. Scroll to Default Install Settings -> Guild Install and add "bot" scope to scopes.
* On the same page, copy the Discord Provided Link into the browser and follow the steps to add the bot to your server.

### Environment Setup
* Clone the repo.
* Create `.env` under the root directory by copying `.env.template`.
* Fill in the required environment variables.
    * `DISCORD_TOKEN` is your bot's Token. Get it from your Discord application's Bot settings -> Reset Token.
    * `OPENAI_API_KEY` is your API key for the OpenAI platform: https://platform.openai.com/api-keys
    * `DESIGNATED_CHANNELS` is a comma-separated list of channel IDs that the bot will listen to, automatically responding to messages containing certain keywords. Channels do not need to be listed here for the bot to respond to @ mentions. Get the Channel ID by right-clicking the channel in discord -> Copy Channel ID.
    * `GUILD_TEST_ID` is your Discord server's ID. Get it by right-clicking the server in Discord -> Copy Server ID.
    * `OWNER_ID` is your Discord account's User ID. Get it by right-clicking your name in Discord -> Copy User ID.

### Startup
* Run `make start` in the terminal.
