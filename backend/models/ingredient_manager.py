from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os

# --- Pydantic Data Model ---
class Ingredient(BaseModel):
    """
    Defines the structure for a single ingredient item.
    """
    name: str
    category: str # e.g., 'Protein', 'Carbohydrate', 'Vegetable'
    quantity: float # Current stock quantity
    unit: str # e.g., 'grams', 'ml', 'pieces'
    expiration_date: Optional[str] = None # Date in 'YYYY-MM-DD' format
    calories: Optional[float] = None # Calories per 100g/ml/unit
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None

# --- Manager Class ---
class IngredientManager:
    """
    Manages a list of Ingredient objects, handling persistence via JSON files.
    NOTE: In a real-world app, this would typically use a database (like Firestore).
    """
    def __init__(self, data_file: str = "data/ingredients.json"):
        self.data_file = data_file
        self.ingredients: List[Ingredient] = []
        self.load_ingredients()

    def load_ingredients(self):
        """Loads ingredients from the JSON file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Create Pydantic Ingredient objects from the loaded data
                    self.ingredients = [Ingredient(**item) for item in data]
            else:
                # Initial dummy data if file does not exist
                self.ingredients = [
                    Ingredient(name="Chicken", category="Protein", quantity=500, unit="grams", calories=165, protein=31, carbs=0, fats=3.6),
                    Ingredient(name="Rice", category="Carbohydrate", quantity=1000, unit="grams", calories=130, protein=2.7, carbs=28, fats=0.3),
                    Ingredient(name="Olive Oil", category="Fat", quantity=250, unit="ml", calories=884, protein=0, carbs=0, fats=100),
                    Ingredient(name="Tomatoes", category="Vegetable", quantity=800, unit="grams", calories=18, protein=0.9, carbs=3.9, fats=0.2),
                ]
                self.save_ingredients()
        except Exception as e:
            # Handle potential loading errors (e.g., malformed JSON)
            print(f"Error loading ingredients: {e}")
            self.ingredients = []

    def save_ingredients(self):
        """Saves the current list of ingredients to the JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # Convert list of Pydantic models to list of dictionaries before saving
                json.dump([ingredient.dict() for ingredient in self.ingredients], 
                             f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving ingredients: {e}")

    def add_ingredient(self, ingredient: Ingredient) -> bool:
        """Adds a new ingredient to the list and saves the changes."""
        try:
            self.ingredients.append(ingredient)
            self.save_ingredients()
            return True
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False

    def get_ingredients(self) -> List[Ingredient]:
        """Returns all ingredients currently managed."""
        return self.ingredients

    def search_ingredients(self, query: str) -> List[Ingredient]:
        """
        Searches ingredients by name or category (case-insensitive).
        """
        query = query.lower()
        return [ing for ing in self.ingredients 
                if query in ing.name.lower() or query in ing.category.lower()]

    def get_low_quantity_ingredients(self, threshold: float = 200.0) -> List[Ingredient]:
        """
        Retrieves ingredients whose current quantity is at or below the specified threshold.
        """
        return [ing for ing in self.ingredients if ing.quantity <= threshold]