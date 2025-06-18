import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

model_data = joblib.load('artifacts/model_data.joblib')
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

def predict(
        age, loan_to_income, loan_tenure_months, avg_dpd_per_delinquency, 
        delinquency_ratio, credit_utilization_ratio, number_of_open_accounts, 
        residense_type, loan_purpose, loan_type):
    
    input_data = {
        # Numerical features
        'age': age,
        'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': number_of_open_accounts,
        'credit_utilization_ratio': credit_utilization_ratio,
        'loan_to_income': loan_to_income,
        'delinquency_ratio': delinquency_ratio,
        'avg_dpd_per_delinquency': avg_dpd_per_delinquency,

        # One-hot encoded: Residence Type
        'residence_type_Owned': 1 if residense_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residense_type == 'Rented' else 0,

        # One-hot encoded: Loan Purpose
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,

        # One-hot encoded: Loan Type
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0
    }
    # Add dummy value 1 for missing columns in scaler input
    for col in scaler.feature_names_in_:
        if col not in input_data:
            input_data[col] = 1  # Set dummy value 
    
    df = pd.DataFrame([input_data])
    df_scaled = df.copy()
    df_scaled[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df_final = df_scaled[features]

    prediction_proba = model.predict_proba(df_final)[0][1]  # Class 1 probability
    probability_of_default = prediction_proba * 100
    base_score = 300
    credit_score = round(base_score + (1 - prediction_proba) * 600)
    
    rating = (
        "Undefined" if (credit_score < 300) or (credit_score > 900) else
        "Poor" if credit_score < 580 else
        "Fair" if credit_score < 670 else
        "Good" if credit_score < 740 else
        "Very Good" if credit_score < 800 else
        "Excellent"
    )

    return round(probability_of_default, 2), credit_score, rating

