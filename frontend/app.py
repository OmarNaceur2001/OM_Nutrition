import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Nutrition", page_icon="🎯")

# App title and introduction
st.title("🍎 Nutrition AI Assistant")
st.write("Calculate your nutritional needs easily!")

# User Input Form
with st.form("user_info"):
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=170.0)
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", [
            "Low (Sedentary)",
            "Medium (Exercise 3-4 times/week)", 
            "High (Daily exercise)"
        ])
    
    submitted = st.form_submit_button("Calculate My Needs")

# Handle form submission and API call
if submitted:
    # Data mapping for the backend API
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
    
    try:
        # Sending request to the backend (FastAPI)
        response = requests.post("http://localhost:8000/calculate", json=user_data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        
        # Display Results
        st.success("🎊 Your nutritional needs have been calculated!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Daily Calories", f"{result['daily_calories']} kcal")
        with col2:
            st.metric("Protein", f"{result['protein_grams']} g")
        with col3:
            st.metric("Carbohydrates", f"{result['carbs_grams']} g")
        with col4:
            st.metric("Fat", f"{result['fat_grams']} g")
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Connection Error: Could not connect to the FastAPI server.")
        st.info("Please ensure the backend server is running on http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ API Error: Received status code {response.status_code}")
        st.info(f"Details: {response.text}")
    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {e}")
        st.info("Please check the console for details.")