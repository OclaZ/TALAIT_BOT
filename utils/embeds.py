import discord
from datetime import datetime

def create_challenge_embed(title, description, difficulty, week, posted_by):
    color_map = {
        'easy': discord.Color.green(),
        'medium': discord.Color.orange(),
        'hard': discord.Color.red()
    }
    
    embed = discord.Embed(
        title=f'🎯 {title}',
        description=description,
        color=color_map.get(difficulty.lower(), discord.Color.blue())
    )
    
    embed.add_field(name='📊 Difficulty', value=difficulty, inline=True)
    embed.add_field(name='📅 Week', value=f'Week {week}', inline=True)
    embed.add_field(name='👤 Posted by', value=posted_by.mention, inline=True)
    
    embed.add_field(
        name='📝 How to Submit',
        value=f'Post your solution in `#code-wars-submissions`',
        inline=False
    )
    
    embed.add_field(
        name='🏆 Rewards',
        value='🥇 1st: 10 XP\n🥈 2nd: 7 XP\n🥉 3rd: 5 XP\n✅ Participation: 2 XP',
        inline=False
    )
    
    embed.set_footer(text=f'Posted on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}')
    embed.timestamp = datetime.now()
    
    return embed

def create_submission_embed(user, challenge_title):
    embed = discord.Embed(
        title='✅ Submission Received!',
        description=f'Your submission for **{challenge_title}** has been recorded.',
        color=discord.Color.green()
    )
    embed.set_footer(text='Trainers will review your submission soon!')
    return embed

def create_leaderboard_embed(sorted_users, month_key):
    embed = discord.Embed(
        title='🏆 talAIt Monthly Leaderboard',
        description=f'**{month_key}**',
        color=discord.Color.gold()
    )
    
    medals = ['🥇', '🥈', '🥉']
    
    for idx, (user_id, data) in enumerate(sorted_users):
        medal = medals[idx] if idx < 3 else f'**{idx + 1}.**'
        username = data['username']
        xp = data['xp']
        
        badge_count = len(data.get('badges', []))
        badge_text = f' | 🏅 {badge_count} badges' if badge_count > 0 else ''
        
        embed.add_field(
            name=f'{medal} {username}',
            value=f'{xp} XP{badge_text}',
            inline=False
        )
    
    embed.set_footer(text='Updated monthly • Top 10 shown')
    embed.timestamp = datetime.now()
    
    return embed

def create_stats_embed(user_data, rank, discord_user):
    embed = discord.Embed(
        title=f'📊 Stats for {user_data["username"]}',
        color=discord.Color.blue()
    )
    
    embed.add_field(name='Current Month XP', value=f'{user_data["xp"]} XP', inline=True)
    embed.add_field(name='Total XP', value=f'{user_data["total_xp"]} XP', inline=True)
    embed.add_field(name='Current Rank', value=f'#{rank}', inline=True)
    
    badges = user_data.get('badges', [])
    embed.add_field(name='Badges Earned', value=str(len(badges)), inline=True)
    
    weekly_xp = user_data.get('weekly_xp', {})
    embed.add_field(name='Weeks Participated', value=str(len(weekly_xp)), inline=True)
    
    if discord_user.avatar:
        embed.set_thumbnail(url=discord_user.avatar.url)
    
    embed.timestamp = datetime.now()
    
    return embed