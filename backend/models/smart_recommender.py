from typing import List, Dict, Any, Optional
from .ingredient_manager import Ingredient, IngredientManager

class MealRecommendation:
    def __init__(self, name: str, ingredients: List[Ingredient], 
                 total_calories: float, total_protein: float, 
                 total_carbs: float, total_fats: float):
        self.name = name
        self.ingredients = ingredients
        self.total_calories = total_calories
        self.total_protein = total_protein
        self.total_carbs = total_carbs
        self.total_fats = total_fats

class SmartMealRecommender:
    def __init__(self):
        self.ingredient_manager = IngredientManager()
        self.meal_templates = self._initialize_meal_templates()

    def _initialize_meal_templates(self) -> Dict[str, Dict]:
        """Initialize basic meal templates"""
        return {
            "high_protein": {
                "name": "High Protein Meal",
                "required_categories": ["Protein", "Vegetables"],
                "target_ratio": {"protein": 0.4, "carbs": 0.3, "fats": 0.3}
            },
            "balanced": {
                "name": "Balanced Meal", 
                "required_categories": ["Protein", "Carbohydrates", "Vegetables"],
                "target_ratio": {"protein": 0.3, "carbs": 0.4, "fats": 0.3}
            },
            "low_carb": {
                "name": "Low Carbohydrate Meal",
                "required_categories": ["Protein", "Vegetables", "Fats"],
                "target_ratio": {"protein": 0.4, "carbs": 0.2, "fats": 0.4}
            }
        }

    def recommend_meals(self, target_calories: int, preference: str = "balanced") -> List[MealRecommendation]:
        """Recommend meals based on calories and preferences"""
        available_ingredients = self.ingredient_manager.get_ingredients()
        template = self.meal_templates.get(preference, self.meal_templates["balanced"])
        
        recommendations = []
        
        # Breakfast
        breakfast = self._create_meal("Breakfast", available_ingredients, target_calories * 0.25, template)
        if breakfast:
            recommendations.append(breakfast)
        
        # Lunch
        lunch = self._create_meal("Lunch", available_ingredients, target_calories * 0.35, template)
        if lunch:
            recommendations.append(lunch)
        
        # Dinner
        dinner = self._create_meal("Dinner", available_ingredients, target_calories * 0.25, template)
        if dinner:
            recommendations.append(dinner)
        
        # Snack
        snack = self._create_meal("Snack", available_ingredients, target_calories * 0.15, template)
        if snack:
            recommendations.append(snack)
        
        return recommendations

    def _create_meal(self, meal_type: str, ingredients: List[Ingredient], 
                    target_calories: float, template: Dict) -> Optional[MealRecommendation]:
        """Create individual meal"""
        try:
            # Filter available ingredients
            available_ingredients = [ing for ing in ingredients if ing.quantity > 0]
            
            if not available_ingredients:
                return None
            
            # Select random ingredients for variety (in production use smart algorithms)
            import random
            selected_ingredients = random.sample(
                available_ingredients, 
                min(4, len(available_ingredients))
            )
            
            # Calculate total nutrition
            total_calories = sum(ing.calories or 0 for ing in selected_ingredients)
            total_protein = sum(ing.protein or 0 for ing in selected_ingredients)
            total_carbs = sum(ing.carbs or 0 for ing in selected_ingredients)
            total_fats = sum(ing.fats or 0 for ing in selected_ingredients)
            
            meal_name = f"{meal_type} {template['name']}"
            
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
        """Find recipes based on available ingredients"""
        available_ingredients = self.ingredient_manager.get_ingredients()
        available_names = [ing.name.lower() for ing in available_ingredients]
        
        matching_recipes = []
        
        # Sample recipes (in production use database)
        sample_recipes = [
            {
                "name": "Chicken Salad",
                "ingredients": ["Chicken", "Tomato", "Lettuce", "Olive Oil"],
                "calories": 320,
                "protein": 25,
                "carbs": 12,
                "fats": 18
            },
            {
                "name": "Chicken Rice",
                "ingredients": ["Rice", "Chicken", "Olive Oil"],
                "calories": 450,
                "protein": 30,
                "carbs": 45,
                "fats": 12
            },
            {
                "name": "Vegetable Salad",
                "ingredients": ["Tomato", "Lettuce", "Olive Oil"],
                "calories": 150,
                "protein": 2,
                "carbs": 10,
                "fats": 12
            }
        ]
        
        for recipe in sample_recipes:
            # Calculate match percentage
            matching_ingredients = [ing for ing in recipe["ingredients"] 
                                  if ing.lower() in available_names]
            match_percentage = len(matching_ingredients) / len(recipe["ingredients"])
            
            if match_percentage >= 0.5:  # At least 50% match
                recipe["match_percentage"] = round(match_percentage * 100)
                recipe["missing_ingredients"] = [ing for ing in recipe["ingredients"] 
                                               if ing.lower() not in available_names]
                matching_recipes.append(recipe)
        
        return sorted(matching_recipes, key=lambda x: x["match_percentage"], reverse=True)

    def get_meal_suggestions(self, available_ingredients: List[str]) -> List[Dict]:
        """Get meal suggestions based on available ingredients"""
        suggestions = []
        
        # Simple suggestion logic
        if "Chicken" in available_ingredients and "Rice" in available_ingredients:
            suggestions.append({
                "name": "Chicken with Rice",
                "description": "Simple and protein-rich meal",
                "calories": 400,
                "prep_time": "20 mins"
            })
        
        if "Tomato" in available_ingredients and "Lettuce" in available_ingredients:
            suggestions.append({
                "name": "Fresh Salad",
                "description": "Light and healthy salad",
                "calories": 150,
                "prep_time": "10 mins"
            })
        
        return suggestions