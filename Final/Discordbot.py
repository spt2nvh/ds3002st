#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 22:26:38 2022

@author: shannontran
"""

import os
import discord
import json
import requests


TOKEN = os.getenv('DISCORD_TOKEN','OTY2MzU2MjkyMDM1ODI1NzQ0.YmAjbg.Yde7jtngUbb5DYcu7tPbymWOALo')

client = discord.Client() # Connects to discord

greeting = ['hi', 'Hi', 'Hello', 'hello'] # Possible user inputs for greeting to start bot
affirmative = ['Yes', 'yes', 'yeah', 'Yeah', 'Yes please', 'yes please', 'Hell yeah', 'hell yeah'] # Possible user inputs for joke
non_affirmative = ['No', 'no', 'No thanks', 'no thanks', 'Nope', 'nope', 'Hell no', 'hell no'] # Possible user inputs for no joke
help_me = ['Help','help','Help me','help me','Please help me', "please help me", 'Please help', 'please help'] # Possible user inputs for help 
 

def get_joke(): # Pulls joke of the day from Joke API: https://jokes.one/api/joke/ 
    response = requests.request("GET", "https://api.jokes.one/jod")
    data = response.json()
    contents = data['contents']
    jokes = contents['jokes']
    joke = jokes[0]['joke']
    text = joke['text']
    return text

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
 
  

@client.event

async def on_message(message): # Prevents message from self
    if message.author == client.user:
        return

    msg = message.content

    if any(word in msg for word in greeting): # Greeting, prompt user for joke
        await message.channel.send('Hello, would you like to hear a joke?')
        
    if any(word in msg for word in affirmative): # Uses get_joke function to return joke of the day
        tell_joke = get_joke()
        await message.channel.send(tell_joke + "If you want to hear another, type 'Tell one more'. If not, type 'No'")
    
    if message.content.startswith("Tell one more"): # Handles if user wants another joke
        tell_joke = get_joke()
        await message.channel.send("Oops, I only tell one per day. Come back tomorrow for more!")
        
    if any(word in msg for word in non_affirmative): # If user does not want to hear a joke
        await message.channel.send("Ok, goodbye!")
    
    if any(word in msg for word in help_me): #Help response
        await message.channel.send("Don't panic! Type 'Hi' or 'Hello' to hear a joke. If you need something else, ask Google lol.")
        
    else:
        await message.channel.send("Sorry, I don't understand. Say 'Hi' or 'Hello' to me to continue.") # If bot does not recognize input, prompts user to begin again
 


client.run(TOKEN)

















