import json
import os
from datetime import datetime
from utils.constants import DATA_DIR, LEADERBOARD_FILE, HALL_OF_FAME_FILE, CHALLENGES_FILE

class DataManager:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.leaderboard_file = LEADERBOARD_FILE
        self.hall_of_fame_file = HALL_OF_FAME_FILE
        self.challenges_file = CHALLENGES_FILE
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.leaderboard = self._load_data(self.leaderboard_file)
        self.hall_of_fame = self._load_data(self.hall_of_fame_file)
        self.challenges = self._load_data(self.challenges_file)

    def _load_data(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {} if filename != self.challenges_file else []

    def _save_data(self, filename, data):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_month_key(self):
        now = datetime.now()
        return f"{now.year}-{now.month:02d}"

    def ensure_user(self, user_id, username):
        user_id = str(user_id)
        if user_id not in self.leaderboard:
            self.leaderboard[user_id] = {
                'username': username,
                'xp': 0,
                'weekly_xp': {},
                'total_xp': 0,
                'badges': []
            }
        else:
            self.leaderboard[user_id]['username'] = username
        self._save_data(self.leaderboard_file, self.leaderboard)

    def add_xp(self, user_id, amount, week_key):
        user_id = str(user_id)
        self.leaderboard[user_id]['xp'] += amount
        self.leaderboard[user_id]['total_xp'] += amount
        
        if week_key not in self.leaderboard[user_id]['weekly_xp']:
            self.leaderboard[user_id]['weekly_xp'][week_key] = 0
        self.leaderboard[user_id]['weekly_xp'][week_key] += amount
        
        self._save_data(self.leaderboard_file, self.leaderboard)

    def remove_xp(self, user_id, amount):
        user_id = str(user_id)
        self.leaderboard[user_id]['xp'] = max(0, self.leaderboard[user_id]['xp'] - amount)
        self._save_data(self.leaderboard_file, self.leaderboard)

    def add_badge(self, user_id, badge):
        user_id = str(user_id)
        if 'badges' not in self.leaderboard[user_id]:
            self.leaderboard[user_id]['badges'] = []
        if badge not in self.leaderboard[user_id]['badges']:
            self.leaderboard[user_id]['badges'].append(badge)
        self._save_data(self.leaderboard_file, self.leaderboard)

    def get_user(self, user_id):
        return self.leaderboard.get(str(user_id))

    def get_leaderboard(self):
        return self.leaderboard

    def get_hall_of_fame(self):
        return self.hall_of_fame

    def get_user_rank(self, user_id):
        sorted_users = sorted(self.leaderboard.items(), key=lambda x: x[1]['xp'], reverse=True)
        rank = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(user_id)), 0)
        return rank

    def reset_monthly_leaderboard(self):
        month_key = self.get_month_key()
        
        self.hall_of_fame[month_key] = dict(self.leaderboard)
        self._save_data(self.hall_of_fame_file, self.hall_of_fame)
        
        for user_id in self.leaderboard:
            self.leaderboard[user_id]['xp'] = 0
        
        self._save_data(self.leaderboard_file, self.leaderboard)

    # Challenge management
    def create_challenge(self, challenge_data):
        challenge_id = len(self.challenges) + 1
        challenge_data['id'] = challenge_id
        self.challenges.append(challenge_data)
        self._save_data(self.challenges_file, self.challenges)
        return challenge_id

    def update_challenge(self, challenge_id, updates):
        for challenge in self.challenges:
            if challenge['id'] == challenge_id:
                challenge.update(updates)
                self._save_data(self.challenges_file, self.challenges)
                return True
        return False

    def get_active_challenge(self):
        for challenge in reversed(self.challenges):
            if challenge.get('status') == 'active':
                return challenge
        return None

    def get_latest_challenge(self):
        return self.challenges[-1] if self.challenges else None

    def add_submission(self, challenge_id, submission_data):
        for challenge in self.challenges:
            if challenge['id'] == challenge_id:
                if 'submissions' not in challenge:
                    challenge['submissions'] = []
                challenge['submissions'].append(submission_data)
                self._save_data(self.challenges_file, self.challenges)
                return True
        return False