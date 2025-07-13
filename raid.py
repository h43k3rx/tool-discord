import os
import discord
import time
import json
from discord.ext import commands
from discord import app_commands
from colorama import Fore, Style, init
from datetime import datetime, timezone, timedelta

os.system('cls' if os.name == 'nt' else 'clear')
asciiart = Fore.BLUE + r"""
  _   _ _             ___      _    _ 
 | |_| | |__ ___ _   | _ \__ _(_)__| |
 | ' \_  _\ V / ' \  |   / _` | / _` |
 |_||_||_| \_/|_||_| |_|_\__,_|_\__,_|
                                      
"""
print(asciiart)
print(Fore.BLUE + "Đang lấy token...")
time.sleep(2)
print(Fore.GREEN + "Đã xác định được token")
import time, sys
states = ["Loading", "Loading.", "Loading..", "Loading... \n"]
t = time.time()

while time.time() - t < 1:
    for s in states:
        if time.time() - t >= 1:
            break
        sys.stdout.write('\r' + Fore.WHITE + s)
        sys.stdout.flush()
        time.sleep(0.3)
def get_token():
    try:
        with open("token.json", "r") as f:
            data = json.load(f)
            return data.get("token")
    except FileNotFoundError:
        print("File token.json chưa được tạo hãy chạy file main.py")
    except json.JSONDecodeError:
        print("Lỗi khi decode JSON")
    return None
token = get_token()
time.sleep(1)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

goiday_meme = [
    "Dậy đi {name} ơi! Trời sáng rồi!",
    "{name} ngủ gì lắm thế, dậy làm việc nào!",
    "Alo alo {name}, dậy ăn sáng nè!",
    "{name}, mày ngủ như chết thế?",
    "DẬYYYY {name.upper()}!!! CÒI BÁO THỨC NÈ!",
]

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(Fore.GREEN + f'✅ Bot đã sẵn sàng. Logged in as {bot.user}.')
    print(Fore.GREEN + f'✅ Total Synced: {len(synced)}')
    print("Hướng dẫn sử dụng:")
    print(f"Link mời bot của bạn: https://discord.com/api/oauth2/authorize?client_id={bot.user.id} \n Sau đó bấm thêm vào ứng dụng của tôi")
    print("Vào server bạn muốn nuke và ghi lệnh /spam ,v.v.")

@bot.tree.command(name="spam", description="Nhắn một tin nhắn nhiều lần")
@app_commands.describe(message="Nội dung muốn gửi", times="Số lần gửi (tối đa 5)")
async def say(interaction: discord.Interaction, message: str, times: int):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    if times > 5:
        await interaction.response.send_message("❌ Bạn chỉ được gửi tối đa 5 lần!", ephemeral=True)
        print(Fore.RED + f"❌[{now_utc}] [LOG    ] Userid: {interaction.user.id} cố vượt mức bích cờ bôn")
        return
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /spam {message} với số lần {times    }")
    for _ in range(times):
        await interaction.followup.send(message, allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.tree.command(name="say", description="Nhắn một tin nhắn")
@app_commands.describe(message="Nội dung muốn gửi")
async def say1(interaction: discord.Interaction, message: str):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /say {message}")
    await interaction.followup.send(message, allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.tree.command(name="goiday", description="Gọi một ai đó dậy bằng câu meme")
@app_commands.describe(user="Người bạn muốn gọi dậy")
async def goiday(interaction: discord.Interaction, user: discord.User):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /goiday {user}")
    for template in goiday_meme:
        msg = template.format(name=user.mention)
        await interaction.followup.send(msg)

@bot.tree.command(name="spamembed", description="Embed Spammer")
async def embed(interaction: discord.Interaction):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /spamembed")
    emb = discord.Embed(
        title="<-+-🤫raid by bot Noname🤫-+->",
        description="<-+-:0 🤫 dễ raid quá 🤫 0:-+-> \n <--ko bt setup thì dễ chết thôi con-->",
        color=discord.Color.blue()
    )
    for _ in range(5):
        await interaction.followup.send(embed=emb)

@bot.tree.command(name="pingevery", description="Ping everyone thần chưởng")
async def pingevery(interaction: discord.Interaction):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    return not interaction.guild or interaction.guild.id != 1349968006649876512
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /pingevery")
    for _ in range(5):
        await interaction.followup.send("@everyone raid no permission by Noname", allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.tree.command(name="pinghere", description="Ping here thần chưởng")
async def pingevery(interaction: discord.Interaction):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /pinghere")
    for _ in range(5):
        await interaction.followup.send("@here raid no permission by Noname", allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.tree.command(name="flood", description="Flood chat")
async def pingevery(interaction: discord.Interaction):
    utc7 = timezone(timedelta(hours=7))
    now_utc = datetime.now(utc7).strftime("%Y-%m-%d %H:%M:%S")
    await interaction.response.send_message("🤫Sending...", ephemeral=True)
    print(Fore.GREEN + f"✅[{now_utc}] [LOG    ] Userid: {interaction.user.id} vừa dùng lệnh /flood")
    await interaction.followup.send("⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀⠀\n⠀")

bot.run(token)
