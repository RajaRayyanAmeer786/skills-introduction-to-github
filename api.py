from flask import Flask, request, jsonify
import requests

class SyntaxChecker:


    "Handles syntax checking with the Gemini API."

    def _init_(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def check_syntax(self, code):
        "Makes a request to the Gemini API to check the code syntax."
        json_payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": code
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=json_payload
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

class PredictionService:
    "Handles code prediction functionality."

    def predict_code(self, code):
        "Logic for predicting code based on input."
        return {"prediction": "Predicted future code..."}

class API:
    "Flask API class that integrates with external services."

    def _init_(self, syntax_checker, prediction_service):
        self.app = Flask(_name_)
        self.syntax_checker = syntax_checker
        self.prediction_service = prediction_service
        self._add_routes()

    def _add_routes(self):
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])  # Root URL
        self.app.add_url_rule('/favicon.ico', 'favicon', self.favicon, methods=['GET'])  # Favicon
        self.app.add_url_rule('/check_syntax', 'check_syntax', self.check_syntax, methods=['POST'])
        self.app.add_url_rule('/predict_code', 'predict_code', self.predict_code, methods=['POST'])

    def index(self):
        return jsonify({"message": "Welcome to the API!"})  # Default response for /

    def favicon(self):
        return '', 204  # Respond with no content for /favicon.ico

    def check_syntax(self):
        code = request.json.get('code')
        result = self.syntax_checker.check_syntax(code)
        return jsonify(result)

    def predict_code(self):
        code = request.json.get('code')
        prediction = self.prediction_service.predict_code(code)
        return jsonify(prediction)


def create_app():
    api_key = 'AlzaSyDZus0NaKoJnKUNt-hhrKtdY9bd2-yzpqw'  # Add your Gemini API key here
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Updated endpoint
    syntax_checker = SyntaxChecker(api_key, api_url)
    prediction_service = PredictionService()
    api = API(syntax_checker, prediction_service)
    return api.app  # Return the Flask app instance

if __name__ == '_main_':
    app = create_app()
    app.run(debug=True)