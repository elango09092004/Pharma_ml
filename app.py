from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS 

app = Flask(__name__)

CORS(app)
model = joblib.load('model.pkl')

def dataframe_to_json(df):
    return df.to_json(orient='records')

def predict_sales(start_date, end_date, drug):
    # Create a date range based on the provided start and end dates
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df_test = pd.DataFrame(index=dates)
    
    # Add features like Year, Month, Weekday, Drug
    df_test['Year'] = df_test.index.year
    df_test['Month'] = df_test.index.month
    df_test['Weekday Name'] = df_test.index.weekday
    df_test['Drug'] = drug  # Here we assign the drug input to the column

    # Label encode the 'Weekday Name' column
    le_weekday = LabelEncoder()
    df_test['Weekday Name'] = le_weekday.fit_transform(df_test['Weekday Name'])

    # Encode the 'Drug' column using LabelEncoder
    le_drug = LabelEncoder()
    df_test['Drug'] = le_drug.fit_transform(df_test['Drug'])
    
    # Ensure the DataFrame has the correct types for all features
    df_test['Year'] = df_test['Year'].astype(int)
    df_test['Month'] = df_test['Month'].astype(int)

    # Make predictions using the trained model
    df_test['predicted_quantity'] = model.predict(df_test[['Year', 'Month', 'Weekday Name', 'Drug']])
    
    # Convert the predictions to JSON
    json_output = dataframe_to_json(df_test)

    return json_output

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        start_date = data['start_date']
        end_date = data['end_date']
        drug = data['drug']

        prediction = predict_sales(start_date, end_date, drug)
        return prediction
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
