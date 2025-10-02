from fastapi import FastAPI
from utils.data_manager import DataManager

app = FastAPI(title="TalAIt Bot API", version="1.0.0")

# Use the same DataManager as your bot
data_manager = DataManager()

@app.get("/")
def home():
    return {"message": "🚀 TalAIt Bot API running on Vercel!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/leaderboard")
def get_leaderboard():
    """Return leaderboard data"""
    if hasattr(data_manager, "get_leaderboard"):
        leaderboard_data = data_manager.get_leaderboard()
        return {"leaderboard": leaderboard_data}
    return {"error": "Leaderboard method not found in DataManager"}

@app.get("/hall_of_fame")
def get_hall_of_fame():
    """Return hall of fame data"""
    if hasattr(data_manager, "get_hall_of_fame"):
        hof_data = data_manager.get_hall_of_fame()
        return {"hall_of_fame": hof_data}
    return {"error": "Hall of Fame method not found in DataManager"}
