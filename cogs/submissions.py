import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.constants import ALLOWED_ROLES, SUBMISSIONS_CATEGORY_NAME
from utils.supabase_client import supabase

class Submissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = bot.data_manager

    def has_trainer_role(self, interaction: discord.Interaction):
        return any(role.name.lower() in ALLOWED_ROLES for role in interaction.user.roles)

    @app_commands.command(name='submit', description='Submit your code for the current challenge')
    @app_commands.describe(
        code='Your code solution (use code blocks)',
        language='Programming language used',
        notes='Optional notes about your submission'
    )
    async def submit_code(
        self,
        interaction: discord.Interaction,
        code: str,
        language: str = 'python',
        notes: str = None
    ):
        await interaction.response.defer(ephemeral=True)

        active_challenge = self.data_manager.get_active_challenge()
        if not active_challenge:
            await interaction.followup.send('No active challenge found!', ephemeral=True)
            return

        try:
            existing_submission = supabase.table('submissions')\
                .select('*')\
                .eq('challenge_id', active_challenge['id'])\
                .eq('user_id', str(interaction.user.id))\
                .maybeSingle()\
                .execute()

            if existing_submission.data:
                await interaction.followup.send(
                    'You have already submitted for this challenge! You can view your submission thread in the submissions category.',
                    ephemeral=True
                )
                return

            category = discord.utils.get(interaction.guild.categories, name=SUBMISSIONS_CATEGORY_NAME)
            if not category:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                category = await interaction.guild.create_category(
                    name=SUBMISSIONS_CATEGORY_NAME,
                    overwrites=overwrites
                )

            trainer_roles = [role for role in interaction.guild.roles if role.name.lower() in ALLOWED_ROLES]

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            for role in trainer_roles:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            thread_name = f"{interaction.user.name}-week{active_challenge['week']}"
            thread = await category.create_text_channel(
                name=thread_name,
                overwrites=overwrites
            )

            submission_data = {
                'challenge_id': active_challenge['id'],
                'user_id': str(interaction.user.id),
                'username': interaction.user.name,
                'code': code,
                'language': language,
                'notes': notes or '',
                'thread_id': str(thread.id),
                'status': 'pending'
            }

            result = supabase.table('submissions').insert(submission_data).execute()

            embed = discord.Embed(
                title=f"Submission for: {active_challenge['title']}",
                description=f"Week {active_challenge['week']} - {active_challenge['difficulty']}",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name='Submitted by', value=interaction.user.mention, inline=True)
            embed.add_field(name='Language', value=language.capitalize(), inline=True)
            embed.add_field(name='Status', value='Pending Review', inline=True)

            if notes:
                embed.add_field(name='Notes', value=notes, inline=False)

            embed.add_field(name='Code', value=f"```{language}\n{code[:1900]}\n```", inline=False)

            if len(code) > 1900:
                embed.set_footer(text='Code truncated - full code in following message')

            await thread.send(embed=embed)

            if len(code) > 1900:
                await thread.send(f"```{language}\n{code}\n```")

            await interaction.followup.send(
                f'Your submission has been recorded! A private thread has been created: {thread.mention}\n\nTrainers will review your submission there.',
                ephemeral=True
            )

            self.data_manager.add_submission(active_challenge['id'], {
                'user_id': interaction.user.id,
                'message_id': thread.id,
                'channel_id': thread.id,
                'submitted_at': datetime.now().isoformat()
            })

        except Exception as e:
            await interaction.followup.send(
                f'Error creating submission: {str(e)}',
                ephemeral=True
            )
            print(f'Submission error: {e}')

    @app_commands.command(name='viewsubmissions', description='View all submissions for the current challenge (Trainers only)')
    async def view_submissions(self, interaction: discord.Interaction):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('Only trainers can view all submissions!', ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        active_challenge = self.data_manager.get_active_challenge() or self.data_manager.get_latest_challenge()
        if not active_challenge:
            await interaction.followup.send('No challenge found!', ephemeral=True)
            return

        try:
            result = supabase.table('submissions')\
                .select('*')\
                .eq('challenge_id', active_challenge['id'])\
                .order('created_at', desc=False)\
                .execute()

            submissions = result.data

            if not submissions:
                await interaction.followup.send('No submissions yet for this challenge!', ephemeral=True)
                return

            embed = discord.Embed(
                title=f"Submissions for: {active_challenge['title']}",
                description=f"Week {active_challenge['week']} - Total: {len(submissions)} submissions",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            for idx, sub in enumerate(submissions[:25], 1):
                try:
                    user = await self.bot.fetch_user(int(sub['user_id']))
                    thread = interaction.guild.get_channel(int(sub['thread_id']))

                    status_emoji = {
                        'pending': '',
                        'reviewed': '',
                        'winner': ''
                    }.get(sub['status'], '')

                    thread_link = f"[View Thread]({thread.jump_url})" if thread else "Thread not found"

                    embed.add_field(
                        name=f"{idx}. {status_emoji} {user.name}",
                        value=f"Language: {sub['language']} | Status: {sub['status'].capitalize()}\n{thread_link}",
                        inline=False
                    )
                except:
                    continue

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f'Error fetching submissions: {str(e)}', ephemeral=True)
            print(f'Error fetching submissions: {e}')

    @app_commands.command(name='updatestatus', description='Update submission status (Trainers only)')
    @app_commands.describe(
        user='User whose submission to update',
        status='New status'
    )
    @app_commands.choices(status=[
        app_commands.Choice(name='Pending', value='pending'),
        app_commands.Choice(name='Reviewed', value='reviewed'),
        app_commands.Choice(name='Winner', value='winner')
    ])
    async def update_status(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        status: app_commands.Choice[str]
    ):
        if not self.has_trainer_role(interaction):
            await interaction.response.send_message('Only trainers can update submission status!', ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        active_challenge = self.data_manager.get_active_challenge() or self.data_manager.get_latest_challenge()
        if not active_challenge:
            await interaction.followup.send('No challenge found!', ephemeral=True)
            return

        try:
            result = supabase.table('submissions')\
                .update({'status': status.value, 'updated_at': datetime.now().isoformat()})\
                .eq('challenge_id', active_challenge['id'])\
                .eq('user_id', str(user.id))\
                .execute()

            if result.data:
                await interaction.followup.send(
                    f"Updated {user.mention}'s submission status to: **{status.name}**",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f'No submission found for {user.mention} in the current challenge.',
                    ephemeral=True
                )

        except Exception as e:
            await interaction.followup.send(f'Error updating status: {str(e)}', ephemeral=True)
            print(f'Error updating status: {e}')

async def setup(bot):
    await bot.add_cog(Submissions(bot))
