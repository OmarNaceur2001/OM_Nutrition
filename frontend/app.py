import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="Nutrition AI Assistant", 
    page_icon="🍎",
    layout="wide"
)

# Main title
st.title("🍎 Smart Nutrition Assistant")
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
            return None
    except Exception as e:
        st.error(f"❌ Connection error: {e}")
        return None

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Nutrition needs calculation
    st.subheader("Your Nutrition Needs")
    with st.form("nutrition_needs_form"):
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
        age = st.number_input("Age", 10, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", [
            "Low (Sedentary)",
            "Medium (Exercise 3-4 times/week)", 
            "High (Daily exercise)"
        ])
        
        calculate_needs = st.form_submit_button("Calculate My Needs")
    
    if calculate_needs:
        activity_map = {
            "Low (Sedentary)": "low", 
            "Medium (Exercise 3-4 times/week)": "medium", 
            "High (Daily exercise)": "high"
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
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 My Needs", "🍽️ Ingredients", "👨‍🍳 Recommendations"])

with tab1:
    st.header("🎯 Welcome to Smart Nutrition Assistant!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Quick Overview")
        if st.session_state.nutrition_needs:
            needs = st.session_state.nutrition_needs
            st.metric("Daily Calories", f"{needs['daily_calories']} kcal")
            st.metric("Protein Required", f"{needs['protein_grams']} g")
            st.metric("Carbs Required", f"{needs['carbs_grams']} g")
            st.metric("Fats Required", f"{needs['fat_grams']} g")
        else:
            st.info("⚠️ Calculate your nutrition needs first from sidebar")
    
    with col2:
        st.subheader("🚀 Available Features")
        st.success("✅ Calculate nutrition needs")
        st.success("✅ Manage ingredients")
        st.success("✅ Meal recommendations")
        st.success("✅ Recipe suggestions")
        st.success("✅ Nutrition tips")

with tab2:
    st.header("📊 Nutrition Needs Analysis")
    
    if not st.session_state.nutrition_needs:
        st.warning("⏳ Calculate your nutrition needs first from sidebar")
    else:
        needs = st.session_state.nutrition_needs
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Macronutrients Distribution")
            macros_data = {
                "Nutrients": ["Protein", "Carbs", "Fats"],
                "Grams": [needs['protein_grams'], needs['carbs_grams'], needs['fat_grams']]
            }
            df_macros = pd.DataFrame(macros_data)
            
            fig = px.pie(df_macros, values='Grams', names='Nutrients', 
                        title='Daily Macronutrients Distribution')
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("🎯 Nutrition Recommendations")
            st.info(f"**Daily Target:** {needs['daily_calories']} calories")
            
            st.markdown("### 💡 Smart Tips:")
            if needs['daily_calories'] < 1800:
                st.write("• Focus on nutrient-dense foods")
                st.write("• Eat small frequent meals")
                st.write("• Choose lean protein sources")
            else:
                st.write("• Maintain balanced meals")
                st.write("• Diversify food sources")
                st.write("• Include healthy fats")

with tab3:
    st.header("🍽️ Ingredients Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Add New Ingredient")
        with st.form("add_ingredient_form"):
            ing_name = st.text_input("Ingredient Name")
            ing_category = st.selectbox("Category", ["Protein", "Carbs", "Fats", "Vegetables", "Fruits", "Dairy"])
            ing_quantity = st.number_input("Quantity", 0.0, 10000.0, 100.0)
            ing_unit = st.selectbox("Unit", ["grams", "kg", "ml", "liter", "piece"])
            
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
                    st.session_state.ingredients_list = call_backend("ingredients") or []
                else:
                    st.error("❌ Error adding ingredient")
            else:
                st.warning("⚠️ Please enter ingredient name")
    
    with col2:
        st.subheader("📋 Available Ingredients")
        if not st.session_state.ingredients_list:
            st.session_state.ingredients_list = call_backend("ingredients") or []
        
        ingredients = st.session_state.ingredients_list
        
        if ingredients:
            ing_data = []
            for ing in ingredients:
                ing_data.append({
                    "Ingredient": ing['name'],
                    "Category": ing['category'],
                    "Quantity": f"{ing['quantity']} {ing['unit']}"
                })
            
            df = pd.DataFrame(ing_data)
            st.dataframe(df, width=1000)
            
            if st.button("🔄 Refresh List"):
                st.session_state.ingredients_list = call_backend("ingredients") or []
                st.rerun()
        else:
            st.info("📝 No ingredients registered yet")

with tab4:
    st.header("👨‍🍳 Smart Recommendations")
    
    if not st.session_state.nutrition_needs:
        st.warning("⏳ Calculate your nutrition needs first from sidebar")
    else:
        needs = st.session_state.nutrition_needs
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🍽️ Daily Meal Plan")
            preference = st.selectbox("Choose Nutrition Plan", [
                "Balanced", "High Protein", "Low Carbs"
            ])
            
            if st.button("🎯 Generate Meal Plan"):
                pref_map = {
                    "Balanced": "balanced", 
                    "High Protein": "high_protein", 
                    "Low Carbs": "low_carb"
                }
                meals = call_backend(f"recommend-meals?target_calories={needs['daily_calories']}&preference={pref_map[preference]}")
                
                if meals and "meals" in meals:
                    for meal in meals["meals"]:
                        with st.expander(f"🍽️ {meal['name']} - {meal['total_calories']} cal"):
                            st.write(f"**Nutrition:** {meal['total_calories']} cal | {meal['total_protein']}g protein | {meal['total_carbs']}g carbs | {meal['total_fats']}g fats")
                            st.write("**Ingredients:**")
                            for ing in meal['ingredients']:
                                st.write(f"- {ing['name']} ({ing['quantity']} {ing['unit']})")
                else:
                    st.error("❌ No recommendations available")
        
        with col2:
            st.subheader("💡 Nutrition Tips")
            goal = st.selectbox("Choose your goal", [
                "Weight Maintenance", "Weight Loss", "Muscle Gain", "General"
            ])
            
            if st.button("🎯 Get Tips"):
                goal_map = {
                    "Weight Maintenance": "maintenance",
                    "Weight Loss": "weight_loss", 
                    "Muscle Gain": "muscle_gain",
                    "General": "general"
                }
                tips = call_backend(f"nutrition-tips?goal={goal_map[goal]}")
                if tips and "tips" in tips:
                    st.success("💪 Tips for you:")
                    for tip in tips["tips"]:
                        st.write(f"• {tip}")

# Footer
st.markdown("---")
st.markdown("### 🎯 Nutrition AI Assistant")