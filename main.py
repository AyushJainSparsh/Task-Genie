from flask import Flask
from flask_cors import CORS
from routes.recommend import recommend_bp
from routes.priority import priority_bp
from routes.roadmap import roadmap_bp
from routes.module import module_bp
from routes.settimetable import settimetable_bp

app = Flask(__name__)  # Initialize the Flask app
CORS(app)  # Allow Cross-Origin Requests (for API access from other domains)

# Register each blueprint (route) so that the app knows about them
app.register_blueprint(recommend_bp)
app.register_blueprint(priority_bp)
app.register_blueprint(roadmap_bp)
app.register_blueprint(module_bp)
app.register_blueprint(settimetable_bp)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to my AI-World"  # This is the home page route

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask app
