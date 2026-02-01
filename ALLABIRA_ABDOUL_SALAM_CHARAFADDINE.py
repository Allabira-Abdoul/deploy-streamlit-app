import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

st.set_page_config(page_title="HR Attrition Predictor", layout="wide")

@st.cache_resource
def load_assets():
    with open('rfc.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_assets()

freq_maps = {
    'BusinessTravel': {'Travel_Rarely': 0.709, 'Travel_Frequently': 0.188, 'Non-Travel': 0.102},
    'Department': {'Research & Development': 0.653, 'Sales': 0.303, 'Human Resources': 0.042},
    'EducationField': {'Life Sciences': 0.412, 'Medical': 0.315, 'Marketing': 0.108, 'Technical Degree': 0.089, 'Other': 0.055, 'Human Resources': 0.018},
    'JobRole': {'Sales Executive': 0.221, 'Research Scientist': 0.198, 'Laboratory Technician': 0.176, 'Manufacturing Director': 0.098, 'Healthcare Representative': 0.089, 'Manager': 0.069, 'Sales Representative': 0.056, 'Research Director': 0.054, 'Human Resources': 0.035},
    'MaritalStatus': {'Married': 0.457, 'Single': 0.320, 'Divorced': 0.221}
}

st.title("HR Employee Attrition Predictor")
st.markdown("Predicting whether an employee will stay or leave using your **Random Forest** model.")

with st.spinner('Loading model and configurations...'):
    time.sleep(1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Personal Details")
    age = st.slider('Age', 18, 60, 30)
    gender = st.selectbox('Gender', ['Male', 'Female'])
    marital = st.selectbox('Marital Status', list(freq_maps['MaritalStatus'].keys()))
    distance = st.number_input('Distance From Home (km)', 1, 30, 5)
    overtime = st.selectbox('Works Overtime?', ['Yes', 'No'])

with col2:
    st.subheader("Professional Factors")
    dept = st.selectbox('Department', list(freq_maps['Department'].keys()))
    role = st.selectbox('Job Role', list(freq_maps['JobRole'].keys()))
    income = st.number_input('Monthly Income ($)', 1000, 20000, 5000)
    stock = st.slider('Stock Option Level', 0, 3, 1)
    travel = st.selectbox('Business Travel', list(freq_maps['BusinessTravel'].keys()))

with st.expander("Additional Parameters (Impacts Accuracy)"):
    c1, c2, c3 = st.columns(3)
    with c1:
        env_sat = st.slider('Environment Satisfaction (1-4)', 1, 4, 3)
        num_cos = st.slider('Num Companies Worked', 0, 9, 1)
    with c2:
        work_life = st.slider('Work-Life Balance (1-4)', 1, 4, 3)
        years_at_co = st.slider('Years At Company', 0, 40, 5)
    with c3:
        total_work = st.slider('Total Working Years', 0, 40, 10)
        manager_yrs = st.slider('Years With Current Manager', 0, 17, 3)

if st.button('Analyze Risk'):
    with st.spinner('Random Forest is crunching the numbers...'):
        
        data = {
            'Age': age,
            'BusinessTravel': freq_maps['BusinessTravel'][travel],
            'DailyRate': 800, # Default/Mean
            'Department': freq_maps['Department'][dept],
            'DistanceFromHome': distance,
            'Education': 3,
            'EducationField': freq_maps['EducationField']['Life Sciences'],
            'EnvironmentSatisfaction': env_sat,
            'Gender': 1 if gender == 'Male' else 0,
            'HourlyRate': 65,
            'JobInvolvement': 3,
            'JobLevel': 2,
            'JobRole': freq_maps['JobRole'][role],
            'JobSatisfaction': 3,
            'MaritalStatus': freq_maps['MaritalStatus'][marital],
            'MonthlyIncome': income,
            'MonthlyRate': 14000,
            'NumCompaniesWorked': num_cos,
            'OverTime': 1 if overtime == 'Yes' else 0,
            'PercentSalaryHike': 15,
            'PerformanceRating': 3,
            'RelationshipSatisfaction': 3,
            'StockOptionLevel': stock,
            'TotalWorkingYears': total_work,
            'TrainingTimesLastYear': 2,
            'WorkLifeBalance': work_life,
            'YearsAtCompany': years_at_co,
            'YearsInCurrentRole': 2,
            'YearsSinceLastPromotion': 1,
            'YearsWithCurrManager': manager_yrs
        }
        
        input_df = pd.DataFrame([data])
        
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0]
        time.sleep(1.5)

    st.divider()
    if prediction == 1:
        st.error(f"**High Attrition Risk** (Probability: {prob[1]:.2%})")
        st.write("This employee is likely to leave the company.")
    else:
        st.success(f"**Low Attrition Risk** (Probability: {prob[1]:.2%})")
        st.write("This employee is likely to stay.")
        st.balloons()