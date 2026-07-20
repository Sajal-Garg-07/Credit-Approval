import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Credit Scoring Prediction System",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Credit Scoring Prediction System")
st.write("Predict whether an applicant is a **Good** or **Bad** credit risk.")

MODEL_PATH = Path("model/credit_scoring_model.pkl")

if not MODEL_PATH.exists():
    MODEL_PATH = Path("credit_scoring_model.pkl")

model = joblib.load(MODEL_PATH)

# -----------------------------
# Helper Function
# -----------------------------
def select_from_mapping(label, mapping):
    option = st.selectbox(label, list(mapping.keys()))
    return mapping[option]

# =====================================================
# Dropdown Mappings
# =====================================================

checking_map = {
    "No checking account": 1,
    "< 0 DM": 2,
    "0 ≤ Balance < 200 DM": 3,
    "≥ 200 DM / Salary for at least 1 year": 4,
}

credit_history_map = {
    "Delay in paying off in the past": 0,
    "Critical account / Other credits elsewhere": 1,
    "No credits taken / All credits paid back duly": 2,
    "Existing credits paid back duly till now": 3,
    "All credits at this bank paid back duly": 4,
}

purpose_map = {
    "Others": 0,
    "New Car": 1,
    "Used Car": 2,
    "Furniture / Equipment": 3,
    "Radio / Television": 4,
    "Domestic Appliances": 5,
    "Repairs": 6,
    "Education": 7,
    "Vacation": 8,
    "Retraining": 9,
    "Business": 10,
}

savings_map = {
    "Unknown / No savings account": 1,
    "< 100 DM": 2,
    "100 – 500 DM": 3,
    "500 – 1000 DM": 4,
    "≥ 1000 DM": 5,
}

employment_map = {
    "Unemployed": 1,
    "< 1 Year": 2,
    "1 – 4 Years": 3,
    "4 – 7 Years": 4,
    "≥ 7 Years": 5,
}

installment_map = {
    "≥ 35%": 1,
    "25% – 35%": 2,
    "20% – 25%": 3,
    "< 20%": 4,
}

personal_status_map = {
    "Male : Divorced / Separated": 1,
    "Female : Non-single or Male : Single": 2,
    "Male : Married / Widowed": 3,
    "Female : Single": 4,
}

other_debtors_map = {
    "None": 1,
    "Co-applicant": 2,
    "Guarantor": 3,
}

residence_map = {
    "< 1 Year": 1,
    "1 – 4 Years": 2,
    "4 – 7 Years": 3,
    "≥ 7 Years": 4,
}

property_map = {
    "Unknown / No property": 1,
    "Car or Other Property": 2,
    "Life Insurance / Savings": 3,
    "Real Estate": 4,
}

other_installment_map = {
    "Bank": 1,
    "Stores": 2,
    "None": 3,
}

housing_map = {
    "For Free": 1,
    "Rent": 2,
    "Own House": 3,
}

existing_credits_map = {
    "1 Credit": 1,
    "2 – 3 Credits": 2,
    "4 – 5 Credits": 3,
    "6 or More Credits": 4,
}

job_map = {
    "Unemployed / Unskilled (Non-resident)": 1,
    "Unskilled (Resident)": 2,
    "Skilled Employee / Official": 3,
    "Manager / Self-employed / Highly Qualified": 4,
}

dependents_map = {
    "3 or More People": 1,
    "0 – 2 People": 2,
}

telephone_map = {
    "No Telephone": 1,
    "Telephone Available": 2,
}

foreign_worker_map = {
    "Yes": 1,
    "No": 2,
}
st.header("Applicant Information")

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )

    duration = st.number_input(
        "Loan Duration (Months)",
        min_value=1,
        max_value=120,
        value=24,
        step=1
    )

    credit_amount = st.number_input(
        "Credit Amount (DM)",
        min_value=100,
        value=5000,
        step=100
    )

    checking_account = select_from_mapping(
        "Checking Account",
        checking_map
    )

    credit_history = select_from_mapping(
        "Credit History",
        credit_history_map
    )

    purpose = select_from_mapping(
        "Purpose of Loan",
        purpose_map
    )

    savings_account = select_from_mapping(
        "Savings Account",
        savings_map
    )

    employment_duration = select_from_mapping(
        "Employment Duration",
        employment_map
    )

    installment_rate = select_from_mapping(
        "Installment Rate",
        installment_map
    )

with col2:

    personal_status = select_from_mapping(
        "Personal Status & Sex",
        personal_status_map
    )

    other_debtors = select_from_mapping(
        "Other Debtors",
        other_debtors_map
    )

    residence_duration = select_from_mapping(
        "Residence Duration",
        residence_map
    )

    property_type = select_from_mapping(
        "Property",
        property_map
    )

    other_installment = select_from_mapping(
        "Other Installment Plans",
        other_installment_map
    )

    housing = select_from_mapping(
        "Housing",
        housing_map
    )

    existing_credits = select_from_mapping(
        "Existing Credits",
        existing_credits_map
    )

    job = select_from_mapping(
        "Job",
        job_map
    )

    dependents = select_from_mapping(
        "People Liable",
        dependents_map
    )

    telephone = select_from_mapping(
        "Telephone",
        telephone_map
    )

    foreign_worker = select_from_mapping(
        "Foreign Worker",
        foreign_worker_map
    )
credit_per_month = credit_amount / duration

if age < 25:
    age_group = "Young"

elif age < 40:
    age_group = "Adult"

elif age < 60:
    age_group = "Middle"

else:
    age_group = "Senior"

st.divider()

predict = st.button(
    "Predict Credit Risk",
    use_container_width=True
)
if predict:

    input_data = pd.DataFrame({
        "CheckingAccount": [checking_account],
        "Duration": [duration],
        "CreditHistory": [credit_history],
        "Purpose": [purpose],
        "CreditAmount": [credit_amount],
        "SavingsAccount": [savings_account],
        "EmploymentDuration": [employment_duration],
        "InstallmentRate": [installment_rate],
        "PersonalStatusSex": [personal_status],
        "OtherDebtors": [other_debtors],
        "ResidenceDuration": [residence_duration],
        "Property": [property_type],
        "Age": [age],
        "OtherInstallmentPlans": [other_installment],
        "Housing": [housing],
        "ExistingCredits": [existing_credits],
        "Job": [job],
        "NumberOfDependents": [dependents],
        "Telephone": [telephone],
        "ForeignWorker": [foreign_worker],
        "CreditPerMonth": [credit_per_month],
        "AgeGroup": [age_group]
    })

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    bad_probability = probability[0] * 100
    good_probability = probability[1] * 100

    st.divider()

    st.header("Prediction Result")

    if prediction == 1:
        st.success("✅ Good Credit Risk")
    else:
        st.error("❌ Bad Credit Risk")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Good Credit Probability",
            f"{good_probability:.2f}%"
        )

    with col2:
        st.metric(
            "Bad Credit Probability",
            f"{bad_probability:.2f}%"
        )

    st.progress(float(max(probability)))

    st.subheader("Applicant Details")

    display_data = pd.DataFrame({
        "Feature": [
            "Age",
            "Loan Duration",
            "Credit Amount",
            "Credit Per Month",
            "Age Group"
        ],
        "Value": [
            age,
            duration,
            credit_amount,
            round(credit_per_month, 2),
            age_group
        ]
    })

    st.table(display_data)

    with st.expander("View Model Input"):
        st.dataframe(input_data)
