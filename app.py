from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from extract_features import extract_features

app = Flask(__name__)
CORS(app)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')

    if not url or not url.startswith(('http://', 'https://')):
        return jsonify({'error': '⚠️ Please enter a valid URL (start with http or https).'}), 400

    try:
        features = extract_features(url)

        if features is None or len(features) != 87:
            return jsonify({'error': f'❌ Feature extraction failed. Got {len(features)} features instead of 87.'}), 400

        # Optional debug print (for backend terminal only)
        print(f"✅ Extracted {len(features)} features from URL: {url}")

        prediction = model.predict([features])[0]
        return jsonify({'prediction': int(prediction)})

    except Exception as e:
        print(f"🔥 Error during prediction: {e}")
        return jsonify({'error': 'Internal server error occurred during prediction.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
