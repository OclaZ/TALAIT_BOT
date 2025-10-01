# talAIt Discord Leaderboard Bot

A Discord bot to manage weekly coding challenges, track XP, and maintain leaderboards for the talAIt community.

## Features

- 🏆 **XP System**: Award points for challenge positions (1st: 10 XP, 2nd: 7 XP, 3rd: 5 XP, Participation: 2 XP)
- 📊 **Monthly Leaderboard**: Track current month rankings
- 🏛️ **Hall of Fame**: Preserve all-time champion data
- 🔄 **Auto Reset**: Automatic monthly leaderboard reset
- 📈 **User Stats**: View detailed statistics for any user

## Commands

### User Commands
- `/leaderboard` - View current monthly rankings
- `/halloffame` - View all-time Hall of Fame
- `/stats [@user]` - Check your or another user's statistics

### Formateur/Admin Commands
- `/addxp @user [position] [week]` - Add XP to a user
- `/removexp @user [amount]` - Remove XP from a user

### Admin Only
- `/resetmonth` - Manually reset the monthly leaderboard

## Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
5. Copy the bot token

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your bot token:
```
DISCORD_TOKEN=your_actual_bot_token_here
```

### 4. Invite Bot to Server

1. In Developer Portal, go to OAuth2 → URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Read Messages/View Channels
   - Use Slash Commands
4. Copy the generated URL and open it to invite the bot

### 5. Run the Bot

```bash
python bot.py
```

## Project Structure

```
talait-bot/
│
├── bot.py                 # Main bot entry point
├── cogs/
│   ├── __init__.py
│   ├── leaderboard.py     # Leaderboard commands
│   └── admin.py           # Admin commands & auto-reset
├── utils/
│   ├── __init__.py
│   ├── data_manager.py    # Data persistence handler
│   └── constants.py       # Configuration constants
├── data/                  # Auto-generated data storage
│   ├── leaderboard.json
│   └── hall_of_fame.json
├── .env                   # Your configuration (create from .env.example)
├── .env.example           # Example configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuration

### Adjust Role Permissions

Edit `utils/constants.py` to change which roles can use admin commands:

```python
ALLOWED_ROLES = ['formateur', 'admin', 'moderator']
```

### Modify XP Values

Edit `utils/constants.py` to change XP rewards:

```python
XP_VALUES = {
    '1st': 10,
    '2nd': 7,
    '3rd': 5,
    'participation': 2
}
```

## Usage Examples

### Award XP
```
/addxp @username 1st
/addxp @username participation 12
```

### Check Rankings
```
/leaderboard
/halloffame
/stats
/stats @username
```

## Data Storage

All data is stored in JSON files in the `data/` directory:
- `leaderboard.json` - Current month data
- `hall_of_fame.json` - Historical monthly data

## Support

For issues or questions, contact the bot administrator or check the [Discord.py documentation](https://discordpy.readthedocs.io/).

## License

MIT License - Feel free to modify and use for your community!