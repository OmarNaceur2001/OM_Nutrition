# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Nutrition AI Assistant",
    page_icon="🍎",
    layout="wide"
)

# Main title
st.title("🍎 Nutrition AI Assistant")
st.markdown("---")

# Function to call backend
def call_backend(endpoint, method="GET", data=None):
    base_url = "http://localhost:8000"
    try:
        if method == "GET":
            response = requests.get(f"{base_url}/{endpoint}", timeout=10)
        else:
            response = requests.post(f"{base_url}/{endpoint}", json=data, timeout=10)

        return response.json() if response.status_code == 200 else None

    except Exception as e:
        st.error(f"❌ Connection error: {e}")
        return None


# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Nutrition needs
    st.subheader("Your Nutrition Needs")

    with st.form("nutrition_needs"):
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
        age = st.number_input("Age", 10, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", [
            "Low (little movement)",
            "Medium (3-4 workouts/week)",
            "High (daily workouts)"
        ])

        calculate_needs = st.form_submit_button("Calculate Needs")

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
            st.success("✅ Nutrition needs calculated!")
        else:
            st.error("❌ Error calculating nutrition needs")


# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 My Needs", "🍽️ Ingredient Manager", "👨‍🍳 Smart Recommendations"])

# TAB 1 — HOME
with tab1:
    st.header("🎯 Welcome to the Nutrition AI Assistant!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Quick Overview")
        if "nutrition_needs" in st.session_state:
            needs = st.session_state.nutrition_needs
            st.metric("Daily Calories", f"{needs['daily_calories']} kcal")
            st.metric("Protein Needed", f"{needs['protein_grams']} g")
            st.metric("Carbs Needed", f"{needs['carbs_grams']} g")
            st.metric("Fat Needed", f"{needs['fat_grams']} g")
        else:
            st.info("⚠️ Please calculate your nutrition needs in the sidebar.")

    with col2:
        st.subheader("🚀 Available Features")
        st.success("✅ Calculate nutrition needs")
        st.success("✅ Manage available ingredients")
        st.success("✅ Smart meal recommendations")
        st.success("✅ Recipe suggestions")
        st.success("✅ Track ingredient availability")

# TAB 2 — MY NEEDS
with tab2:
    st.header("📊 Nutrition Needs Analysis")

    if "nutrition_needs" not in st.session_state:
        st.warning("⏳ Please calculate your nutrition needs first.")
    else:
        needs = st.session_state.nutrition_needs

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Macro Distribution")
            st.write(f"**Protein:** {needs['protein_grams']} g (30%)")
            st.progress(0.3)

            st.write(f"**Carbs:** {needs['carbs_grams']} g (40%)")
            st.progress(0.4)

            st.write(f"**Fats:** {needs['fat_grams']} g (30%)")
            st.progress(0.3)

        with col2:
            st.subheader("🎯 Nutrition Recommendations")
            st.info(f"**Daily Target:** {needs['daily_calories']} kcal")

            st.markdown("### 💡 Smart Tips:")

            if needs['daily_calories'] < 1800:
                st.write("• Focus on nutrient-dense foods")
                st.write("• Eat multiple small meals")
                st.write("• Choose lean protein sources")
            else:
                st.write("• Maintain balanced meals")
                st.write("• Vary protein and carb sources")
                st.write("• Don’t skip healthy fats")


# TAB 3 — INGREDIENT MANAGER
with tab3:
    st.header("🍽️ Ingredient Manager")

    col1, col2 = st.columns(2)

    # Add new ingredient
    with col1:
        st.subheader("➕ Add New Ingredient")

        with st.form("add_ingredient"):
            ing_name = st.text_input("Ingredient Name")
            ing_category = st.selectbox("Category", ["Protein", "Carbohydrates", "Fats", "Vegetables", "Fruits", "Dairy"])
            ing_quantity = st.number_input("Quantity", 0.0, 10000.0, 100.0)
            ing_unit = st.selectbox("Unit", ["g", "kg", "ml", "L", "piece"])

            if st.form_submit_button("Add Ingredient"):
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
                    else:
                        st.error("❌ Error adding ingredient")
                else:
                    st.warning("⚠️ Please enter ingredient name")

    # Show ingredients
    with col2:
        st.subheader("📋 Available Ingredients")

        ingredients = call_backend("ingredients")

        if ingredients:
            ing_data = []
            for ing in ingredients:
                ing_data.append({
                    "Ingredient": ing['name'],
                    "Category": ing['category'],
                    "Quantity": f"{ing['quantity']} {ing['unit']}"
                })

            df = pd.DataFrame(ing_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📝 No ingredients found")


# TAB 4 — SMART RECOMMENDATIONS
with tab4:
    st.header("👨‍🍳 Smart Meal Recommendations & Recipes")

    if "nutrition_needs" not in st.session_state:
        st.warning("⏳ Please calculate your nutrition needs first.")
    else:
        needs = st.session_state.nutrition_needs

        col1, col2 = st.columns(2)

        # Meal plan
        with col1:
            st.subheader("🍽️ Daily Meal Plan")

            preference = st.selectbox("Select Nutrition Style", [
                "Balanced", "High Protein", "Low Carb"
            ])

            if st.button("🎯 Generate Meal Plan"):
                pref_map = {
                    "Balanced": "balanced",
                    "High Protein": "high_protein",
                    "Low Carb": "low_carb"
                }

                meals = call_backend(
                    f"recommend-meals?target_calories={needs['daily_calories']}&preference={pref_map[preference]}"
                )

                if meals and "meals" in meals:
                    for i, meal in enumerate(meals["meals"]):
                        with st.expander(f"🍽️ {meal['name']} - {meal['total_calories']} kcal", expanded=i == 0):
                            st.write(f"**Nutrition:** ⚡ {meal['total_calories']} kcal | 🥩 {meal['total_protein']}g protein | 🌾 {meal['total_carbs']}g carbs | 🥑 {meal['total_fats']}g fats")
                            st.write("**Ingredients:**")
                            for ing in meal['ingredients']:
                                st.write(f"- {ing['name']} ({ing['quantity']} {ing['unit']})")
                else:
                    st.error("❌ No recommendations available")

        # Recipe search
        with col2:
            st.subheader("🔍 Search Recipes")

            search_ingredients = st.text_input("Enter Ingredients (comma separated)", "Chicken, Rice, Tomato")

            if st.button("👨‍🍳 Search"):
                if search_ingredients:
                    recipes = call_backend(f"find-recipes?ingredients={search_ingredients}")

                    if recipes and recipes['recipes']:
                        for recipe in recipes['recipes']:
                            with st.expander(f"🍳 {recipe['name']} - {recipe['match_percentage']}% match"):
                                st.write(f"**Calories:** {recipe['calories']} | **Protein:** {recipe['protein']}g")
                                st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
                    else:
                        st.info("🔍 No matching recipes found.")
                else:
                    st.warning("⚠️ Please enter ingredients to search.")


# Footer
st.markdown("---")
st.markdown("### 🎯 Nutrition AI Assistant")

