import streamlit as st
import joblib
import pandas as pd

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="FinGuard AI",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------------
# LOAD MODEL
# ----------------------------------
model = joblib.load("loan_approval_model.pkl")
feature_names = joblib.load("feature_names.pkl")

# ----------------------------------
# CSS
# ----------------------------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"]{
    background:#FFF7FA;
}

/* Hide Streamlit header */
header{
    visibility:hidden;
}

/* Labels */
label{
    color:black !important;
    font-weight:600 !important;
}

/* Hero Card */
.hero-card{
    background:white;
    border-radius:25px;
    padding:40px;
    text-align:center;
    box-shadow:0px 4px 20px rgba(0,0,0,0.08);
}

/* White Cards */
.white-card{
    background:white;
    border-radius:20px;
    padding:25px;
    box-shadow:0px 4px 20px rgba(0,0,0,0.08);
    margin-top:20px;
}

/* Title */
.main-title{
    color:#E91E63;
    font-size:60px;
    font-weight:800;
}

/* Subtitle */
.sub-title{
    color:#E91E63;
    font-size:34px;
    font-weight:700;
}

.desc{
    color:#555;
    font-size:18px;
}

.status-title{
    color:#E91E63;
    font-size:32px;
    font-weight:700;
}

.black-text{
    color:black;
    font-size:20px;
}

.small-text{
    color:black;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HERO SECTION
# ----------------------------------
st.markdown("""
<div class="hero-card">

<div class="main-title">
🏦 FinGuard AI
</div>

<div class="sub-title">
AI-Powered Loan Risk Assessment Platform
</div>

<br>

<div class="desc">
Evaluate loan applications using machine learning,
risk intelligence and predictive analytics.
</div>

</div>
""", unsafe_allow_html=True)

# ----------------------------------
# STATUS CARD
# ----------------------------------
st.markdown("""
<div class="white-card">

<div class="status-title">
✅ Model Status
</div>

<br>

<div class="black-text">
Random Forest Model Loaded Successfully
</div>

<br>

<div class="small-text">
Ready for loan prediction.
</div>

</div>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAN FORM CARD
# ----------------------------------
st.markdown("""
<div class="white-card">

<h2 style="
text-align:center;
color:#E91E63;
margin-bottom:10px;
">
📝 Loan Application Details
</h2>

<p style="
text-align:center;
color:black;
">
Fill in the applicant information below for risk assessment
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------
# FORM
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    applicant_income = st.number_input(
        "Applicant Monthly Income (₹)",
        min_value=0,
        value=5000
    )

    loan_amount = st.number_input(
    "Loan Amount (₹ Thousands)",
    min_value=0,
    value=120,
    help="Example: 120 means ₹120,000 (1.2 Lakh)"
    )
    

    married = st.selectbox(
        "Marital Status",
        ["No", "Yes"]
    )

    education = st.selectbox(
        "Education",
        ["Not Graduate", "Graduate"]
    )

    credit_history = st.selectbox(
        "Credit History",
        ["Poor", "Good"]
    )

with col2:

    coapplicant_income = st.number_input(
        "Coapplicant Monthly Income (₹)",
        min_value=0,
        value=0
    )

    loan_term = st.number_input(
        "Loan Amount Term (Months)",
        min_value=0,
        value=360
    )

    dependents = st.selectbox(
        "Dependents",
        ["0", "1", "2", "3+"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["No", "Yes"]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Rural", "Semiurban", "Urban"]
    )
    

# ----------------------------------
# BUTTON (NEXT STEP)
# ----------------------------------

st.write("")
st.write("")
predict_btn = st.button(
    "🔮 Predict Loan Approval",
    use_container_width=True
)

if predict_btn:

    # Validation
    if loan_amount > 10000:
        st.error("⚠️ Loan Amount should be entered in ₹ Thousands. Example: 120 = ₹120,000")
        st.stop()

    if applicant_income <= 0:
        st.error("⚠️ Applicant income must be greater than 0")
        st.stop()

    if applicant_income + coapplicant_income <= 0:
        st.error("⚠️ Total income cannot be zero")
        st.stop()

    married = 1 if married == "Yes" else 0

    education = 1 if education == "Graduate" else 0

    self_employed = 1 if self_employed == "Yes" else 0

    credit_history = 1 if credit_history == "Good" else 0

    dependents = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3+": 3
    }[dependents]

    # Feature Engineering

    total_income = applicant_income + coapplicant_income

    loan_income_ratio = loan_amount / total_income

    property_area_semiurban = 1 if property_area == "Semiurban" else 0
    property_area_urban = 1 if property_area == "Urban" else 0

    input_data = pd.DataFrame([{
    "Married": married,
    "Dependents": dependents,
    "Education": education,
    "Self_Employed": self_employed,
    "ApplicantIncome": applicant_income,
    "CoapplicantIncome": coapplicant_income,
    "LoanAmount": loan_amount,
    "Loan_Amount_Term": loan_term,
    "Credit_History": credit_history,
    "Property_Area_Semiurban": property_area_semiurban,
    "Property_Area_Urban": property_area_urban,
    "TotalIncome": total_income,
    "LoanIncomeRatio": loan_income_ratio
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("🟢 Loan Approved")
    else:
        st.error("🔴 Loan Rejected")


    #confidence score calculaation

    probability = model.predict_proba(input_data)

    confidence = max(probability[0]) * 100

    st.info(f"Confidence Score: {confidence:.2f}%")

    #risk levell

    if confidence >= 80:
        st.success("🟢 Low Risk")
    elif confidence >= 60:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")


    st.markdown("""
    <h2 style="
    text-align:center;
    color:#E91E63;
    margin-top:20px;
    ">
    📋 Application Summary
    </h2>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
    background:white;
    padding:20px;
    border-radius:15px;
    color:black;
    font-size:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    ">

    <b>Total Income:</b> ₹{total_income:,}<br><br>

    <b>Loan Amount:</b> ₹{loan_amount:,}000<br><br>

    <b>Credit History:</b> {"Good" if credit_history else "Bad"}

    </div>
    """, unsafe_allow_html=True)

    

