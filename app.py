from flask import Flask, request, jsonify
import streamlit as st
import requests

# Flask Backend
app = Flask(__name__)

@app.route('/check_ph', methods=['GET'])
def check_ph():
    try:
        ph_value = float(request.args.get('ph', 0))
        if 6.5 <= ph_value <= 8.5:
            return jsonify({'status': 'Safe', 'message': 'Water is safe to drink'})
        else:
            return jsonify({'status': 'Unsafe', 'message': 'Water is not safe to drink'})
    except ValueError:
        return jsonify({'error': 'Invalid input, please enter a numeric pH value'})

if __name__ == '__main__':
    app.run(port=5000, debug=False)  # Change debug=True to debug=False


# Streamlit Frontend
st.title("Water Drinkability Checker")
ph_input = st.number_input("Enter pH value of water:", min_value=0.0, max_value=14.0, step=0.1)

if st.button("Check Drinkability"):
    response = requests.get(f"http://127.0.0.1:5000/check_ph?ph={ph_input}")
    result = response.json()
    
    if 'error' in result:
        st.error(result['error'])
    else:
        status = result['status']
        message = result['message']
        if status == 'Safe':
            st.success(message)
        else:
            st.warning(message)
