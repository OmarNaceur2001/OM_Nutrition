from typing import List, Dict, Any, Optional
from ingredient_manager import Ingredient, IngredientManager
import random

# --- Data Structure for a Recommended Meal ---
class MealRecommendation:
    """
    Holds the details and calculated macros for a single recommended meal.
    """
    def __init__(self, name: str, ingredients: List[Ingredient], 
                 total_calories: float, total_protein: float, 
                 total_carbs: float, total_fats: float):
        self.name = name
        self.ingredients = ingredients
        self.total_calories = total_calories
        self.total_protein = total_protein
        self.total_carbs = total_carbs
        self.total_fats = total_fats

# --- Main Recommender Logic ---
class SmartMealRecommender:
    """
    Recommends meals based on target calories, macronutrient preferences, 
    and available pantry ingredients.
    """
    def __init__(self):
        # Assumes IngredientManager is initialized and loaded
        self.ingredient_manager = IngredientManager()
        self.meal_templates = self._initialize_meal_templates()

    def _initialize_meal_templates(self) -> Dict[str, Dict]:
        """Initializes the base meal templates with required categories and macro ratios."""
        # Note: English categories should match the Ingredient class definitions (e.g., 'Protein')
        return {
            "high_protein": {
                "name": "High Protein Meal",
                "required_categories": ["Protein", "Vegetable"],
                "target_ratio": {"protein": 0.4, "carbs": 0.3, "fats": 0.3}
            },
            "balanced": {
                "name": "Balanced Meal", 
                "required_categories": ["Protein", "Carbohydrate", "Vegetable"],
                "target_ratio": {"protein": 0.3, "carbs": 0.4, "fats": 0.3}
            },
            "low_carb": {
                "name": "Low Carbohydrate Meal",
                "required_categories": ["Protein", "Vegetable", "Fat"],
                "target_ratio": {"protein": 0.4, "carbs": 0.2, "fats": 0.4}
            }
        }

    def recommend_meals(self, target_calories: int, preference: str = "balanced") -> List[MealRecommendation]:
        """
        Recommends a full day's worth of meals (Breakfast, Lunch, Dinner, Snack) 
        based on total calorie goal and preference.
        """
        available_ingredients = self.ingredient_manager.get_ingredients()
        # Select the template based on preference, defaulting to "balanced"
        template = self.meal_templates.get(preference, self.meal_templates["balanced"])
        
        recommendations = []
        
        # Split target calories across meals (e.g., 25% Breakfast, 35% Lunch, 25% Dinner, 15% Snack)
        
        # Breakfast (25% of daily calories)
        breakfast = self._create_meal("Breakfast", available_ingredients, target_calories * 0.25, template)
        if breakfast:
            recommendations.append(breakfast)
        
        # Lunch (35% of daily calories)
        lunch = self._create_meal("Lunch", available_ingredients, target_calories * 0.35, template)
        if lunch:
            recommendations.append(lunch)
        
        # Dinner (25% of daily calories)
        dinner = self._create_meal("Dinner", available_ingredients, target_calories * 0.25, template)
        if dinner:
            recommendations.append(dinner)
        
        # Snack (15% of daily calories)
        snack = self._create_meal("Snack", available_ingredients, target_calories * 0.15, template)
        if snack:
            recommendations.append(snack)
        
        return recommendations

    def _create_meal(self, meal_type: str, ingredients: List[Ingredient], 
                     target_calories: float, template: Dict) -> Optional[MealRecommendation]:
        """
        Internal method to generate a single meal recommendation.
        
        NOTE: This is a simplified approach (random selection) for demonstration. 
              A real system would use optimization algorithms to hit macro/calorie targets.
        """
        try:
            # Filter for ingredients that have some quantity available
            available_ingredients = [ing for ing in ingredients if (ing.quantity or 0) > 0]
            
            if not available_ingredients:
                return None
            
            # Simple Ingredient Selection: Take a few random items
            num_ingredients_to_select = min(4, len(available_ingredients))
            
            # Ensure we select ingredients that have nutritional data (calories, protein, etc.)
            ingredients_with_data = [ing for ing in available_ingredients if ing.calories is not None]

            if not ingredients_with_data:
                return None

            selected_ingredients = random.sample(
                ingredients_with_data, 
                min(num_ingredients_to_select, len(ingredients_with_data))
            )
            
            # Calculate total nutrition for the selected combination
            # In this simplified version, we just sum up the nutritional value 
            # as defined per unit in the Ingredient class (needs improvement in production).
            total_calories = sum(ing.calories or 0 for ing in selected_ingredients)
            total_protein = sum(ing.protein or 0 for ing in selected_ingredients)
            total_carbs = sum(ing.carbs or 0 for ing in selected_ingredients)
            total_fats = sum(ing.fats or 0 for ing in selected_ingredients)
            
            meal_name = f"{meal_type}: {template['name']}"
            
            return MealRecommendation(
                name=meal_name,
                ingredients=selected_ingredients,
                total_calories=round(total_calories, 1),
                total_protein=round(total_protein, 1),
                total_carbs=round(total_carbs, 1),
                total_fats=round(total_fats, 1)
            )
            
        except Exception as e:
            print(f"Error creating meal: {e}")
            return None

    def find_recipes_by_ingredients(self, ingredient_names: List[str]) -> List[Dict]:
        """
        Finds sample recipes that match the user's available ingredients.
        """
        # Get all currently managed ingredients to check availability
        available_ingredients = self.ingredient_manager.get_ingredients()
        available_names = [ing.name.lower() for ing in available_ingredients]
        
        matching_recipes = []
        
        # Hardcoded sample recipes (should come from a database in production)
        sample_recipes = [
            {
                "name": "Chicken Salad",
                "ingredients": ["Chicken", "Tomatoes", "Lettuce", "Olive Oil"],
                "calories": 320,
                "protein": 25,
                "carbs": 12,
                "fats": 18
            },
            {
                "name": "Chicken and Rice Bowl",
                "ingredients": ["Rice", "Chicken", "Olive Oil"],
                "calories": 450,
                "protein": 30,
                "carbs": 45,
                "fats": 12
            },
            {
                "name": "Simple Vegetable Salad",
                "ingredients": ["Tomatoes", "Lettuce", "Olive Oil"],
                "calories": 150,
                "protein": 2,
                "carbs": 10,
                "fats": 12
            }
        ]
        
        for recipe in sample_recipes:
            # Check how many ingredients in the recipe are available
            matching_ingredients = [ing for ing in recipe["ingredients"] 
                                  if ing.lower() in available_names]
            
            # Calculate match percentage
            match_percentage = len(matching_ingredients) / len(recipe["ingredients"])
            
            if match_percentage >= 0.5: # Require at least 50% match
                recipe["match_percentage"] = round(match_percentage * 100)
                recipe["missing_ingredients"] = [ing for ing in recipe["ingredients"] 
                                                if ing.lower() not in available_names]
                matching_recipes.append(recipe)
        
        # Sort results by the highest match percentage
        return sorted(matching_recipes, key=lambda x: x["match_percentage"], reverse=True)