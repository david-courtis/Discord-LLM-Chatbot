from datetime import datetime
import os
import logging
import discord
import openai
import json
import re
import uwuify
from dotenv import load_dotenv

try:
    load_dotenv()
except:
    print("No .env file found")

try:
    TOKEN = os.getenv('DISCORD_TOKEN')
    API_KEY = os.getenv('API_KEY')
except KeyError:
    Exception("No API key found")

openai.api_key = API_KEY

cache = []


class MyClient(discord.Client):

    async def on_ready(self):
        self.cache = {}
        self.replyto = ["why", "what", "how", "?", "wtf", "idk", "huh"]
        self.threshold = 5000
        self.send_limit = 1200
        self.smiley = True
        # set the activity to "Playing with fire"
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Mention me to chat! ($normal to disable uwu)"))

        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(
            f'Message from {message.author}, {message.guild}, {message.channel}: {message.content}')
        # get server
        serverchannel = str(message.guild) + str(message.channel)
        if serverchannel not in self.cache:
            self.cache[serverchannel] = []

        # save message and time (to the second) to json file as json object with keys 'time', 'author', 'content', 'replied to' (if applicable), messagechannel
        # with open('messages.json', 'a') as f:
        # 	json.dump({"time": f'{message.created_at}', "author": f'{message.author}', "content": f'{message.content}', "replied to": f'{message.reference}', "serverchannel": f'{serverchannel}'}, f)

        mentioned = client.user.mentioned_in(message)

        if mentioned:
            message.content = message.content.replace(
                f'<@{client.user.id}>', '')

        # save message and time (to the second) to cache, also save the name of the person it was replying to

        if message.author == self.user:
            return

        if "$clear" in message.content:
            self.cache[serverchannel] = []

        self.cache[serverchannel].append([message.created_at, message.author, message.content,
                                         message.reference.resolved.author if message.reference is not None and message.reference.resolved is not None else None])

        numCharsCached = sum([len(message[2])
                             for message in self.cache[serverchannel]])

        # if waiting for reply, don't send message to gpt-3
        if mentioned or ((numCharsCached > self.threshold or any([word in message.content.lower() for word in self.replyto])) and int(message.channel.id) == 894807066953285673):

            while numCharsCached > self.send_limit:
                numCharsCached -= len(self.cache[serverchannel][0][2])
                self.cache[serverchannel].pop(0)

            print(f'----Sending {numCharsCached} Chars----')
            messages = [
                {"role": "system", "content": "You (ViViV2) are a normal human being, assume you are in conversation and you're casual and close. Don't Be formal"}]
            messages.append(
                {"role": "user", "content": "%USERNAME said %COMMAND%"})
            for item in self.cache[serverchannel]:
                if item[3] is not None:
                    messages.append(
                        {"role": "user", "content": f'{item[1]} said {item[2]} (replying to {item[3]})'})
                else:
                    messages.append(
                        {"role": "user", "content": f'{item[1]} said {item[2]}'})

            response = send_message(messages)

            text = response["choices"][0]["message"]["content"]

            # remove %USERNAME "anything" space in regex
            text = re.sub(r"(v|V)i(v|V)i(v|V)2(#5153)?\s?[^\s]*\s?", "", text)
            # remove %(replying to *)%
            text = re.sub(r".(r|R)eplying to\s?.*", "", text)
            # remove digits
            text = re.sub(r"#[0-9][0-9][0-9][0-9]", "", text)

            if ("$uwu" in message.content):
                uwud = uwuify_text(text)
            elif (self.smiley):
                uwud = uwuify_text(text, flags=uwuify.SMILEY)
            else:
                uwud = text

            time = datetime.now()

            if mentioned:
                self.cache[serverchannel].append(
                    [time, client.user, text, message.author])
                await message.channel.send(uwud[:2000], reference=message)
            else:
                self.cache[serverchannel].append(
                    [time, client.user, text, None])
                await message.channel.send(uwud[:2000])


def uwuify_text(text, flags=uwuify.SMILEY | uwuify.YU | uwuify.STUTTER):
    try:
        # sometimes uwuify fails, library is not perfect
        uwud = uwuify.uwu(text, flags=flags)
    except:
        uwud = text
    return uwud


def send_message(messages):
    # send message to gpt-3
    # get response
    # send response to discord
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )


intents = discord.Intents.default()
intents.message_content = True
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
client = MyClient(intents=intents)
client.run(TOKEN, log_handler=handler)
