import asyncio
import discord
from discord.ext import commands

import config
from services.database import Database


class TeamBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        print("========== 初始化 ==========")

        # 初始化資料庫
        await Database.initialize()

        # 載入所有 Cog
        cogs = [
            "cogs.player",
            "cogs.team",
            "cogs.admin"
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ 已載入 {cog}")
            except Exception as e:
                print(f"❌ 載入失敗 {cog}")
                print(e)

        # 同步 Slash Commands
        try:
            guild = discord.Object(id=config.GUILD_ID)

            self.tree.copy_global_to(guild=guild)

            synced = await self.tree.sync(guild=guild)

            print(f"✅ 已同步 {len(synced)} 個 Slash Commands")

        except Exception as e:
            print("❌ Slash 同步失敗")
            print(e)

        print("============================")

    async def on_ready(self):

        print()
        print("============================")
        print(f"Bot：{self.user}")
        print(f"ID：{self.user.id}")
        print("============================")
        print("TeamBot 啟動成功")
        print("============================")


async def main():

    bot = TeamBot()

    async with bot:
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())