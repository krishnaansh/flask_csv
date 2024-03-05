import os
import pickle
import boto3
import pandas as pd
from sklearn.linear_model import LinearRegression
from flask import Blueprint, request
from flask_mongoengine import MongoEngine

from .models import Tenant, ProjectMetadata


api_bp = Blueprint("api", __name__)

# S3 Configuration
S3_BUCKET_NAME = "your_bucket_name"
S3_MODEL_KEY = "model.pkl"
S3_METADATA_KEY = "metadata.json"
S3_REGION = "your_s3_region"

# Connect to S3
s3 = boto3.client("s3", region_name=S3_REGION)


@api_bp.route("/build-model", methods=["POST"])
def build_model():
    # Process request data, save metadata to MongoDB
    if "file" not in request.files:
        return {"error": "No file part"}
    target_column = request.form.get("target_column")

    file = request.files["file"]

    # Read CSV file into pandas DataFrame
    df = pd.read_csv(file)

    # Build model
    X = df.drop("target_column", axis=1)
    y = df[target_column]
    model = LinearRegression()
    model.fit(X, y)

    # Save model to disk
    model_file = "model.pkl"
    with open(model_file, "wb") as f:
        pickle.dump(model, f)

    # Upload model to S3
    s3.upload_file(model_file, S3_BUCKET_NAME, S3_MODEL_KEY)

    # Save metadata to MongoDB
    tenant = Tenant(target_column=target_column, local_csv_file=file.filename).save()
    url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{S3_MODEL_KEY}"
    metadata = {
        "tenant": tenant,
        "local_csv_file": file.filename,
        "s3_location": url,
        "model_evaluation_results": model_file,
    }
    ProjectMetadata(**metadata).save()

    metadata["features"] = list(X.columns)
    # Clean up local files
    os.remove(model_file)

    return {"message": "Model built successfully", "data": metadata}
