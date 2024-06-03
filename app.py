import streamlit as st
import requests
import json

# Static data for previous predictions
previous_predictions = [
    {
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing"],
        "result": {
            "disease": "Fungal infection",
            "description": [
                {"Symptom_Description": "Fungal infections are common infections caused by fungi."}
            ],
            "precaution": [
                {"0": "Keep the affected area dry"},
                {"1": "Use antifungal cream"},
                {"2": "Maintain good hygiene"},
                {"3": "Avoid sharing personal items"}
            ],
            "doctor": [
                {"0": "Dermatologist"},
                {"1": "General Physician"}
            ]
        }
    }
]

# Function to get prediction from the external API
def get_prediction(symptoms):
    url = 'https://pharmcare-dpv2-deployment.onrender.com/predict_disease'
    response = requests.post(url, json={"symptoms": symptoms})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get prediction."}

# Streamlit app layout
st.title('Disease Predictor')

# Tabs for prediction and previous results
tab1, tab2 = st.tabs(["Predict Disease", "Previous Predictions"])

with tab1:
    st.header('Predict Disease')
    symptoms = [
        "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing",
        "shivering", "chills", "joint_pain", "stomach_pain", "acidity",
        "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition",
        "spotting_urination", "fatigue", "weight_gain", "anxiety", 
        "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", 
        "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", 
        "high_fever", "sunken_eyes", "breathlessness", "sweating", 
        "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine", 
        "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", 
        "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", 
        "yellowing_of_eyes", "acute_liver_failure", "fluid_overload", 
        "swelling_of_stomach", "swelled_lymph_nodes", "malaise", 
        "blurred_and_distorted_vision", "phlegm", "throat_irritation", 
        "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", 
        "chest_pain", "weakness_in_limbs", "fast_heart_rate", 
        "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", 
        "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", 
        "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", 
        "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger", 
        "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech", 
        "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck", 
        "swelling_joints", "movement_stiffness", "spinning_movements", 
        "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", 
        "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine", 
        "continuous_feel_of_urine", "passage_of_gases", "internal_itching", 
        "toxic_look_(typhos)", "depression", "irritability", "muscle_pain", 
        "altered_sensorium", "red_spots_over_body", "belly_pain", 
        "abnormal_menstruation", "dischromic_patches", "watering_from_eyes", 
        "increased_appetite", "polyuria", "family_history", "mucoid_sputum", 
        "rusty_sputum", "lack_of_concentration", "visual_disturbances", 
        "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", 
        "stomach_bleeding", "distention_of_abdomen", "history_of_alcohol_consumption", 
        "fluid_overload", "blood_in_sputum", "prominent_veins_on_calf", 
        "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", 
        "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", 
        "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"
    ]

    selected_symptoms = []
    for i in range(1, 7):
        selected_symptoms.append(st.selectbox(f'Symptom {i}', [""] + symptoms))

    if st.button('Predict Disease'):
        selected_symptoms = [s for s in selected_symptoms if s]
        if 4 <= len(selected_symptoms) <= 6:
            result = get_prediction(selected_symptoms)
            if "error" in result:
                st.error(result["error"])
            else:
                st.write(f"**Predicted Disease:** {result['disease']}")
                st.write(f"**Description:** {result['description'][0]['Symptom_Description']}")
                
                precautions = "Precautions: " + ", ".join(
                    precaution[key] for precaution in result['precaution'] for key in precaution
                )
                st.write(precautions)

                doctors = "Specialists to Consult: " + ", ".join(
                    doctor[key] for doctor in result['doctor'] for key in doctor
                )
                st.write(doctors)
        else:
            st.error("Please provide between 4 to 6 symptoms.")

with tab2:
    st.header('Previous Predictions')
    if previous_predictions:
        for pred in previous_predictions:
            symptoms = pred["symptoms"]
            result = pred["result"]
            st.write(f"**Symptoms:** {', '.join(symptoms)}")
            st.write(f"**Predicted Disease:** {result['disease']}")
            st.write(f"**Description:** {result['description'][0]['Symptom_Description']}")
            precautions = "Precautions: " + ", ".join(
                precaution[key] for precaution in result['precaution'] for key in precaution
            )
            st.write(precautions)
            doctors = "Specialists to Consult: " + ", ".join(
                doctor[key] for doctor in result['doctor'] for key in doctor
            )
            st.write(doctors)
            st.write("---")
    else:
        st.write("No previous predictions found.")
