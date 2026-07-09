import discord
from discord import app_commands
from discord.ext import commands

from services.player_service import PlayerService


class Player(commands.GroupCog, group_name="player"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="add-discord",
        description="新增 Discord 玩家"
    )
    async def add_discord(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        success = await PlayerService.create_discord_player(
            name=member.display_name,
            discord_id=member.id,
            avatar=member.display_avatar.url
        )

        if success:

            embed = discord.Embed(
                title="✅ 玩家新增成功",
                color=discord.Color.green()
            )

            embed.add_field(
                name="玩家",
                value=member.mention,
                inline=False
            )

            embed.set_thumbnail(
                url=member.display_avatar.url
            )

        else:

            embed = discord.Embed(
                title="❌ 玩家已存在",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="add-name",
        description="新增一般玩家"
    )
    async def add_name(
        self,
        interaction: discord.Interaction,
        name: str
    ):

        success = await PlayerService.create_custom_player(name)

        if success:

            embed = discord.Embed(
                title="✅ 玩家新增成功",
                description=name,
                color=discord.Color.green()
            )

        else:

            embed = discord.Embed(
                title="❌ 玩家已存在",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="list",
        description="查看所有玩家"
    )
    async def player_list(
        self,
        interaction: discord.Interaction
    ):

        players = await PlayerService.get_all_players()

        if not players:

            await interaction.response.send_message(
                "目前沒有玩家。",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="👥 玩家列表",
            color=discord.Color.blue()
        )

        for player in players:

            if player.is_discord:
                text = f"Discord：{player.discord_id}"
            else:
                text = "一般玩家"

            embed.add_field(
                name=player.name,
                value=text,
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="remove",
        description="刪除玩家"
    )
    async def remove(
        self,
        interaction: discord.Interaction,
        player_id: int
    ):

        player = await PlayerService.get_player(player_id)

        if player is None:

            await interaction.response.send_message(
                "找不到玩家。",
                ephemeral=True
            )

            return

        await PlayerService.delete_player(player_id)

        await interaction.response.send_message(
            f"✅ 已刪除 **{player.name}**"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Player(bot))