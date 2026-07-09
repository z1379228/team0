import discord
from discord import app_commands
from discord.ext import commands

from services.room_service import RoomService


class Room(commands.GroupCog, group_name="房間", group_description="房間管理"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="建立",
        description="建立目前頻道的房間"
    )
    async def create(
        self,
        interaction: discord.Interaction,
        名稱: str
    ):

        success = await RoomService.create_room(
            name=名稱,
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id,
            owner_id=interaction.user.id
        )

        if not success:
            await interaction.response.send_message(
                "❌ 此頻道已經有房間。",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="✅ 房間建立成功",
            color=discord.Color.green()
        )

        embed.add_field(
            name="房間名稱",
            value=名稱,
            inline=False
        )

        embed.add_field(
            name="建立者",
            value=interaction.user.mention,
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="刪除",
        description="刪除目前頻道的房間"
    )
    async def delete(
        self,
        interaction: discord.Interaction
    ):

        success = await RoomService.delete_room(
            interaction.channel.id
        )

        if not success:

            await interaction.response.send_message(
                "❌ 此頻道沒有房間。",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "✅ 房間已刪除。"
        )

    @app_commands.command(
        name="資訊",
        description="查看房間資訊"
    )
    async def info(
        self,
        interaction: discord.Interaction
    ):

        room = await RoomService.get_room_by_channel(
            interaction.channel.id
        )

        if room is None:

            await interaction.response.send_message(
                "❌ 此頻道尚未建立房間。",
                ephemeral=True
            )

            return

        players = await RoomService.get_players(room.id)

        embed = discord.Embed(
            title=f"🏠 {room.name}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="房主",
            value=f"<@{room.owner_id}>",
            inline=True
        )

        embed.add_field(
            name="狀態",
            value=room.status,
            inline=True
        )

        if players:

            text = "\n".join(
                f"• {player['name']}"
                for player in players
            )

        else:

            text = "目前沒有玩家"

        embed.add_field(
            name=f"玩家 ({len(players)}/10)",
            value=text,
            inline=False
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Room(bot))