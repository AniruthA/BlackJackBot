import discord, random,json, asyncio
from discord.ext import commands
bot = commands.Bot(command_prefix='bj ')


GREEN = 0x00ff00
RED = 0xff0000
BLUE = 0x0000ff
PURPLE = 0xff00ff
BLUEGREEN = 0x00ffff
YELLOW = 0xffff00
COLORS = [BLUE,YELLOW,BLUEGREEN,PURPLE]


def addUser(username):
  currentData = json.loads(open('user.db','r').read())
  currentData[username] = {'score':0, 'wins':0, 'losses':0, 'coins':100, 'bet':10}
  open('user.db','w').write(json.dumps(currentData))
def editUserScore(username,newScore):
  currentData = json.loads(open('user.db','r').read())
  currentData[username]['score'] = newScore
  open('user.db','w').write(json.dumps(currentData))
def editUserLosses(username):
  currentData = json.loads(open('user.db','r').read())
  currentData[username]['losses'] += 1
  open('user.db','w').write(json.dumps(currentData))
def editUserWins(username):
  currentData = json.loads(open('user.db','r').read())
  currentData[username]['wins'] += 1
  open('user.db','w').write(json.dumps(currentData))
def editUserCoins(username,coins):
  currentData = json.loads(open('user.db','r').read())
  currentData[username]['coins'] = coins
  open('user.db','w').write(json.dumps(currentData))
def editUserBet(username,coins):
  currentData = json.loads(open('user.db','r').read())
  currentData[username]['bet'] = coins
  open('user.db','w').write(json.dumps(currentData))

failureMessages = ['oof.','thats gotta hurt','sucks to suck','ouch...','oh oh.','😢']
successMessages = ['nice job','Dang','Good job!','wow']

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
  guild = bot.guilds[0]
  database = json.loads(open('user.db','r').read())
  for member in guild.members:
    if member.name+member.discriminator not in database.keys():
      addUser(member.name+member.discriminator)
  print('Succesfully added all users into database')

@bot.command()
async def hit(ctx):
  database = json.loads(open('user.db','r').read())
  if ctx.message.author.name+ctx.message.author.discriminator not in database.keys():
    addUser(ctx.message.author.name+ctx.message.author.discriminator)

  author = database[ctx.message.author.name+ctx.message.author.discriminator]

  newScore = author['score']+random.randint(1,11)
  editUserScore(ctx.message.author.name+ctx.message.author.discriminator,newScore)
    
  score = discord.Embed(title="BlackJack", description="@"+ctx.message.author.name+"'s Score : "+str(newScore), color=random.choice(COLORS))
    
  if newScore == 21:
    score.add_field(name="You Won!" , value=random.choice(successMessages), inline=False)
    score.color = GREEN
  if newScore > 21:
    score.add_field(name="You busted" , value=random.choice(failureMessages), inline=False)
    score.color = RED
    editUserCoins(ctx.message.author.name+ctx.message.author.discriminator,(database[ctx.message.author.name+ctx.message.author.discriminator]['coins'])-(database[ctx.message.author.name+ctx.message.author.discriminator]['bet']))

  await ctx.send(embed=score)
  if newScore == 21:
    editUserScore(ctx.message.author.name+ctx.message.author.discriminator,0)
    editUserWins(ctx.message.author.name+ctx.message.author.discriminator)
  if newScore > 21:
    editUserScore(ctx.message.author.name+ctx.message.author.discriminator,0)
    editUserLosses(ctx.message.author.name+ctx.message.author.discriminator)

