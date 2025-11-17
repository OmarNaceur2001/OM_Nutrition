# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Nutrition AI Assistant", 
    page_icon="🍎",
    layout="wide"
)

# Main title
st.title("🍎 Nutrition AI Assistant")
st.markdown("---")

# Initialize session state
if 'nutrition_needs' not in st.session_state:
    st.session_state.nutrition_needs = None
if 'ingredients_list' not in st.session_state:
    st.session_state.ingredients_list = []

# Function to call backend
def call_backend(endpoint, method="GET", data=None):
    base_url = "http://localhost:8000"
    try:
        if method == "GET":
            response = requests.get(f"{base_url}/{endpoint}", timeout=10)
        else:
            response = requests.post(f"{base_url}/{endpoint}", json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Server Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to server. Ensure Backend is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
        return None

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Calculate nutrition needs
    st.subheader("Your Nutrition Needs")
    with st.form("nutrition_needs_form"):
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="weight")
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")
        age = st.number_input("Age", 10, 100, 25, key="age")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        activity = st.selectbox("Activity Level", [
            "Low (little movement)",
            "Medium (3-4 workouts/week)", 
            "High (daily workouts)"
        ], key="activity")
        
        calculate_needs = st.form_submit_button("Calculate My Needs")
    
    if calculate_needs:
        activity_map = {
            "Low (little movement)": "low", 
            "Medium (3-4 workouts/week)": "medium", 
            "High (daily workouts)": "high"
        }
        user_data = {
            "weight": weight, 
            "height": height, 
            "age": age,
            "gender": "male" if gender == "Male" else "female",
            "activity": activity_map[activity]
        }
        
        result = call_backend("calculate", "POST", user_data)
        if result and result.get("status") == "success":
            st.session_state.nutrition_needs = result
            st.success("✅ Needs calculated successfully!")
        else:
            st.error("❌ Error in calculation")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 My Needs", "🍽️ Ingredient Manager", "👨‍🍳 Smart Recommendations"])

with tab1:
    st.header("🎯 Welcome to Nutrition AI Assistant!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Quick Overview")
        if st.session_state.nutrition_needs:
            needs = st.session_state.nutrition_needs
            st.metric("Daily Calories", f"{needs['daily_calories']} kcal")
            st.metric("Required Protein", f"{needs['protein_grams']} g")
            st.metric("Required Carbs", f"{needs['carbs_grams']} g")
            st.metric("Required Fats", f"{needs['fat_grams']} g")
        else:
            st.info("⚠️ Calculate your nutrition needs first from the sidebar")
    
    with col2:
        st.subheader("🚀 Available Features")
        st.success("✅ Calculate Nutrition Needs")
        st.success("✅ Manage Available Ingredients")
        st.success("✅ Smart Meal Recommendations")
        st.success("✅ Suggest Suitable Recipes")
        st.success("✅ Track Expired Ingredients")

with tab2:
    st.header("📊 Nutrition Needs Analysis")
    
    if not st.session_state.nutrition_needs:
        st.warning("⏳ Please calculate your nutrition needs first from the sidebar")
    else:
        needs = st.session_state.nutrition_needs
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Macronutrient Distribution")
            # Simple chart
            macros_data = {
                "Nutrients": ["Protein", "Carbs", "Fats"],
                "Grams": [needs['protein_grams'], needs['carbs_grams'], needs['fat_grams']]
            }
            df_macros = pd.DataFrame(macros_data)
            
            fig = px.pie(df_macros, values='Grams', names='Nutrients', 
                        title='Daily Macronutrient Distribution')
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("🎯 Nutrition Recommendations")
            st.info(f"**Daily Goal:** {needs['daily_calories']} calories")
            
            st.markdown("### 💡 Smart Tips:")
            if needs['daily_calories'] < 1800:
                st.write("• Focus on nutrient-dense foods")
                st.write("• Eat multiple small meals throughout the day")
                st.write("• Choose lean protein sources")
            else:
                st.write("• Maintain balance in your main meals")
                st.write("• Vary your protein and carbohydrate sources")
                st.write("• Don't neglect healthy fats")

