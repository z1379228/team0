import discord
from discord.ext import commands

import config
from services.database import Database


class TeamBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        print("========== 初始化 ==========")

        # 初始化資料庫
        await Database.initialize()

        # 載入所有 Cog
        extensions = [
            "cogs.player",
            "cogs.room",
            "cogs.team",
            "cogs.admin"
        ]

        for extension in extensions:

            try:
                await self.load_extension(extension)
                print(f"✅ 已載入 {extension}")

            except Exception as e:
                print(f"❌ 載入失敗 {extension}")
                print(e)

        # 同步 Slash Commands
        try:

            if config.GUILD_ID:

                guild = discord.Object(id=config.GUILD_ID)

                self.tree.copy_global_to(guild=guild)

                synced = await self.tree.sync(guild=guild)

            else:

                synced = await self.tree.sync()

            print(f"✅ 已同步 {len(synced)} 個 Slash Commands")

        except Exception as e:

            print("❌ Slash Command 同步失敗")
            print(e)

        print("============================")

    async def on_ready(self):

        print("============================")
        print(f"Bot：{self.user}")
        print(f"ID：{self.user.id}")
        print("============================")
        print("TeamBot 啟動成功")
        print("============================")


bot = TeamBot()

bot.run(config.TOKEN)