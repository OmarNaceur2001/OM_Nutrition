from datetime import datetime, timedelta
from typing import List, Dict

class NotificationSystem:
    def __init__(self):
        self.notifications = []
    
    def add_reminder(self, user_id: str, message: str, reminder_time: datetime):
        """Add reminder"""
        self.notifications.append({
            "user_id": user_id,
            "message": message,
            "time": reminder_time,
            "sent": False
        })
    
    def get_due_reminders(self, user_id: str) -> List[str]:
        """Get due reminders"""
        now = datetime.now()
        due_reminders = []
        
        for notification in self.notifications:
            if (notification["user_id"] == user_id and 
                not notification["sent"] and 
                notification["time"] <= now):
                due_reminders.append(notification["message"])
                notification["sent"] = True
        
        return due_reminders
    
    def create_meal_reminders(self, user_id: str, meal_times: List[str]):
        """Create meal reminders"""
        # Default reminders
        reminders = [
            "⏰ Time for Breakfast! Don't skip the most important meal of the day",
            "🍽️ Lunch Time! Maintain balanced meal",
            "🌙 Dinner Time! Choose light and healthy meal",
            "💧 Don't forget to drink water! Your target is 8 glasses today",
            "🏃 Time for workout! 30 minutes of activity"
        ]
        
        for reminder in reminders:
            self.add_reminder(user_id, reminder, datetime.now() + timedelta(hours=2))

    def create_shopping_reminders(self, user_id: str, low_ingredients: List[str]):
        """Create shopping reminders for low ingredients"""
        if low_ingredients:
            message = f"🛒 Time to shop! Low on: {', '.join(low_ingredients)}"
            self.add_reminder(user_id, message, datetime.now() + timedelta(hours=1))

    def get_all_reminders(self, user_id: str) -> List[Dict]:
        """Get all reminders for user"""
        user_reminders = [
            notif for notif in self.notifications 
            if notif["user_id"] == user_id
        ]
        return user_reminders

    def clear_sent_reminders(self, user_id: str):
        """Clear sent reminders for user"""
        self.notifications = [
            notif for notif in self.notifications 
            if not (notif["user_id"] == user_id and notif["sent"])
        ]