import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.data_manager import DataManager

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize data manager
data_manager = DataManager()
bot.data_manager = data_manager



async def load_cogs():
    await bot.load_extension('cogs.leaderboard')
    await bot.load_extension('cogs.admin')
    print('✅ All cogs loaded successfully!')

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is now online!')
    print(f'📊 Bot ID: {bot.user.id}')
    print(f'🏠 Servers: {len(bot.guilds)}')
    print('='*50)
    
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="talAIt challenges | /help"
        )
    )

@bot.event
async def on_guild_join(guild):
    print(f'✅ Joined new server: {guild.name} (ID: {guild.id})')

async def load_cogs():
    await bot.load_extension('cogs.challenges')
    await bot.load_extension('cogs.leaderboard')
    await bot.load_extension('cogs.admin')
    await bot.load_extension('cogs.help')
    print('✅ All cogs loaded successfully!')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())