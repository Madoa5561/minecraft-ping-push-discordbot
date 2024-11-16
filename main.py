import discord
from discord.ext import tasks
from mcstatus import JavaServer
from datetime import datetime

#Discordボットのトークンを設定
TOKEN = ''
#更新したいチャンネルIDを設定
CHANNEL_ID = 000000000000000

#Minecraftサーバーの情報
SERVER_IP = "xxx.com"
SERVER_PORT = 25565 #defalt port
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_server_status(ip, port=25565):
    server = JavaServer(ip, port)
    try:
        status = server.status()
        ping = round(status.latency, 2)
        player_count = status.players.online
        if status.players.sample:
            player_list = [player.name for player in status.players.sample]
        else:
            player_list = []
        current_time = datetime.now().strftime('%H:%M:%S')
        message = (f"**:white_check_mark:{ip} の状態:white_check_mark:**\n"
                    f"取得日時: {current_time}\n"
                    f"Ping: {ping} ms\n"
                    f"現在の参加人数: {player_count}\n"
                    f"↓参加者プレイヤーリスト↓\n{', '.join(player_list) if player_list else 'いません'}")
        return message
    except Exception as e:
        return f"サーバーへの接続に失敗しました: {e}"

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    #ボットがオンラインになった時に、最初のメッセージを送信
    channel = client.get_channel(CHANNEL_ID)
    initial_message = await channel.send("Minecraftサーバーの状態を監視しています...")
    #30秒ごとにメッセージを更新するタスクを開始
    update_ping_status.start(channel, initial_message)

@tasks.loop(seconds=30)
async def update_ping_status(channel, message):
    server_status = get_server_status(SERVER_IP, SERVER_PORT)
    #メッセージを更新
    await message.edit(content=server_status)

#ボットの起動
client.run(TOKEN)
