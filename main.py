import discord
import json
import os

try:
	grants = json.load(open('grants.json',))
except FileNotFoundError:
	grants = dict()
except json.decoder.JSONDecodeError:
    grants = dict()

client = discord.Client()
guild = discord.Guild

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("~stop"):
        with open("grants.json", "w") as file:
            json.dump(grants, file)
        await message.channel.send("Shut down")
        await client.logout()

    if message.content.startswith("~trust "):
        granted = message.content[7:].strip()[3:-1]
        grantee = message.author.id
        grants[grantee] = granted

        with open("grants.json", "w") as file:
            json.dump(grants, file)
        await message.channel.send("Granted {0}'s voting power to {1}".format(message.author.name, granted))
        print(grants)

    if message.content.startswith("~info "):
        granted = message.content[6:].strip()[3:-1]
        print(granted)
        output = [guild.get_member(grantee) for grantee in grants if grants[grantee] == granted]
        if len(output) > 0:
            await message.channel.send("{0} is trusted by {1}: {2}".format(guild.get_member(granted), len(output), output))
        else:
                await message.channel.send("{0} is trusted by {1}".format(guild.get_member(granted), len(output)))
        await message.channel.send("{0} trusts: {1}".format(granted, grants[granted]))

client.run(os.environ.get('LIQUID_TOKEN'))