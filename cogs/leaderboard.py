import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from collections import defaultdict
from utils.constants import XP_VALUES

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = bot.data_manager

    @app_commands.command(name='addxp', description='Add XP to a user')
    @app_commands.describe(
        user='The user to add XP to',
        position='Position or participation (1st, 2nd, 3rd, participation)',
        week='Week number (optional, defaults to current week)'
    )
    async def add_xp(self, interaction: discord.Interaction, user: discord.Member, position: str, week: int = None):
        allowed_roles = ['formateur', 'admin', 'moderator']
        if not any(role.name.lower() in allowed_roles for role in interaction.user.roles):
            await interaction.response.send_message('❌ You do not have permission to use this command.', ephemeral=True)
            return
        
        position = position.lower()
        if position not in XP_VALUES:
            await interaction.response.send_message(
                f'❌ Invalid position. Use: 1st, 2nd, 3rd, or participation',
                ephemeral=True
            )
            return
        
        if week is None:
            week = datetime.now().isocalendar()[1]
        
        week_key = f"week_{week}"
        xp_amount = XP_VALUES[position]
        
        self.data_manager.ensure_user(user.id, user.name)
        self.data_manager.add_xp(user.id, xp_amount, week_key)
        
        user_data = self.data_manager.get_user(user.id)
        
        embed = discord.Embed(
            title='✅ XP Added!',
            description=f'{user.mention} received **{xp_amount} XP** for **{position}** place!',
            color=discord.Color.green()
        )
        embed.add_field(name='Current XP', value=f"{user_data['xp']} XP", inline=True)
        embed.add_field(name='Week', value=f"Week {week}", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='leaderboard', description='View the current monthly leaderboard')
    async def leaderboard_cmd(self, interaction: discord.Interaction):
        leaderboard = self.data_manager.get_leaderboard()
        
        if not leaderboard:
            await interaction.response.send_message('📊 The leaderboard is empty!')
            return
        
        sorted_users = sorted(leaderboard.items(), key=lambda x: x[1]['xp'], reverse=True)
        month_key = self.data_manager.get_month_key()
        
        embed = discord.Embed(
            title='🏆 talAIt Monthly Leaderboard',
            description=f'**{month_key}**',
            color=discord.Color.gold()
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        for idx, (user_id, data) in enumerate(sorted_users[:10]):
            medal = medals[idx] if idx < 3 else f'**{idx + 1}.**'
            username = data['username']
            xp = data['xp']
            embed.add_field(
                name=f'{medal} {username}',
                value=f'{xp} XP',
                inline=False
            )
        
        embed.set_footer(text='Updated monthly • Top 10 shown')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='halloffame', description='View the all-time Hall of Fame')
    async def hall_of_fame_cmd(self, interaction: discord.Interaction):
        hall_of_fame = self.data_manager.get_hall_of_fame()
        
        if not hall_of_fame:
            await interaction.response.send_message('🏛️ The Hall of Fame is empty!')
            return
        
        all_users = defaultdict(lambda: {'username': '', 'total_xp': 0})
        
        for month, users in hall_of_fame.items():
            for user_id, data in users.items():
                all_users[user_id]['username'] = data['username']
                all_users[user_id]['total_xp'] += data.get('xp', 0)
        
        sorted_users = sorted(all_users.items(), key=lambda x: x[1]['total_xp'], reverse=True)
        
        embed = discord.Embed(
            title='🏛️ Hall of Fame - All Time Champions',
            description='Top performers across all months',
            color=discord.Color.purple()
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        for idx, (user_id, data) in enumerate(sorted_users[:10]):
            medal = medals[idx] if idx < 3 else f'**{idx + 1}.**'
            username = data['username']
            xp = data['total_xp']
            embed.add_field(
                name=f'{medal} {username}',
                value=f'{xp} Total XP',
                inline=False
            )
        
        embed.set_footer(text='All-time rankings • Top 10 shown')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='stats', description='View your or another user\'s stats')
    @app_commands.describe(user='User to check stats for (optional)')
    async def stats(self, interaction: discord.Interaction, user: discord.Member = None):
        target_user = user or interaction.user
        user_data = self.data_manager.get_user(target_user.id)
        
        if not user_data:
            await interaction.response.send_message(
                f'❌ {target_user.mention} has no stats yet!',
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f'📊 Stats for {user_data["username"]}',
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Current Month XP', value=f'{user_data["xp"]} XP', inline=True)
        embed.add_field(name='Total XP', value=f'{user_data["total_xp"]} XP', inline=True)
        
        rank = self.data_manager.get_user_rank(target_user.id)
        embed.add_field(name='Current Rank', value=f'#{rank}', inline=True)
        
        if target_user.avatar:
            embed.set_thumbnail(url=target_user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))