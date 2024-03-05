from flask import Flask
from flask_api.routes import api_bp


app = Flask(__name__)
app.register_blueprint(api_bp)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}



def main():
    # Create tenant entry
    # Read environment variables
    # Call build_model from ml_component
    # Upload model to S3
    # Save metadata to MongoDB    
    app.run(debug=True, use_reloader=True)

if __name__ == "__main__":
    main()
