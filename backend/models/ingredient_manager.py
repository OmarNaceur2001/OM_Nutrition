from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os

class Ingredient(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    expiration_date: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None

class IngredientManager:
    def __init__(self, data_file: str = "data/ingredients.json"):
        self.data_file = data_file
        self.ingredients: List[Ingredient] = []
        self.load_ingredients()

    def load_ingredients(self):
        """Load ingredients from JSON file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ingredients = [Ingredient(**item) for item in data]
            else:
                # Sample data for testing
                self.ingredients = [
                    Ingredient(name="Chicken", category="Protein", quantity=500, unit="grams", calories=165, protein=31, carbs=0, fats=3.6),
                    Ingredient(name="Rice", category="Carbohydrates", quantity=1000, unit="grams", calories=130, protein=2.7, carbs=28, fats=0.3),
                    Ingredient(name="Olive Oil", category="Fats", quantity=250, unit="ml", calories=884, protein=0, carbs=0, fats=100),
                    Ingredient(name="Tomato", category="Vegetables", quantity=800, unit="grams", calories=18, protein=0.9, carbs=3.9, fats=0.2),
                ]
                self.save_ingredients()
        except Exception as e:
            print(f"Error loading ingredients: {e}")
            self.ingredients = []

    def save_ingredients(self):
        """Save ingredients to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([ingredient.dict() for ingredient in self.ingredients], 
                         f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving ingredients: {e}")

    def add_ingredient(self, ingredient: Ingredient) -> bool:
        """Add new ingredient"""
        try:
            self.ingredients.append(ingredient)
            self.save_ingredients()
            return True
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False

    def get_ingredients(self) -> List[Ingredient]:
        """Get all ingredients"""
        return self.ingredients

    def search_ingredients(self, query: str) -> List[Ingredient]:
        """Search ingredients by name or category"""
        query = query.lower()
        return [ing for ing in self.ingredients 
                if query in ing.name.lower() or query in ing.category.lower()]

    def get_low_quantity_ingredients(self, threshold: float = 200.0) -> List[Ingredient]:
        """Get low quantity ingredients"""
        return [ing for ing in self.ingredients if ing.quantity <= threshold]

    def remove_ingredient(self, ingredient_name: str) -> bool:
        """Remove ingredient by name"""
        try:
            self.ingredients = [ing for ing in self.ingredients 
                              if ing.name.lower() != ingredient_name.lower()]
            self.save_ingredients()
            return True
        except Exception as e:
            print(f"Error removing ingredient: {e}")
            return False

    def get_expiring_soon(self, days: int = 3) -> List[Ingredient]:
        """Get ingredients expiring soon"""
        today = datetime.now()
        expiring = []
        
        for ingredient in self.ingredients:
            if ingredient.expiration_date:
                try:
                    exp_date = datetime.strptime(ingredient.expiration_date, "%Y-%m-%d")
                    if 0 <= (exp_date - today).days <= days:
                        expiring.append(ingredient)
                except ValueError:
                    continue
        
        return expiring