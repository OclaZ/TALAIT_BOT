import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = bot.data_manager
        self.monthly_reset.start()

    def cog_unload(self):
        self.monthly_reset.cancel()

    @app_commands.command(name='removexp', description='Remove XP from a user')
    @app_commands.describe(user='The user to remove XP from', amount='Amount of XP to remove')
    async def remove_xp(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        allowed_roles = ['formateur', 'admin', 'moderator']
        if not any(role.name.lower() in allowed_roles for role in interaction.user.roles):
            await interaction.response.send_message('❌ You do not have permission to use this command.', ephemeral=True)
            return
        
        user_data = self.data_manager.get_user(user.id)
        
        if not user_data:
            await interaction.response.send_message('❌ User not found in leaderboard!', ephemeral=True)
            return
        
        self.data_manager.remove_xp(user.id, amount)
        updated_data = self.data_manager.get_user(user.id)
        
        await interaction.response.send_message(
            f'✅ Removed {amount} XP from {user.mention}. Current XP: {updated_data["xp"]}'
        )

    @app_commands.command(name='resetmonth', description='Manually reset the monthly leaderboard (Admin only)')
    async def reset_month(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message('❌ You must be an administrator to use this command.', ephemeral=True)
            return
        
        month_key = self.data_manager.get_month_key()
        self.data_manager.reset_monthly_leaderboard()
        
        await interaction.response.send_message(
            f'✅ Monthly leaderboard reset! Data saved to Hall of Fame for {month_key}'
        )

    @tasks.loop(hours=24)
    async def monthly_reset(self):
        now = datetime.now()
        
        if now.day == 1 and now.hour == 0:
            month_key = self.data_manager.get_month_key()
            self.data_manager.reset_monthly_leaderboard()
            
            print(f'✅ Monthly reset completed for {month_key}')

    @monthly_reset.before_loop
    async def before_monthly_reset(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Admin(bot))