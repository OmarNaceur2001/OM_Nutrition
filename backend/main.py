from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="Nutrition AI Assistant")

# Add CORS to allow connection from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple data storage
ingredients_data = []
user_feedback = []

class UserInfo(BaseModel):
    weight: float
    height: float
    age: int
    gender: str
    activity: str

class IngredientRequest(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str

class FeedbackRequest(BaseModel):
    user_id: str
    recipe_name: str
    rating: int
    feedback: str = ""

@app.get("/")
def home():
    return {"message": "🎯 Nutrition AI Assistant is running!"}

@app.post("/calculate")
def calculate_calories(user: UserInfo):
    """Calorie Calculator"""
    try:
        if user.gender.lower() == "male":
            calories = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
        else:
            calories = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
        
        activity_multiplier = {
            "low": 1.2, "medium": 1.55, "high": 1.9
        }.get(user.activity, 1.2)
        
        daily_calories = calories * activity_multiplier
        
        return {
            "daily_calories": round(daily_calories),
            "protein_grams": round(daily_calories * 0.3 / 4),
            "carbs_grams": round(daily_calories * 0.4 / 4),
            "fat_grams": round(daily_calories * 0.3 / 9),
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Ingredients routes
@app.get("/ingredients")
def get_ingredients():
    """Get all ingredients"""
    return ingredients_data

@app.post("/ingredients")
def add_ingredient(ingredient: IngredientRequest):
    """Add new ingredient"""
    ingredients_data.append(ingredient.dict())
    return {"status": "success", "message": "Ingredient added successfully"}

@app.get("/recommend-meals")
def recommend_meals(target_calories: int, preference: str = "balanced"):
    """Recommend daily meals"""
    sample_meals = [
        {
            "name": "Balanced Breakfast",
            "ingredients": [
                {"name": "Oats", "quantity": 50, "unit": "grams"},
                {"name": "Milk", "quantity": 200, "unit": "ml"},
                {"name": "Banana", "quantity": 1, "unit": "piece"}
            ],
            "total_calories": 350,
            "total_protein": 15,
            "total_carbs": 60,
            "total_fats": 6
        },
        {
            "name": "Healthy Lunch", 
            "ingredients": [
                {"name": "Chicken", "quantity": 150, "unit": "grams"},
                {"name": "Rice", "quantity": 100, "unit": "grams"},
                {"name": "Vegetables", "quantity": 200, "unit": "grams"}
            ],
            "total_calories": 450,
            "total_protein": 35,
            "total_carbs": 50,
            "total_fats": 10
        }
    ]
    return {"meals": sample_meals}

@app.get("/find-recipes")
def find_recipes(ingredients: str = ""):
    """Find recipes based on ingredients"""
    sample_recipes = [
        {
            "name": "Chicken Salad",
            "ingredients": ["Chicken", "Tomato", "Lettuce", "Olive Oil"],
            "calories": 320,
            "protein": 25,
            "carbs": 12,
            "fats": 18,
            "match_percentage": 80
        },
        {
            "name": "Chicken Rice",
            "ingredients": ["Rice", "Chicken", "Olive Oil"],
            "calories": 450,
            "protein": 30,
            "carbs": 45,
            "fats": 12,
            "match_percentage": 75
        }
    ]
    return {"recipes": sample_recipes}

@app.get("/nutrition-tips")
def get_nutrition_tips(goal: str = "general"):
    """Customized nutrition tips"""
    tips = {
        "weight_loss": [
            "Drink water before meals to reduce appetite",
            "Focus on protein and vegetables",
            "Avoid sugary drinks",
            "Walk 30 minutes daily"
        ],
        "muscle_gain": [
            "Eat protein after workout",
            "Increase complex carbs for energy",
            "Don't neglect healthy fats",
            "Sleep 7-8 hours for recovery"
        ],
        "maintenance": [
            "Maintain meal variety",
            "Exercise 3-4 times weekly",
            "Eat vegetables and fruits daily",
            "Drink 2 liters of water"
        ],
        "general": [
            "Eat breakfast daily",
            "Use olive oil not processed oils",
            "Choose whole grains",
            "Reduce salt and sugar"
        ]
    }
    return {"tips": tips.get(goal, tips["general"])}

# Feedback system
@app.post("/feedback")
def add_user_feedback(feedback: FeedbackRequest):
    """Add user rating"""
    user_feedback.append(feedback.dict())
    return {"status": "success", "message": "Rating saved successfully"}

@app.get("/personalized-recipes/{user_id}")
def get_personalized_recipes(user_id: str):
    """Get personalized recommendations"""
    user_recipes = [fb for fb in user_feedback if fb["user_id"] == user_id and fb["rating"] >= 4]
    return {"recommendations": [fb["recipe_name"] for fb in user_recipes[:3]]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)