import configparser
import time
import json
from discord.ext import commands

bot = commands.Bot(command_prefix="~", description="CivBot")

try:
    grants = json.load(open('grants.json'))
except FileNotFoundError:
    grants = dict()
except json.decoder.JSONDecodeError:
    grants = dict()

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

@bot.command(pass_context=True)
async def trust(ctx, content):
    """trusts a user"""
    granted = content[7:].strip()[3:-1]
    grantee = ctx.author.id
    grants[grantee] = granted
    with open("grants.json", "w") as file:
        json.dump(grants, file)
    await ctx.channel.send("Granted {0}'s voting power to {1}".format(ctx.author.name, granted))
    print(grants)

@bot.command(pass_context=True)
async def info(ctx, content):
    """Gets info on a user"""
    member = ctx.message.mentions[0] #todo : check if valid

    output = [ctx.guild.get_member(grantee) for grantee in grants if grants[grantee] == member.id]
    if len(output) > 0:
        await ctx.channel.send("{0} is trusted by {1}: {2}".format(member.name, len(output), output))
    else:
        await ctx.channel.send("{0} is trusted by {1}".format(member.name, len(output)))
    await ctx.channel.send("{0} trusts: {1}".format(member.name, grants[member.id]))

if __name__ == "__main__":
    config_type = 'test'
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get(config_type, 'token')
    while True:
        try:
            bot.run(token)
        except Exception as e:
            print("Error", e)
        print("Waiting until restart")
        time.sleep(10)