with tab3:
    st.header("🍽️ Manage Available Ingredients")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Add New Ingredient")
        with st.form("add_ingredient_form"):
            ing_name = st.text_input("Ingredient Name", key="ing_name")
            ing_category = st.selectbox("Category", ["Protein", "Carbs", "Fats", "Vegetables", "Fruits", "Dairy"], key="ing_category")
            ing_quantity = st.number_input("Quantity", 0.0, 10000.0, 100.0, key="ing_quantity")
            ing_unit = st.selectbox("Unit", ["g", "kg", "ml", "l", "piece"], key="ing_unit")
            
            add_ingredient = st.form_submit_button("Add Ingredient")
        
        if add_ingredient:
            if ing_name:
                ingredient_data = {
                    "name": ing_name,
                    "category": ing_category,
                    "quantity": ing_quantity,
                    "unit": ing_unit
                }
                result = call_backend("ingredients", "POST", ingredient_data)
                if result:
                    st.success("✅ Ingredient added successfully!")
                    # Reload ingredients
                    st.session_state.ingredients_list = call_backend("ingredients") or []
                else:
                    st.error("❌ Error adding ingredient")
            else:
                st.warning("⚠️ Please enter an ingredient name")
    
    with col2:
        st.subheader("📋 Available Ingredients")
        # Load ingredients if not loaded
        if not st.session_state.ingredients_list:
            st.session_state.ingredients_list = call_backend("ingredients") or []
        
        ingredients = st.session_state.ingredients_list
        
        if ingredients:
            # Convert to DataFrame for better display
            ing_data = []
            for ing in ingredients:
                ing_data.append({
                    "Ingredient": ing['name'],
                    "Category": ing['category'],
                    "Quantity": f"{ing['quantity']} {ing['unit']}"
                })
            
            df = pd.DataFrame(ing_data)
            st.dataframe(df, width='stretch')
            
            # Refresh button
            if st.button("🔄 Refresh Ingredient List"):
                st.session_state.ingredients_list = call_backend("ingredients") or []
                st.rerun()
        else:
            st.info("📝 No ingredients registered yet")

with tab4:
    st.header("👨‍🍳 Smart Recommendations and Recipes")
    
    if not st.session_state.nutrition_needs:
        st.warning("⏳ Please calculate your nutrition needs first from the sidebar")
    else:
        needs = st.session_state.nutrition_needs
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🍽️ Daily Meal Plan")
            preference = st.selectbox("Choose your diet plan", [
                "Balanced", "High Protein", "Low Carb"
            ], key="preference")
            
            if st.button("🎯 Generate Meal Plan", key="generate_meals"):
                pref_map = {
                    "Balanced": "balanced", 
                    "High Protein": "high_protein", 
                    "Low Carb": "low_carb"
                }
                meals = call_backend(f"recommend-meals?target_calories={needs['daily_calories']}&preference={pref_map[preference]}")
                
                if meals and "meals" in meals:
                    for i, meal in enumerate(meals["meals"]):
                        with st.expander(f"🍽️ {meal['name']} - {meal['total_calories']} cal", expanded=i==0):
                            st.write(f"**Nutrition:** ⚡ {meal['total_calories']} cal | 🥩 {meal['total_protein']}g protein | 🌾 {meal['total_carbs']}g carbs | 🥑 {meal['total_fats']}g fats")
                            
                            st.write("**Ingredients:**")
                            for ing in meal['ingredients']:
                                st.write(f"- {ing['name']} ({ing['quantity']} {ing['unit']})")
                else:
                    st.error("❌ No recommendations available at the moment")
        
        with col2:
            st.subheader("🔍 Search Recipes")
            search_ingredients = st.text_input("Enter ingredients (comma separated)", "chicken, rice, tomato", key="search_ingredients")
            
            if st.button("👨‍🍳 Search Recipes", key="search_recipes"):
                if search_ingredients:
                    recipes = call_backend(f"find-recipes?ingredients={search_ingredients}")
                    
                    if recipes and recipes['recipes']:
                        for recipe in recipes['recipes']:
                            with st.expander(f"🍳 {recipe['name']} - {recipe['match_percentage']}% match"):
                                st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g")
                                st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
                    else:
                        st.info("🔍 No recipes match the ingredients")
                else:
                    st.warning("⚠️ Please enter some ingredients to search")

# Footer
st.markdown("---")
st.markdown("### 🎯 Nutrition AI Assistant")