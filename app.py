from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from extract_features import extract_features

app = Flask(__name__)
CORS(app)

# Load trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')

    if not url or not url.startswith(('http://', 'https://')):
        return jsonify({'error': 'Please enter a valid URL (start with http or https).'}), 400

    try:
        features = extract_features(url)

        if features is None or len(features) != 87:
            return jsonify({'error': f'❌ Feature extraction failed. Got {len(features)} features instead of 87.'}), 400

        # Predict probability
        proba = model.predict_proba([features])[0]
        confidence = float(proba[1])  # probability of phishing

        # You can adjust the threshold as needed (e.g., 0.7 = 70%)
        threshold = 0.7
        prediction = int(confidence >= threshold)

        print(f"🔍 URL: {url}")
        print(f"✅ Features: {len(features)}")
        print(f"🎯 Confidence: {confidence:.4f} | Prediction: {'Phishing' if prediction else 'Legitimate'}")

        return jsonify({
            'prediction': prediction,
            'confidence': round(confidence, 4),
            'threshold': threshold
        })

    except Exception as e:
        print(f"🔥 Error during prediction: {e}")
        return jsonify({'error': 'Internal server error occurred during prediction.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
