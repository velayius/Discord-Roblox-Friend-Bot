import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import threading
import requests
import json
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '.', intents=intents)

with open('content\\cookies.txt', 'r') as cookies:
    cookies = cookies.read().splitlines()

with open('content\\proxies.txt', 'r') as proxies:
    proxies = proxies.read().splitlines()

config = json.loads(
    open(
        'content\\config.json',
        'r'
    ).read()
)['config']

if config['cookies']['format'] == 1:

    batch = []

    for x in cookies:

        batch.append(
            '_|' + x.split('_|')[1]
        )
    
    cookies = batch

PROXY_TYPE = config['proxies']['type']

@client.event
async def on_ready():
    print("Bot is online")

ServerId = 000000000000000 # Dedicated ServerID

def send_friend(cookie, userid): # SendFriend Function
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            friend = session.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship')
            if friend.status_code == 200:
                print('sent')
            else:
                print(friend.text)
    except:
        print('skipped')


@client.slash_command(name = "friend", description='friend botter', guild_ids=[ServerId]) # FriendBot Command
async def friendcommand(interaction: Interaction,  user_id:str,):
    userid = user_id
    amount = 1
    friendEmbed = nextcord.Embed(title='Discord Bot', description=f'NOTE: This may not send the full amount of friends.', color=0xFFE80B)
    await interaction.response.send_message(embed=friendEmbed)
    for x in range(int(amount)):
        cookie = cookies[x]
        threading.Thread(target=send_friend, args=(cookie,userid,)).start()
    

    
client.run('') # Discord Bot Token
