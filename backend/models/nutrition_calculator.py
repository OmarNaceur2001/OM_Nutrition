from pydantic import BaseModel
from typing import Dict, List
import math

class UserProfile(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str

class NutritionCalculator:
    def __init__(self):
        self.activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        self.goal_multipliers = {
            "weight_loss": 0.8,
            "maintenance": 1.0,
            "muscle_gain": 1.2
        }

    def calculate_bmr(self, user: UserProfile) -> float:
        """Calculate Basal Metabolic Rate"""
        if user.gender.lower() == "male":
            bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
        else:
            bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)
        return bmr

    def calculate_tdee(self, user: UserProfile) -> float:
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr(user)
        activity_multiplier = self.activity_multipliers.get(user.activity_level, 1.2)
        goal_multiplier = self.goal_multipliers.get(user.goal, 1.0)
        
        tdee = bmr * activity_multiplier * goal_multiplier
        return round(tdee)

    def calculate_macros(self, user: UserProfile, tdee: float) -> Dict[str, float]:
        """Calculate Macronutrients distribution"""
        if user.goal == "weight_loss":
            protein_ratio = 0.4
            carb_ratio = 0.3
            fat_ratio = 0.3
        elif user.goal == "muscle_gain":
            protein_ratio = 0.35
            carb_ratio = 0.4
            fat_ratio = 0.25
        else:  # maintenance
            protein_ratio = 0.3
            carb_ratio = 0.4
            fat_ratio = 0.3

        # Calculate grams
        protein_cals = tdee * protein_ratio
        carb_cals = tdee * carb_ratio
        fat_cals = tdee * fat_ratio

        protein_grams = round(protein_cals / 4)
        carb_grams = round(carb_cals / 4)
        fat_grams = round(fat_cals / 9)

        return {
            "calories": tdee,
            "protein_grams": protein_grams,
            "carb_grams": carb_grams,
            "fat_grams": fat_grams,
            "protein_ratio": protein_ratio,
            "carb_ratio": carb_ratio,
            "fat_ratio": fat_ratio
        }

    def get_recommendations(self, user: UserProfile, macros: Dict) -> Dict:
        """Get personalized nutrition recommendations"""
        recommendations = {
            "daily_calories": f"Your daily target: {macros['calories']} calories",
            "protein": f"Protein: {macros['protein_grams']} grams ({macros['protein_ratio']*100}%)",
            "carbs": f"Carbohydrates: {macros['carb_grams']} grams ({macros['carb_ratio']*100}%)",
            "fats": f"Fats: {macros['fat_grams']} grams ({macros['fat_ratio']*100}%)"
        }
        
        # Add personalized tips
        if user.goal == "weight_loss":
            recommendations["tips"] = [
                "Focus on protein and fiber for satiety",
                "Drink water before meals",
                "Avoid sugary drinks"
            ]
        elif user.goal == "muscle_gain":
            recommendations["tips"] = [
                "Eat protein after workout",
                "Increase carbohydrates for energy",
                "Don't neglect healthy fats"
            ]
        else:
            recommendations["tips"] = [
                "Maintain balanced meals",
                "Diversify food sources",
                "Practice regular physical activity"
            ]
            
        return recommendations

    def calculate_water_intake(self, weight: float, activity_level: str) -> float:
        """Calculate daily water intake in liters"""
        base_water = weight * 0.033  # Base: 33ml per kg
        
        activity_adjustment = {
            "sedentary": 0,
            "light": 0.3,
            "moderate": 0.5,
            "active": 0.7,
            "very_active": 1.0
        }
        
        additional_water = activity_adjustment.get(activity_level, 0)
        total_water = base_water + additional_water
        
        return round(total_water, 1)