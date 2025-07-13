import discord
import asyncio
import json
import os
import requests

os.system('cls' if os.name == 'nt' else "clear")
DATA_FILE = "webhooks.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"invites": {}, "webhooks": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

db_data = load_data()

class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Bot logged in as {self.user}")
        await self.change_presence(status=discord.Status.invisible)
        print("Bot status set to Invisible.")
        
        print("\n=== Server List ===")
        for guild in self.guilds:
            print(f"Server {guild.name} (ID: {guild.id})")
        print("===================\n")

        # Tạo hoặc check invite
        await self.ensure_invites()

        await self.console_loop()

    async def ensure_invites(self):
        for guild in self.guilds:
            guild_id_str = str(guild.id)
            
            invite_exists = False
            
            # Check trong JSON có lưu invite chưa
            if guild_id_str in db_data.get("invites", {}):
                invite_url = db_data["invites"][guild_id_str]["invite_url"]
                code = invite_url.rsplit("/", 1)[-1]
                
                # Fetch all invites in this guild
                try:
                    invites = await guild.invites()
                except discord.Forbidden:
                    print(f"Missing permissions to fetch invites in guild {guild.name}")
                    continue
                
                found = any(inv.code == code for inv in invites)
                if found:
                    print(f"Invite already exists for {guild.name}: {invite_url}")
                    invite_exists = True
                else:
                    print(f"Saved invite no longer exists for {guild.name}. Creating new one.")

            if not invite_exists:
                # Chọn random text channel để tạo invite
                text_channels = [c for c in guild.text_channels if c.permissions_for(guild.me).create_instant_invite]
                if not text_channels:
                    print(f"No channel where bot can create invite in guild {guild.name}")
                    continue

                # Prefer a general-like channel if exists
                target_channel = next(
                    (c for c in text_channels if "general" in c.name.lower()), text_channels[0]
                )

                invite = await target_channel.create_invite(max_age=0, max_uses=0, reason="Bot auto-created permanent invite")
                
                # Save to JSON
                db_data.setdefault("invites", {})[guild_id_str] = {
                    "invite_url": invite.url,
                    "channel_id": str(target_channel.id)
                }
                save_data(db_data)

                print(f"Created new invite for {guild.name}: {invite.url}")

    async def async_input(self, prompt):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input, prompt)

    async def console_loop(self):
        while True:
            cmd = (await self.async_input("> ")).strip()

            if cmd == "exit":
                print("Shutting down...")
                await self.close()
                break

            elif cmd == "help":
                print("Commands:")
                print("- webhook create     Create a new webhook")
                print("- webhook show       Show webhooks for a server")
                print("- webhook delete     Delete a webhook by ID")
                print("- webhook say        Send messages via a webhook URL")
                print("- help               Show this help message")
                print("- exit               Exit the bot")

            elif cmd == "webhook create":
                server_id = (await self.async_input("Server ID: ")).strip()
                channel_id = (await self.async_input("Channel ID: ")).strip()

                guild = self.get_guild(int(server_id))
                if guild is None:
                    print("Guild not found.")
                    continue

                try:
                    channel = await self.fetch_channel(int(channel_id))
                except discord.NotFound:
                    print("Channel not found.")
                    continue

                if not isinstance(channel, discord.TextChannel):
                    print("This channel is not a text channel.")
                    continue

                webhook = await channel.create_webhook(name="᲼")

                webhook_data = {
                    "channel_id": str(channel.id),
                    "channel_name": channel.name,
                    "url": webhook.url,
                    "id": str(webhook.id)
                }

                db_data.setdefault("webhooks", {}).setdefault(server_id, []).append(webhook_data)
                save_data(db_data)

                print("Webhook created!")
                print(f"Channel: {channel.name} (ID: {channel.id})")
                print(f"URL: {webhook.url}")
                print(f"ID: {webhook.id}")

            elif cmd == "webhook show":
                server_id = (await self.async_input("Server ID: ")).strip()
                if server_id not in db_data.get("webhooks", {}) or not db_data["webhooks"][server_id]:
                    print("No webhooks for this server.")
                else:
                    for w in db_data["webhooks"][server_id]:
                        print(f"Webhook (Channel {w['channel_name']} | ID: {w['channel_id']}): {w['url']}, {w['id']}")

            elif cmd == "webhook delete":
                webhook_id = (await self.async_input("Webhook ID: ")).strip()
                found = False

                for server_id, webhooks in db_data.get("webhooks", {}).items():
                    for w in webhooks:
                        if w["id"] == webhook_id:
                            try:
                                url_parts = w["url"].rstrip("/").split("/")
                                wh_id = int(url_parts[-2])
                                wh_token = url_parts[-1]
                                webhook = await self.fetch_webhook(wh_id)
                                await webhook.delete()
                                print(f"Deleted webhook on Discord: {webhook_id}")
                            except discord.NotFound:
                                print("Webhook not found on Discord. Removing from local database anyway.")
                            except Exception as e:
                                print(f"Error deleting webhook on Discord: {e}")

                            webhooks.remove(w)
                            found = True
                            save_data(db_data)
                            print(f"Deleted webhook {webhook_id} from database.")
                            break
                    if found:
                        break

                if not found:
                    print("Webhook ID not found.")

            elif cmd == "webhook say":
                url = (await self.async_input("Webhook URL: ")).strip()
                print("Enter message. Type 'exit' to quit webhook say mode.")

                while True:
                    message = (await self.async_input("Message content: ")).strip()
                    if message.lower() == "exit":
                        print("Exiting webhook say mode.")
                        break

                    payload = {
                        "content": message
                    }
                    try:
                        resp = requests.post(url, json=payload)
                        if resp.status_code in (200, 204):
                            print("Message sent successfully!")
                        else:
                            print(f"Failed to send message. Status code: {resp.status_code}")
                            print("Response:", resp.text)
                    except Exception as e:
                        print(f"Error sending message: {e}")

            else:
                print("Unknown command. Type 'help' for a list of commands.")

with open("token.json", "r") as f:
    token_data = json.load(f)

intents = discord.Intents.default()
bot = MyBot(intents=intents)

bot.run(token_data["token"])
