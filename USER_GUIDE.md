# 📖 talAIt Bot - Complete User Guide

Welcome to talAIt! This guide will help you understand how to use the bot and participate in coding challenges.

## 🎯 Table of Contents
1. [Getting Started](#getting-started)
2. [For Members](#for-members)
3. [For Trainers](#for-trainers)
4. [For Admins](#for-admins)
5. [XP & Badges System](#xp--badges-system)
6. [FAQ](#faq)

---

## 🚀 Getting Started

### What is talAIt?
talAIt is a weekly coding challenge bot that helps you:
- Participate in coding challenges
- Track your progress with XP
- Compete on leaderboards
- Earn badges for achievements
- Improve your coding skills

### How It Works
1. **Every Friday at 8 PM**: New challenge posted in `#exercice`
2. **Submit**: Post your solution in `#code-wars-submissions`
3. **Review**: Trainers review and select top 3 winners
4. **Earn**: Get XP and badges based on your performance
5. **Compete**: Climb the monthly leaderboard!

---

## 👥 For Members

### Viewing the Leaderboard

```
/leaderboard
```
Shows the current month's top 10 performers with their XP and badges.

**Example Output:**
```
🏆 talAIt Monthly Leaderboard
2025-01

🥇 Alice - 45 XP | 🏅 3 badges
🥈 Bob - 32 XP | 🏅 2 badges
🥉 Charlie - 28 XP | 🏅 1 badge
```

### Checking Your Stats

```
/stats
```
or
```
/stats @username
```

View detailed statistics including:
- Current month XP
- Total XP (all-time)
- Current rank
- Badges earned
- Weeks participated

### Viewing Your Badges

```
/badges
```
or
```
/badges @username
```

See all badges you've earned:
- 🥇 Winner badges
- 🥈 2nd Place badges
- 🥉 3rd Place badges

### Viewing Hall of Fame

```
/halloffame
```

See all-time champions across all months. Shows:
- Total XP accumulated
- Number of months won
- Overall rankings

### Getting Help

```
/help
```
Shows all available commands and how to use them.

```
/about
```
Learn about the bot and its features.

### Participating in Challenges

#### Step 1: Read the Challenge
- Check `#exercice` every Friday at 8 PM
- Read the challenge requirements carefully
- Note the difficulty level

#### Step 2: Write Your Solution
- Code your solution in your preferred language
- Test it thoroughly
- Make sure it meets all requirements

#### Step 3: Submit
- Go to `#code-wars-submissions`
- Post your code with explanation
- Include:
  - Your approach
  - Time/space complexity (if applicable)
  - Any challenges you faced

#### Step 4: Wait for Results
- Trainers will review all submissions
- Winners announced usually within a week
- XP and badges awarded automatically

---

## 🎓 For Trainers

### Posting a Challenge

```
/postchallenge
```

**Parameters:**
- `title`: Challenge name (e.g., "Two Sum Problem")
- `description`: Detailed problem description
- `difficulty`: Easy, Medium, or Hard

**Example:**
```
/postchallenge
Title: Reverse a String
Description: Write a function that reverses a string without using built-in reverse methods
Difficulty: Easy
```

The bot will:
- Post challenge in `#exercice`
- Tag @everyone
- Track the challenge automatically

### Closing a Challenge

```
/closechallenge
```

Use this when:
- Submission deadline has passed
- Ready to review submissions
- Before announcing winners

This marks the challenge as closed and shows total submissions.

### Viewing Submissions

```
/submissions
```

Shows all submissions for the current challenge:
- User names
- Direct links to submissions
- Submission timestamps

**Tip**: Use this to review all entries before picking winners!

### Awarding Winners

```
/awardwinners
```

**Parameters:**
- `first`: @mention 1st place winner (required)
- `second`: @mention 2nd place winner (optional)
- `third`: @mention 3rd place winner (optional)

**Example:**
```
/awardwinners first:@Alice second:@Bob third:@Charlie
```

This automatically:
- Awards 10 XP to 1st place + 🥇 badge
- Awards 7 XP to 2nd place + 🥈 badge
- Awards 5 XP to 3rd place + 🥉 badge
- Announces winners publicly

### Giving Participation Points

```
/givepoints @user
```

Award 2 XP for participation to users who:
- Submitted but didn't win
- Showed good effort
- Participated actively

**Example:**
```
/givepoints @David
```

### Removing XP (Corrections)

```
/removexp @user [amount]
```

Use if you need to:
- Correct a mistake
- Remove improperly awarded XP

**Example:**
```
/removexp @User 5
```

### Listing All Users

```
/listusers
```

Shows all users in the leaderboard with their current XP.
Useful for:
- Checking who has participated
- Planning recognition
- Monitoring activity

---

## ⚙️ For Admins

### Manual Monthly Reset

```
/resetmonth
```

**Warning**: Only use if automatic reset fails!

This command:
- Saves current data to Hall of Fame
- Resets all monthly XP to 0
- Keeps total XP and badges
- Announces reset in server

**When to use:**
- Automatic reset didn't trigger
- Need to reset mid-month for special events
- Testing purposes

### Managing Roles

Ensure these roles exist and are assigned correctly:
- **Formateur**: Can post challenges, award XP
- **Admin**: Full control including reset
- **Moderator**: Can help manage submissions

### Channel Setup

Required channels:
- `#exercice` - Challenge posts
- `#code-wars-submissions` - User submissions

**Tips:**
- Set appropriate permissions
- Consider slow mode in submission channel
- Pin important announcements

---

## 🏆 XP & Badges System

### XP Breakdown

| Achievement | XP Earned | Badge |
|-------------|-----------|-------|
| 🥇 1st Place | 10 XP | 🥇 Winner WX |
| 🥈 2nd Place | 7 XP | 🥈 2nd Place WX |
| 🥉 3rd Place | 5 XP | 🥉 3rd Place WX |
| ✅ Participation | 2 XP | None |

*WX = Week Number*

### Monthly Leaderboard

- Resets every 1st of the month
- Top performers earn recognition
- Previous month saved to Hall of Fame
- Compete fresh each month!

### Hall of Fame

- Permanent record of all-time champions
- Shows cumulative performance
- Tracks months won
- Never resets!

### Badges

Badges are permanent achievements:
- Show on leaderboard
- Display in your stats
- Track your progress
- Earn recognition!

---

## ❓ FAQ

### Q: When are challenges posted?
**A:** Every Friday at 8:00 PM automatically. Trainers can also post manually anytime.

### Q: How do I submit my solution?
**A:** Post your code in `#code-wars-submissions` channel. The bot tracks it automatically!

### Q: When are winners announced?
**A:** Typically within a week after challenge closes. Trainers review all submissions first.

### Q: Can I participate in old challenges?
**A:** Challenges are weekly, but you can solve old ones for practice. Only current challenge counts for XP.

### Q: What happens to my XP each month?
**A:** Monthly XP resets to 0, but your Total XP and badges are permanent!

### Q: How do I check my rank?
**A:** Use `/stats` to see your current rank and XP.

### Q: Can I see other people's stats?
**A:** Yes! Use `/stats @username` to view anyone's public stats.

### Q: What if I miss a week?
**A:** No problem! Jump back in next week. Every challenge is a new opportunity!

### Q: How are winners chosen?
**A:** Trainers evaluate based on:
- Correctness
- Code quality
- Efficiency
- Creativity

### Q: Can I submit multiple times?
**A:** Yes, but only your latest submission will be considered.

### Q: What languages can I use?
**A:** Any programming language unless the challenge specifies otherwise!

### Q: How do I earn badges?
**A:** Win challenges! Each placement earns a unique badge.

### Q: Where can I see the Hall of Fame?
**A:** Use `/halloffame` to view all-time champions!

---

## 🎉 Tips for Success

### For Better Submissions
1. ✅ Write clean, readable code
2. ✅ Add comments explaining your logic
3. ✅ Test edge cases
4. ✅ Explain your approach
5. ✅ Consider time/space complexity

### For Climbing the Leaderboard
1. 📅 Participate consistently every week
2. 🎯 Focus on code quality, not just correctness
3. 💡 Try creative solutions
4. 📚 Learn from others' submissions
5. 🚀 Challenge yourself with harder problems

### For Community Building
1. 🤝 Help others learn
2. 💬 Discuss approaches (after submissions close)
3. 🎊 Congratulate winners
4. 📖 Share resources
5. 💪 Stay motivated!

---

## 📞 Support

Need help?
1. Use `/help` command
2. Ask in your server's help channel
3. Contact a trainer or admin
4. Check this guide again!

---

## 🎯 Quick Reference

**Most Used Commands:**
```
/leaderboard  - Check rankings
/stats        - View your stats
/help         - Get help
/badges       - View your badges
```

**For Trainers:**
```
/postchallenge  - Create challenge
/awardwinners   - Award top 3
/givepoints     - Give participation XP
```

---

**Happy Coding! 🚀**

---

*Last Updated: January 2025*
*Version: 1.0.0*