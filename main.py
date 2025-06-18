import streamlit as st
from prediction_helper import predict

st.title('Credit Risk Prediction')

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, max_value=100, step=1)
with row1[1]:
    income = st.number_input('Income', min_value=0, value=1200000, step=1000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2000000, step=1000)

loan_to_income = loan_amount / income if income > 0 else 0

with row2[0]:
    st.text('Loan to Income Ratio:')
    st.text(f'{round(loan_to_income, 2)}')
with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (Months)', min_value=0, value=36, step=1)
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Avg. DPD', min_value=0, value=10)

with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, max_value=100, step=1)
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, value=100, step=1)
with row3[2]:
    number_of_open_accounts = st.number_input('Open Loan Account', min_value=1, max_value=4, step=1, value=2)

with row4[0]:
    residense_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Secured', 'Unsecured'])

    

if st.button('Calculate Risk'):
    probability, credit_score, rating = predict(
        age, loan_to_income,
        loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio,
        credit_utilization_ratio, number_of_open_accounts, residense_type,
        loan_purpose, loan_type
    )

    st.success(f"Probability of Default: {probability}%")
    st.info(f"Credit Score: {credit_score}")
    st.warning(f"Risk Rating: {rating}")