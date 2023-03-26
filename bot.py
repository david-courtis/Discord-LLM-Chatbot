import os
import logging
import discord
import openai
import json
import re
from dotenv import load_dotenv

try:
	load_dotenv()
except:
	print("No .env file found")

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')
openai.api_key = API_KEY

cache = []

class MyClient(discord.Client):

	async def on_ready(self):
		self.cache = {}
		self.replyto = ["why", "what", "how", "?", "wtf", "idk", "huh"]
		self.threshold = 5000
		self.send_limit = 2001
		print(f'Logged on as {self.user}!')

	async def on_message(self, message):

		print(f'Message from {message.author}, {message.guild}, {message.channel}: {message.content}')
		# get server
		serverchannel = str(message.guild) + str(message.channel)
		if serverchannel not in self.cache:
			self.cache[serverchannel] = []

		# save message and time (to the second) to json file as json object with keys 'time', 'author', 'content', 'replied to' (if applicable), messagechannel
		# with open('messages.json', 'a') as f:
		# 	json.dump({"time": f'{message.created_at}', "author": f'{message.author}', "content": f'{message.content}', "replied to": f'{message.reference}', "serverchannel": f'{serverchannel}'}, f)

		mentioned = client.user.mentioned_in(message)

		if mentioned:
			message.content = message.content.replace(f'<@{client.user.id}>', '')

		# save message and time (to the second) to cache, also save the name of the person it was replying to
		self.cache[serverchannel].append([message.created_at,message.author,message.content,message.reference.resolved.author if message.reference is not None and message.reference.resolved is not None else None])

		if message.author == self.user:
			return

		numCharsCached = sum([len(message[2]) for message in self.cache[serverchannel]])

		# if waiting for reply, don't send message to gpt-3
		if numCharsCached > self.threshold or mentioned or any([word in message.content.lower() for word in self.replyto]):

			while numCharsCached > self.send_limit:
				numCharsCached -= len(self.cache[serverchannel][0][2])
				self.cache[serverchannel].pop(0)
			print(numCharsCached)

			print(f'----Sending {numCharsCached} Chars----')
			messages = [{"role": "system", "content": "You are a normal human being called ViViV2#5153, assume you are in conversation and you're casual and close. Don't Be formal. Don't mention %USERNAME"}]
			messages.append({"role": "user", "content": "%USERNAME said %COMMAND %replying to %USERNAME%"})
			for item in self.cache[serverchannel]:
				if item[3] is not None:
					messages.append({"role": "user", "content": f'{item[1]} said {item[2]} replying to {item[3]}'})
				else:
					messages.append({"role": "user", "content": f'{item[1]} said {item[2]}'})
			response = send_message(messages)
			text = response["choices"][0]["message"]["content"]
			# remove %USERNAME "anything" space in regex
			text = re.sub(r"ViViV2(#5153)?\s?[^\s]*\s?", "", text)
			# remove %(replying to *)%
			text = re.sub(r"(r|R)eplying to\s?.*", "", text)
			print(text)

			if mentioned:
				await message.channel.send(text, reference=message)
			else:
				await message.channel.send(text)
			
		

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
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
client = MyClient(intents=intents)
client.run(TOKEN, log_handler=handler)