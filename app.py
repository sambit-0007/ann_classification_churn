import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle
import streamlit as st

model = load_model(r'ann_classification\ann\model.h5')
# load the encoders and scaler
with open(r'ann_classification\ann\label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)

with open(r'ann_classification\ann\one_hot_geography.pkl','rb') as file:
    label_encoder_geo = pickle.load(file)

with open(r'ann_classification\ann\scaler.pkl','rb') as file:
    scaler = pickle.load(file)


#Streamlit app

st.title('Customer Churn Prediction')

geography = st.selectbox('Geography', label_encoder_geo.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age', 18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of Products', 1,4)
has_cr_card = st.selectbox('Has Credit Card', [0,1])
is_active_member = st.selectbox('Is Active Member', [0,1])

input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure': [tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]
})
geo_encoded = label_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=label_encoder_geo.get_feature_names_out(['Geography']))

input_data = pd.concat([input_data.reset_index(drop=True),geo_encoded_df], axis = 1)


input_scaled = scaler.transform(input_data)
prediction = model.predict(input_scaled)
prediction_proba = prediction[0][0]

st.write(f'churn probability: {prediction_proba: .2f}')

if prediction_proba > 0.5 :
    st.write('The Customer is likely to churn')
else:
    st.write('The Customer is not likely to churn')



























