import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
from utils.constants import ALLOWED_ROLES, EXERCISE_CHANNEL_NAME, SUBMISSION_CHANNEL_NAME
from utils.embeds import create_challenge_embed, create_submission_embed

class Challenges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = bot.data_manager
        self.auto_post_challenge.start()

    def cog_unload(self):
        self.auto_post_challenge.cancel()

    def has_trainer_role(self, interaction: discord.Interaction):
        return any(role.name.lower() in ALLOWED_ROLES for role in interaction.user.roles)

    @app_commands.command(name='postchallenge', description='Post a new weekly challenge')
    @app_commands.describe(
        title='Challenge title',
        description='Challenge description',
        difficulty='Difficulty level (Easy, Medium, Hard)'
    )
    async def post_challenge(self, interaction: discord.Interaction, title: str, description: str, difficulty: str = "Medium"):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('❌ Only trainers can post challenges!', ephemeral=True)
            return

        # Get exercise channel
        exercise_channel = discord.utils.get(interaction.guild.channels, name=EXERCISE_CHANNEL_NAME)
        if not exercise_channel:
            await interaction.response.send_message(
                f'❌ Please create a channel named `{EXERCISE_CHANNEL_NAME}` first!',
                ephemeral=True
            )
            return

        # Create challenge
        week_number = datetime.now().isocalendar()[1]
        challenge_data = {
            'title': title,
            'description': description,
            'difficulty': difficulty,
            'week': week_number,
            'posted_by': interaction.user.id,
            'posted_at': datetime.now().isoformat(),
            'status': 'active',
            'submissions': []
        }

        # Save challenge
        challenge_id = self.data_manager.create_challenge(challenge_data)

        # Post to channel
        embed = create_challenge_embed(title, description, difficulty, week_number, interaction.user)
        message = await exercise_channel.send(
            content="@everyone 🚨 **New Coding Challenge Posted!**",
            embed=embed
        )

        # Update challenge with message ID
        self.data_manager.update_challenge(challenge_id, {'message_id': message.id, 'channel_id': exercise_channel.id})

        await interaction.response.send_message(
            f'✅ Challenge posted successfully in {exercise_channel.mention}!',
            ephemeral=True
        )

    @app_commands.command(name='closechallenge', description='Close the current challenge and prepare for winners')
    async def close_challenge(self, interaction: discord.Interaction):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('❌ Only trainers can close challenges!', ephemeral=True)
            return

        active_challenge = self.data_manager.get_active_challenge()
        if not active_challenge:
            await interaction.response.send_message('❌ No active challenge to close!', ephemeral=True)
            return

        self.data_manager.update_challenge(active_challenge['id'], {'status': 'closed'})

        embed = discord.Embed(
            title='🏁 Challenge Closed!',
            description=f"**{active_challenge['title']}** is now closed for submissions.\n\nTrainers are reviewing submissions...",
            color=discord.Color.red()
        )
        embed.add_field(name='Total Submissions', value=str(len(active_challenge.get('submissions', []))), inline=True)
        embed.add_field(name='Week', value=f"Week {active_challenge['week']}", inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='awardwinners', description='Award XP to the top 3 winners')
    @app_commands.describe(
        first='1st place winner',
        second='2nd place winner (optional)',
        third='3rd place winner (optional)'
    )
    async def award_winners(self, interaction: discord.Interaction, first: discord.Member, second: discord.Member = None, third: discord.Member = None):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('❌ Only trainers can award winners!', ephemeral=True)
            return

        challenge = self.data_manager.get_active_challenge() or self.data_manager.get_latest_challenge()
        if not challenge:
            await interaction.response.send_message('❌ No challenge found!', ephemeral=True)
            return

        week_key = f"week_{challenge['week']}"
        winners = []

        # Award 1st place
        self.data_manager.ensure_user(first.id, first.name)
        self.data_manager.add_xp(first.id, 10, week_key)
        self.data_manager.add_badge(first.id, f"🥇 Winner W{challenge['week']}")
        winners.append(f"🥇 {first.mention} - **10 XP**")

        # Award 2nd place
        if second:
            self.data_manager.ensure_user(second.id, second.name)
            self.data_manager.add_xp(second.id, 7, week_key)
            self.data_manager.add_badge(second.id, f"🥈 2nd Place W{challenge['week']}")
            winners.append(f"🥈 {second.mention} - **7 XP**")

        # Award 3rd place
        if third:
            self.data_manager.ensure_user(third.id, third.name)
            self.data_manager.add_xp(third.id, 5, week_key)
            self.data_manager.add_badge(third.id, f"🥉 3rd Place W{challenge['week']}")
            winners.append(f"🥉 {third.mention} - **5 XP**")

        embed = discord.Embed(
            title='🎉 Winners Announced!',
            description=f"**{challenge['title']}** - Week {challenge['week']}\n\n" + "\n".join(winners),
            color=discord.Color.gold()
        )
        embed.set_footer(text='Congratulations to all winners! 🎊')

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='givepoints', description='Give participation points to a user')
    @app_commands.describe(user='User to give points to')
    async def give_points(self, interaction: discord.Interaction, user: discord.Member):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('❌ Only trainers can give points!', ephemeral=True)
            return

        challenge = self.data_manager.get_latest_challenge()
        week_key = f"week_{challenge['week']}" if challenge else f"week_{datetime.now().isocalendar()[1]}"

        self.data_manager.ensure_user(user.id, user.name)
        self.data_manager.add_xp(user.id, 2, week_key)

        await interaction.response.send_message(
            f'✅ Gave {user.mention} **2 participation points**!',
            ephemeral=True
        )

    @app_commands.command(name='submissions', description='List all submissions for the current challenge')
    async def list_submissions(self, interaction: discord.Interaction):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('❌ Only trainers can view submissions!', ephemeral=True)
            return

        challenge = self.data_manager.get_active_challenge() or self.data_manager.get_latest_challenge()
        if not challenge:
            await interaction.response.send_message('❌ No challenge found!', ephemeral=True)
            return

        submissions = challenge.get('submissions', [])
        if not submissions:
            await interaction.response.send_message('❌ No submissions yet!', ephemeral=True)
            return

        embed = discord.Embed(
            title=f'📝 Submissions for: {challenge["title"]}',
            description=f"Total submissions: **{len(submissions)}**",
            color=discord.Color.blue()
        )

        for idx, sub in enumerate(submissions[:25], 1):
            user = await self.bot.fetch_user(sub['user_id'])
            embed.add_field(
                name=f"{idx}. {user.name}",
                value=f"[View Submission](https://discord.com/channels/{interaction.guild_id}/{sub['channel_id']}/{sub['message_id']})",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.loop(hours=24)
    async def auto_post_challenge(self):
        now = datetime.now()
        
        # Check if it's Friday at 8 PM (20:00)
        if now.weekday() == 4 and now.hour == 20:
            for guild in self.bot.guilds:
                exercise_channel = discord.utils.get(guild.channels, name=EXERCISE_CHANNEL_NAME)
                if exercise_channel:
                    week_number = now.isocalendar()[1]
                    
                    embed = discord.Embed(
                        title='🚨 Weekly Challenge Time!',
                        description='A trainer will post this week\'s challenge soon!\n\nStay tuned! 🎯',
                        color=discord.Color.orange()
                    )
                    embed.add_field(name='Week', value=f"Week {week_number}", inline=True)
                    embed.set_footer(text='Use /postchallenge to create the challenge')
                    
                    await exercise_channel.send(content="@everyone", embed=embed)

    @auto_post_challenge.before_loop
    async def before_auto_post(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Track submissions in submission channel
        if message.channel.name == SUBMISSION_CHANNEL_NAME and not message.author.bot:
            active_challenge = self.data_manager.get_active_challenge()
            if active_challenge:
                submission_data = {
                    'user_id': message.author.id,
                    'message_id': message.id,
                    'channel_id': message.channel.id,
                    'submitted_at': datetime.now().isoformat()
                }
                self.data_manager.add_submission(active_challenge['id'], submission_data)
                
                # React to confirm
                await message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(Challenges(bot))