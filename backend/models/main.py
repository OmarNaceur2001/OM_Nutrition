from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

# Initialize the FastAPI application
app = FastAPI(title="Nutrition AI Assistant")

# Define the data structure for user input using Pydantic
class UserInfo(BaseModel):
    weight: float  # Weight in kg
    height: float  # Height in cm
    age: int       # Age in years
    gender: str    # 'male' or 'female'
    activity: str  # 'low', 'medium', or 'high'

# Define the root endpoint
@app.get("/")
def home():
    """Root endpoint to confirm the assistant is running."""
    return {"message": "🎯 Nutrition AI Assistant is running!"}

# Define the calorie calculation endpoint
@app.post("/calculate")
def calculate_calories(user: UserInfo) -> Dict[str, int]:
    """Simple Calorie and Macronutrient Calculator based on Mifflin-St Jeor equation."""
    
    # Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    # (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + gender_factor
    if user.gender.lower() == "male":
        # BMR for men
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        # BMR for women
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
    
    # Determine the Activity Multiplier
    # Multipliers are based on general guidelines (e.g., low = Sedentary, medium = Moderately active, high = Very active)
    activity_multiplier = {
        "low": 1.2,      # Sedentary (little or no exercise)
        "medium": 1.55,  # Moderately Active (moderate exercise 3-5 days/week)
        "high": 1.9      # Very Active (hard exercise 6-7 days/week)
    }.get(user.activity.lower(), 1.2) # Default to 1.2 if activity is not recognized
    
    # Calculate Total Daily Energy Expenditure (TDEE)
    daily_calories = bmr * activity_multiplier
    
    # Calculate Macronutrient Split (example: 30% Protein, 40% Carbs, 30% Fat)
    # Energy conversion: Protein (4 cal/g), Carbs (4 cal/g), Fat (9 cal/g)
    
    protein_calories = daily_calories * 0.30
    carbs_calories = daily_calories * 0.40
    fat_calories = daily_calories * 0.30
    
    protein_grams = protein_calories / 4
    carbs_grams = carbs_calories / 4
    fat_grams = fat_calories / 9
    
    return {
        "daily_calories": round(daily_calories),
        "protein_grams": round(protein_grams),
        "carbs_grams": round(carbs_grams),
        "fat_grams": round(fat_grams)
    }