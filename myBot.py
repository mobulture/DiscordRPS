import discord
from discord.ext import commands
#from dotenv import load_dotenv
from datetime import datetime
import os
import asyncio
import time 
bot = discord.ext.commands.Bot(command_prefix ="$")

#load_dotenv()

#client = discord.Client()
Token = os.getenv("TOKEN")
class MatchMaker():
    def __init__(self):
        self.matches = set()
matcher = MatchMaker()

@bot.event
async def on_ready():
    print("Bot ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hi":
        await message.channel.send( "BOY")
 
    if message.content == "emote me":
        msg = await message.channel.send("Best emote me now!")
        def check(reaction,user):
            return user == message.author and str(reaction.emoji) == "👍"
        
        try:
            reaction,user = await bot.wait_for('reaction_add', timeout = 50.0, check=check)
            print(reaction)
            print(user)
        except asyncio.TimeoutError:
            await msg.edit(content = ":thumbsdown:")
        else:
            await msg.edit(content = "👍")
    await bot.process_commands(message)
@bot.command(name = "test")

async def test(ctx):
    await ctx.send("WHATS BOPPING {}".format(ctx.author.name))
    await ctx.send(ctx.message) 

def checkValid(input):
    if input.lower() in ('yes','y','1','ya'):
        return True
    if input.lower() in ('no','n','0','nah'):
        return False

@bot.command()
async def check(ctx,arg: checkValid):
    print(arg)
    await ctx.send(arg)


async def rpshelper(ctx,user1,user2,results):
    response1 = False
    response2 = False
    
    def check(message):
        valid = ['rock','paper','scissors']
        nonlocal response1,response2,results

        if message.author.id == user1:
            if message.content in valid and not response1:
                response1 = True
                results[0] = message.content
            return response1
        if message.author.id == user2:
            if message.content in valid and not response2:
                response2 = True
                results[1] = message.content
            return response2
        return False

    try:
        while not response1 or not response2:
            await bot.wait_for('message',check = check)

    except asyncio.TimeoutError:
        return results
    else:
        return results

def findWinner(action1,action2):
    lose = [("scissors","rock"),('rock','paper'),('paper','scissors')]
    if (action1 == action2):
        return None
    if (action1,action2) in lose:
        return 2
    return 1


@bot.command()
async def rps(ctx, challenger:discord.Member = None, toWin = 2):
    global matcher
    if ctx.author.id in matcher.matches or challenger.id in matcher.matches:
        await ctx.send("At least one of you are already in a match or are awaiting one")
        return
    users = [ctx.author,challenger]

    if users[0].id==users[1].id:
        await ctx.send("You can't challenge yourself my guy")
        return
    
    if (users[1].id == None or users[1].id == bot.user.id):
        await ctx.send("I WILL CHALLENGE YOU THEN")
        return 

    matcher.matches.add(users[0].id)
    matcher.matches.add(users[1].id)

 
    await ctx.send(users[1].mention +". You have been challenged by "+ users[0].name)

    def check(message):
        yes = ["yes", 'y']
        no = ['no','n']
        print("checking")
        return message.author.id == challenger.id and message.content.lower() in yes

    try:
        accepted =await bot.wait_for('message',timeout = 20.0, check = check)
        print(accepted)

    except:
        await ctx.send("Did not respond")
    else:
        await ctx.send("Opponent has responded")
        wins = [0,0]
        won = False
        repeats = 0
        while not won and repeats <= 3:
            try:

                actions = ["",""]
                await ctx.send("Current score {0}: {1}  to {2}: {3} out of {4}".format(users[0].name,wins[0],users[1].name,wins[1],toWin))
                rpsactions = asyncio.ensure_future(rpshelper(ctx,ctx.author.id,challenger.id,actions))
                msg = await ctx.send("Enter your moves in 5 seconds")
                for i in range(1,6):
                    await msg.edit(content = "Enter your moves in {0} seconds".format(5 - i))
                    await asyncio.sleep(1)
                await msg.edit(content = "GO!")
                actions = rpsactions.result()

            except asyncio.InvalidStateError:
                if actions[0] == "" and actions[1] == "":
                    if repeats == 3:
                        await ctx.send("Ok fine, I'll just stop :sad:")
                        matcher.matches.remove(users[0].id)
                        matcher.matches.remove(users[1].id)
                        return
                    await ctx.send("Neither of you guys did anything, come on")
                    repeats +=1
                    continue

                if actions[0] == "":
                    await ctx.send("{0} sent nothing, so {1} wins the round".format(users[0].name,users[1].name))
                    wins[1]+=1
                    roundWinner = 1

                else:
                    await ctx.send("{0} sent nothing, so {1} wins the round".format(users[1].name,users[0].name))
                    wins[0] += 1
                    roundWinner = 0

            if actions[0] and actions[1]:
                await ctx.send("THE FIGHT HAS STARTED")
                result = findWinner(actions[0],actions[1])
                if not result:
                    await ctx.send("TIE, GO AGAIN")
                else:
                    await ctx.send("{0} won the round".format(users[result-1].name) )
                    roundWinner = result-1
                    wins[roundWinner]+=1
        
            if wins[roundWinner] == toWin:
                    await ctx.send("{0} wins!".format(users[roundWinner].name))
                    matcher.matches.remove(users[0].id)
                    matcher.matches.remove(users[1].id)
                    return

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = ctx.author.name
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

@bot.command()
async def slap(ctx, *, reason: Slapper()):
    await ctx.send(reason)

@bot.command()
async def joined(ctx, member:discord.Member):
    await ctx.send(member.display_name)

async def prinbothelper():
    word = "Punt"
    def check(message):
        print(word)
        print("in check")
        return message.content == "rock"
    
    try:
        print("IN print bot before await)")
        result = await bot.wait_for('message', timeout = 5,check = check)
    except asyncio.TimeoutError:
        print("no response")
    else:
        print(bot)

@bot.command()
async def printbot(ctx):
    await prinbothelper()

@bot.command()
async def history(ctx):
    print(ctx.guild)
    async for message in ctx.channel.history(limit = 200):
        print(message.content, message.author.name)
#client.run(Token)

@bot.command()
async def invokedsdas(ctx):
    await ctx.send(ctx.invoked_with)



bot.run(Token)
