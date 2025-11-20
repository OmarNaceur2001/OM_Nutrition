from typing import Dict, List
import json
import os

class MLRecommendationSystem:
    def __init__(self):
        self.user_preferences = {}
        self.feedback_file = "data/user_feedback.json"
        self.load_feedback()
    
    def load_feedback(self):
        """Load user preferences"""
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.user_preferences = json.load(f)
        except:
            self.user_preferences = {}
    
    def save_feedback(self):
        """Save user preferences"""
        try:
            os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
    def add_feedback(self, user_id: str, recipe_name: str, rating: int, feedback_text: str = ""):
        """Add user rating"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = []
        
        self.user_preferences[user_id].append({
            "recipe": recipe_name,
            "rating": rating,
            "feedback": feedback_text,
            "timestamp": "2024-01-01"  # Simplified without datetime
        })
        self.save_feedback()
    
    def get_personalized_recommendations(self, user_id: str, available_ingredients: List[str]):
        """Personalized recommendations based on preferences"""
        user_feedback = self.user_preferences.get(user_id, [])
        
        if not user_feedback:
            return []  # Not enough data
        
        # Analyze preferences (simplified example)
        high_rated_recipes = [
            fb["recipe"] for fb in user_feedback 
            if fb["rating"] >= 4
        ]
        
        return high_rated_recipes[:3]  # Top 3 favorite recipes

    def get_user_preferences_summary(self, user_id: str) -> Dict:
        """Get summary of user preferences"""
        user_feedback = self.user_preferences.get(user_id, [])
        
        if not user_feedback:
            return {"message": "No preferences data available"}
        
        total_ratings = len(user_feedback)
        average_rating = sum(fb["rating"] for fb in user_feedback) / total_ratings
        favorite_recipes = [fb["recipe"] for fb in user_feedback if fb["rating"] >= 4]
        
        return {
            "total_ratings": total_ratings,
            "average_rating": round(average_rating, 2),
            "favorite_recipes": favorite_recipes[:5],
            "preferred_categories": self._analyze_preferred_categories(user_feedback)
        }
    
    def _analyze_preferred_categories(self, user_feedback: List[Dict]) -> List[str]:
        """Analyze user's preferred food categories"""
        # Simplified category analysis
        categories = []
        for feedback in user_feedback:
            recipe_name = feedback["recipe"].lower()
            if "chicken" in recipe_name:
                categories.append("Protein")
            elif "salad" in recipe_name:
                categories.append("Vegetables")
            elif "rice" in recipe_name:
                categories.append("Carbohydrates")
        
        # Return unique categories
        return list(set(categories))