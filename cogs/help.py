import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Show all available commands and how to use the bot')
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='📚 talAIt Bot - Command Guide',
            description='Welcome to talAIt! Here are all available commands:',
            color=discord.Color.blue()
        )
        
        # Member Commands
        embed.add_field(
            name='👥 Member Commands',
            value=(
                '`/leaderboard` - View current monthly rankings\n'
                '`/halloffame` - View all-time champions\n'
                '`/stats [@user]` - View your or another user\'s stats\n'
                '`/badges [@user]` - View earned badges\n'
                '`/help` - Show this help message'
            ),
            inline=False
        )
        
        # Trainer Commands
        embed.add_field(
            name='🎓 Trainer Commands',
            value=(
                '`/postchallenge` - Post a new weekly challenge\n'
                '`/closechallenge` - Close current challenge\n'
                '`/awardwinners` - Award XP to top 3 winners\n'
                '`/givepoints @user` - Give participation points (2 XP)\n'
                '`/submissions` - List all challenge submissions\n'
                '`/listusers` - View all users in leaderboard\n'
                '`/removexp @user [amount]` - Remove XP from user'
            ),
            inline=False
        )
        
        # Admin Commands
        embed.add_field(
            name='⚙️ Admin Commands',
            value='`/resetmonth` - Manually reset monthly leaderboard',
            inline=False
        )
        
        # XP System
        embed.add_field(
            name='🏆 XP System',
            value=(
                '🥇 **1st Place:** 10 XP + Badge\n'
                '🥈 **2nd Place:** 7 XP + Badge\n'
                '🥉 **3rd Place:** 5 XP + Badge\n'
                '✅ **Participation:** 2 XP'
            ),
            inline=False
        )
        
        # How to Participate
        embed.add_field(
            name='📝 How to Participate',
            value=(
                '1️⃣ Check `#exercice` for weekly challenges (every Friday 8PM)\n'
                '2️⃣ Submit your solution in `#code-wars-submissions`\n'
                '3️⃣ Wait for trainers to review and award points\n'
                '4️⃣ Climb the leaderboard and earn badges! 🚀'
            ),
            inline=False
        )
        
        embed.set_footer(text='Need more help? Contact a trainer!')
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='about', description='Learn about talAIt and the bot')
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='ℹ️ About talAIt Bot',
            description=(
                '**talAIt** is your weekly coding challenge companion!\n\n'
                'We help you track challenges, manage submissions, '
                'award XP, and maintain leaderboards for your coding community.'
            ),
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name='📅 Weekly Schedule',
            value='New challenges every **Friday at 8:00 PM**',
            inline=False
        )
        
        embed.add_field(
            name='🔄 Monthly Reset',
            value='Leaderboards reset on the **1st of each month**\nPrevious data saved to Hall of Fame',
            inline=False
        )
        
        embed.add_field(
            name='🎯 Features',
            value=(
                '✅ Weekly challenge posting\n'
                '✅ Submission tracking\n'
                '✅ XP & badge system\n'
                '✅ Monthly leaderboards\n'
                '✅ Hall of Fame tracking'
            ),
            inline=False
        )
        
        embed.set_footer(text='Built with ❤️ for the talAIt community')
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))