@bot.command()
async def stop(ctx):
  database = json.loads(open('user.db','r').read())
  if ctx.message.author.name+ctx.message.author.discriminator not in database.keys():
    addUser(ctx.message.author.name+ctx.message.author.discriminator)

  finalScore = discord.Embed(title="BlackJack", description="Let's see how you did", color=random.choice(COLORS))
  finalScore2 = discord.Embed(title="BlackJack", description="Let's see how you did", color=random.choice(COLORS))

  userScore = database[ctx.message.author.name+ctx.message.author.discriminator]['score']
  botScore = random.randint(10,26)

  botWin = False
  userWin = False

  if botScore > userScore and botScore < 21:
    botWin = True
    userWin = False
  elif botScore < userScore and userScore < 21:
    botWin = False
    userWin = True
  elif botScore> 21:
    botWin = False
    userWin = True
  elif botScore  == 21:
    if userScore == 21:
      botWin = False
      userWin = True
    else:
      botWin = True
      userWin = False
  elif botScore == userScore:
    botWin = False
    userWin = True

  finalScore.add_field(name=f'@{ctx.message.author.name}\'s Score : ',value=f"{userScore}",inline=False)
  finalScore2.add_field(name=f'@{ctx.message.author.name}\'s Your Score : ',value=f"{userScore}",inline=False)
  finalScore.add_field(name='The Bot\'s Score : ',value=f"{botScore}",inline=False)
  finalScore2.add_field(name='The Bot\'s Score : ',value=f"{botScore}",inline=False)
  finalScore.add_field(name='And the winner is',value="drumroll please")
  if botWin:
    finalScore2.add_field(name='And the winner is the bot!',value=f"{random.choice(failureMessages)}")
    editUserCoins(ctx.message.author.name+ctx.message.author.discriminator,(database[ctx.message.author.name+ctx.message.author.discriminator]['coins'])-(database[ctx.message.author.name+ctx.message.author.discriminator]['bet']))

    editUserLosses(ctx.message.author.name+ctx.message.author.discriminator)
    finalScore2.color = RED
  elif userWin:
    finalScore2.add_field(name = 'And the winner is you!',value =f"{random.choice(successMessages)}")
    editUserWins(ctx.message.author.name+ctx.message.author.discriminator)

    editUserCoins(ctx.message.author.name+ctx.message.author.discriminator,(database[ctx.message.author.name+ctx.message.author.discriminator]['coins'])+(database[ctx.message.author.name+ctx.message.author.discriminator]['bet']))

    finalScore2.color =  GREEN

  editUserScore((ctx.message.author.name+ctx.message.author.discriminator),0)
  message = await ctx.send(embed=finalScore)
  await asyncio.sleep(1)
  await message.edit(embed=finalScore2)
  
@bot.command()
async def bet(ctx,newBet=10):
  database = json.loads(open('user.db','r').read())
  if ctx.message.author.name+ctx.message.author.discriminator not in database.keys():
    addUser(ctx.message.author.name+ctx.message.author.discriminator)
  author = database[ctx.message.author.name+ctx.message.author.discriminator]

  editUserBet(ctx.message.author.name+ctx.message.author.discriminator,newBet)

  if int(newBet) >= 10 and int(newBet) <= 5000: 
    await ctx.send(embed=discord.Embed(title="BlackJack", description=f"Your bet was successfuly changed to {newBet}", color=random.choice(COLORS)))
  else:
    await ctx.send(embed=discord.Embed(title="BlackJack", description="I'm sorry, you bet cannot be less than 10 coins. Your bet can also not be greater than 5000", color=random.choice(COLORS)))

@bot.command()
async def stats(ctx):
  database = json.loads(open('user.db','r').read())
  if ctx.message.author.name+ctx.message.author.discriminator not in database.keys():
    addUser(ctx.message.author.name+ctx.message.author.discriminator)
  author = database[ctx.message.author.name+ctx.message.author.discriminator]

  stats = discord.Embed(name=f'@{ctx.message.author.name}\'s Stats',value="Let's take a look at those stats.",color=random.choice(COLORS))
  stats.add_field(name = 'Wins',value =f"{author['wins']}")
  stats.add_field(name = 'Losses',value =f"{author['losses']}")
  stats.add_field(name = 'Coins',value =f"{author['coins']}")
  stats.add_field(name = 'Bet',value =f"{author['bet']}")
  stats.add_field(name = 'Overall Games',value =f"{author['wins']+author['losses']}")


  await ctx.send(embed=stats)

@bot.command()
async def HELP(ctx):
  helpEmbed = discord.Embed(title="Need help?", description="Well, we've got your back", color=random.choice(COLORS))
  helpEmbed.add_field(name='bj hit',value='hit to draw a card and add to your total!',inline=False)
  helpEmbed.add_field(name='bj stop',value='this is the bot equivalent of stopping in a blackjack game. the bot will then proceed to draw its cards, and the values will be compared!',inline=False)
  helpEmbed.add_field(name='bj stats',value='view your stats',inline=False)
  helpEmbed.add_field(name='bj bet <amount>',value='change your bet amount. by default it is 10',inline=False)
  helpEmbed.add_field(name='bj HELP',value='really?',inline=False)
  helpEmbed.add_field(name='bj leaderboard',value='coming soon, to a discord bot near you',inline=False)
  
  await ctx.message.author.send(embed=helpEmbed)

bot.run("NzEyMzM3NTU1NDExOTU5ODc4.XsQGLQ.XD3CNfT6hhjmrWLRRJ0Wzmw_ZFk")

