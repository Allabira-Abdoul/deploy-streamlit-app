import streamlit as st
import pandas as pd
import numpy as np
import skops.io as sio
import time
import warnings

st.set_page_config(page_title="HR Attrition Predictor", layout="wide")

@st.cache_resource
def load_assets():
    try:
        model = sio.load('rfc.skops', trusted=[])
        return model
    except Exception as e:
        st.error("Failed to load model assets. Please check server configuration.")
        st.stop()

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

# Bolt Optimization: Removed fake loading spinner that added a 1-second delay.
# This prevents a 1s lag on every UI update, saving 1s overall per run.

main_left, main_right = st.columns([2.2, 1], gap="large")

with main_left:
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 👤 Personal Details")
            age = st.slider('AGE', 18, 60, 34)
            gender = st.selectbox('GENDER', ['Female', 'Male'])
            marital = st.selectbox('MARITAL STATUS', list(freq_maps['MaritalStatus'].keys()), index=list(freq_maps['MaritalStatus'].keys()).index('Single'))
            distance = st.number_input('DISTANCE FROM HOME (KM)', 1, 30, 12, step=1)
            overtime = st.toggle('OVERTIME', value=False)

    with col2:
        with st.container(border=True):
            st.markdown("### 💼 Professional Factors")
            dept = st.selectbox('DEPARTMENT', list(freq_maps['Department'].keys()), index=list(freq_maps['Department'].keys()).index('Research & Development'))
            role = st.selectbox('JOB ROLE', list(freq_maps['JobRole'].keys()), index=list(freq_maps['JobRole'].keys()).index('Research Scientist'))
            income = st.number_input('MONTHLY INCOME ($)', 1000, 20000, 5400, step=500)
            stock = st.slider('STOCK OPTION LEVEL', 0, 3, 1)
            travel = st.selectbox('BUSINESS TRAVEL', list(freq_maps['BusinessTravel'].keys()), index=list(freq_maps['BusinessTravel'].keys()).index('Travel_Rarely'))

    with st.expander("Additional Parameters", icon=":material/tune:"):
        c1, c2 = st.columns(2)
        with c1:
            env_sat = st.slider('ENVIRONMENT SATISFACTION', 1, 4, 3)
            total_work = st.slider('TOTAL WORKING YEARS', 0, 40, 10)
            years_at_co = st.slider('YEARS AT COMPANY', 0, 40, 5)
        with c2:
            work_life = st.slider('WORK-LIFE BALANCE', 1, 4, 2)
            num_cos = st.slider('NUM COMPANIES WORKED', 0, 9, 3)
            manager_yrs = st.slider('YEARS WITH CURRENT MANAGER', 0, 17, 2)

with main_right:
    analyze_clicked = st.button('Analyze Risk', type="primary", use_container_width=True, icon=":material/bar_chart:")

    if analyze_clicked:
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
                'OverTime': 1 if overtime else 0,
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

            # Bolt Optimization: Avoid Pandas instantiation overhead and double inference.
            # Single-row dict converted directly to list of lists.
            input_arr = [list(data.values())]

            # Bolt Optimization: Removed fake loading delay (time.sleep(1.5))
            # Prediction now happens instantaneously, saving 1.5s per submission.
            try:
              with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                prob = model.predict_proba(input_arr)[0]
                prediction = model.classes_[np.argmax(prob)]
            except Exception:
                # Sentinel: Prevent leaking internal stack trace to users
                st.error("An error occurred during prediction. Please verify inputs or contact support.")
                st.stop()

        with st.container(border=True):
            if prediction == 1:
                st.error(f"**High Attrition Risk**\n\nProbability: {prob[1]:.2%}", icon=":material/warning:")
                st.write("This employee is likely to leave the company.")
            else:
                st.success(f"**Low Attrition Risk**\n\nProbability: {prob[1]:.2%}", icon=":material/check_circle:")
                st.write("This employee is likely to stay.")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='text-align: center; color: #888;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #888; font-size: 2em; margin-bottom: 0;'>⚙️</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em; letter-spacing: 1px; color: #888;'>MODEL ACCURACY: 94.2%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)