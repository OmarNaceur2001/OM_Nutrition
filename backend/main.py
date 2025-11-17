# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add models directory to path
sys.path.insert(0, str(Path(__file__).parent / 'models'))

from ingredient_manager import Ingredient, IngredientManager
from smart_recommender import SmartMealRecommender, MealRecommendation

app = FastAPI(title="Nutrition AI Assistant")

# إضافة CORS للسماح بالاتصال من Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة المديرين
ingredient_manager = IngredientManager()
meal_recommender = SmartMealRecommender()

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
    expiration_date: Optional[str] = None

@app.get("/")
def home():
    return {"message": "🎯 Nutrition AI Assistant is running!"}

@app.post("/calculate")
def calculate_calories(user: UserInfo):
    """حاسبة السعرات الحرارية"""
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

# ⭐ ⭐ ⭐ المسارات الجديدة ⭐ ⭐ ⭐

@app.get("/ingredients")
def get_ingredients():
    """الحصول على جميع المكونات"""
    return ingredient_manager.get_ingredients()

@app.post("/ingredients")
def add_ingredient(ingredient: IngredientRequest):
    """إضافة مكون جديد"""
    ingredient_obj = Ingredient(**ingredient.dict())
    success = ingredient_manager.add_ingredient(ingredient_obj)
    return {"status": "success" if success else "error"}

@app.get("/recommend-meals")
def recommend_meals(target_calories: int, preference: str = "balanced"):
    """توصية بوجبات يومية"""
    recommendations = meal_recommender.recommend_meals(target_calories, preference)
    
    # تحويل إلى JSON قابل للتserialization
    meals_data = []
    for meal in recommendations:
        meals_data.append({
            "name": meal.name,
            "ingredients": [ing.dict() for ing in meal.ingredients],
            "total_calories": meal.total_calories,
            "total_protein": meal.total_protein,
            "total_carbs": meal.total_carbs,
            "total_fats": meal.total_fats
        })
    
    return {"meals": meals_data}

@app.get("/find-recipes")
def find_recipes(ingredients: str = ""):
    """إيجاد وصفات بناءً على المكونات"""
    ingredient_list = [ing.strip() for ing in ingredients.split(",")] if ingredients else []
    recipes = meal_recommender.find_recipes_by_ingredients(ingredient_list)
    return {"recipes": recipes}

@app.get("/low-quantity")
def get_low_quantity_ingredients():
    """الحصول على المكونات المنخفضة الكمية"""
    low_quantity = ingredient_manager.get_low_quantity_ingredients()
    return {"ingredients": [ing.dict() for ing in low_quantity]}