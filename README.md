# ML Model Builder Application

This application builds a machine learning model from CSV data, uploads the model to S3, and saves relevant metadata to a MongoDB instance.

## Setup

1. Make sure you have Docker installed on your system.
2. Clone this repository.
3. Run the `run.sh` script to start the application.

## Components

### flask_api

This component provides a Flask API that communicates with the MongoDB database to read/write metadata.

### main_script.py

This script stitches everything together. It creates an entry in the tenant table, generates and evaluates a model, uploads the model to S3, and saves metadata to MongoDB.

## Usage

1. After running the application, send a POST request to `http://localhost:5000/build-model` with the CSV file and target column as form data.
2. The model will be built, uploaded to S3, and metadata will be saved to MongoDB.
3. Use appropriate endpoints to retrieve tenant and project metadata.
