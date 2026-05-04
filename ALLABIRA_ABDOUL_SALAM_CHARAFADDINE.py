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
            age = st.slider('AGE', 18, 60, 28)
            gender = st.selectbox('GENDER', ['Female', 'Male'], index=1)
            marital = st.selectbox('MARITAL STATUS', list(freq_maps['MaritalStatus'].keys()), index=list(freq_maps['MaritalStatus'].keys()).index('Single'))
            distance = st.number_input('DISTANCE FROM HOME (KM)', 1, 50, 24, step=1)
            education = st.slider('EDUCATION LEVEL', 1, 5, 1)
            edu_field = st.selectbox('EDUCATION FIELD', list(freq_maps['EducationField'].keys()), index=list(freq_maps['EducationField'].keys()).index('Life Sciences'))

        with st.container(border=True):
            st.markdown("### 💰 Compensation & Benefits")
            income = st.number_input('MONTHLY INCOME ($)', 1000, 20000, 2100, step=500)
            daily_rate = st.number_input('DAILY RATE', 100, 1500, 350, step=50)
            hourly_rate = st.number_input('HOURLY RATE', 30, 100, 40, step=5)
            monthly_rate = st.number_input('MONTHLY RATE', 2000, 30000, 5000, step=1000)
            salary_hike = st.slider('PERCENT SALARY HIKE', 11, 25, 11)
            stock = st.slider('STOCK OPTION LEVEL', 0, 3, 0)

        with st.container(border=True):
            st.markdown("### 😊 Satisfaction & Engagement")
            env_sat = st.slider('ENVIRONMENT SATISFACTION', 1, 4, 1)
            job_inv = st.slider('JOB INVOLVEMENT', 1, 4, 1)
            job_sat = st.slider('JOB SATISFACTION', 1, 4, 1)
            rel_sat = st.slider('RELATIONSHIP SATISFACTION', 1, 4, 1)
            work_life = st.slider('WORK-LIFE BALANCE', 1, 4, 1)
            perf_rating = st.slider('PERFORMANCE RATING', 3, 4, 3)

    with col2:
        with st.container(border=True):
            st.markdown("### 💼 Professional Factors")
            dept = st.selectbox('DEPARTMENT', list(freq_maps['Department'].keys()), index=list(freq_maps['Department'].keys()).index('Sales'))
            role = st.selectbox('JOB ROLE', list(freq_maps['JobRole'].keys()), index=list(freq_maps['JobRole'].keys()).index('Sales Representative'))
            job_level = st.slider('JOB LEVEL', 1, 5, 1)
            travel = st.selectbox('BUSINESS TRAVEL', list(freq_maps['BusinessTravel'].keys()), index=list(freq_maps['BusinessTravel'].keys()).index('Travel_Frequently'), format_func=lambda x: x.replace('_', ' '))
            overtime = st.toggle('OVERTIME', value=True)
            training = st.slider('TRAINING TIMES LAST YEAR', 0, 6, 0)

        with st.container(border=True):
            st.markdown("### 🕰️ Tenure & History")
            total_work = st.slider('TOTAL WORKING YEARS', 0, 40, 4)
            num_cos = st.slider('NUM COMPANIES WORKED', 0, 9, 7)
            years_at_co = st.slider('YEARS AT COMPANY', 0, 40, 1)
            years_in_role = st.slider('YEARS IN CURRENT ROLE', 0, 18, 0)
            years_since_prom = st.slider('YEARS SINCE LAST PROMOTION', 0, 15, 0)
            manager_yrs = st.slider('YEARS WITH CURRENT MANAGER', 0, 17, 0)

with main_right:
    analyze_clicked = st.button('Analyze Risk', type="primary", use_container_width=True, icon=":material/bar_chart:")

    if analyze_clicked:
        with st.spinner('Random Forest is crunching the numbers...'):

            data = {
                'Age': age,
                'BusinessTravel': freq_maps['BusinessTravel'][travel],
                'DailyRate': daily_rate,
                'Department': freq_maps['Department'][dept],
                'DistanceFromHome': distance,
                'Education': education,
                'EducationField': freq_maps['EducationField'][edu_field],
                'EnvironmentSatisfaction': env_sat,
                'Gender': 1 if gender == 'Male' else 0,
                'HourlyRate': hourly_rate,
                'JobInvolvement': job_inv,
                'JobLevel': job_level,
                'JobRole': freq_maps['JobRole'][role],
                'JobSatisfaction': job_sat,
                'MaritalStatus': freq_maps['MaritalStatus'][marital],
                'MonthlyIncome': income,
                'MonthlyRate': monthly_rate,
                'NumCompaniesWorked': num_cos,
                'OverTime': 1 if overtime else 0,
                'PercentSalaryHike': salary_hike,
                'PerformanceRating': perf_rating,
                'RelationshipSatisfaction': rel_sat,
                'StockOptionLevel': stock,
                'TotalWorkingYears': total_work,
                'TrainingTimesLastYear': training,
                'WorkLifeBalance': work_life,
                'YearsAtCompany': years_at_co,
                'YearsInCurrentRole': years_in_role,
                'YearsSinceLastPromotion': years_since_prom,
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
    else:
        st.info("Adjust parameters and click **Analyze Risk** to generate a prediction.", icon=":material/info:")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='text-align: center; color: #888;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #888; font-size: 2em; margin-bottom: 0;'>⚙️</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em; letter-spacing: 1px; color: #888;'>MODEL ACCURACY: 94.2%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)