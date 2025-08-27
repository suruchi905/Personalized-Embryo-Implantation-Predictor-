import streamlit as st

# --- Predictor Function ---
def predict_implantation(age, bmi, day_of_transfer, prev_ivf, endometrium, embryo_grade):
    prob = 0.75  # baseline
    reasons = []

    # Age effect
    if age > 37:
        prob -= 0.15
        reasons.append("Advanced maternal age (>37 years)")
    elif age < 25:
        prob -= 0.05
        reasons.append("Very young maternal age (<25 years)")

    # BMI effect
    if bmi > 30:
        prob -= 0.1
        reasons.append("High BMI (>30)")
    elif bmi < 18:
        prob -= 0.1
        reasons.append("Low BMI (<18)")

    # Previous IVF attempts
    if prev_ivf >= 3:
        prob -= 0.1
        reasons.append("Multiple previous failed IVF attempts (≥3)")

    # Endometrial thickness
    if endometrium < 7:
        prob -= 0.1
        reasons.append("Thin endometrium (<7 mm)")

    # Embryo grade
    if embryo_grade.upper() != "A":
        prob -= 0.1
        reasons.append(f"Embryo grade {embryo_grade} (lower than A)")

    # Day of transfer
    if day_of_transfer not in [5, 6]:
        prob -= 0.05
        reasons.append("Transfer before blastocyst stage (Day 3)")

    # Clamp between 5% and 95%
    prob = max(0.05, min(prob, 0.95))

    # Convert to percentage
    return round(prob * 100, 1), reasons


# --- Streamlit UI ---
st.title("👶 Personalized Embryo Implantation Predictor (Prototype)")
st.write("⚠️ This is a **prototype research app**, not a medical device. Probabilities are illustrative only.")

# Inputs
age = st.number_input("Age of patient", min_value=18, max_value=50, value=32)
bmi = st.number_input("Body Mass Index (BMI)", min_value=15.0, max_value=45.0, value=22.0)
day_of_transfer = st.selectbox("Day of Embryo Transfer", [3, 5, 6])
prev_ivf = st.number_input("Previous IVF attempts", min_value=0, max_value=10, value=0)
endometrium = st.number_input("Endometrial thickness (mm)", min_value=4.0, max_value=20.0, value=9.0)
embryo_grade = st.selectbox("Embryo grade", ["A", "B", "C", "D"])

# Prediction
if st.button("Predict Implantation Probability"):
    prob_percent, reasons = predict_implantation(age, bmi, day_of_transfer, prev_ivf, endometrium, embryo_grade)

    st.subheader(f"🧪 Predicted Implantation Probability: {prob_percent}%")

    if prob_percent >= 70:
        st.success("✅ High probability (prototype estimate).")
    elif 50 <= prob_percent < 70:
        st.warning("🩺 Moderate probability (prototype estimate).")
    else:
        st.error("⚠️ Low probability (prototype estimate).")
        if reasons:
            st.markdown("### 🔎 Possible reasons for lower probability:")
            for r in reasons:
                st.write(f"- {r}")
