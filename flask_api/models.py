from flask_mongoengine import MongoEngine

db = MongoEngine()

class Tenant(db.Document):
    target_column = db.StringField()
    local_csv_file = db.StringField()

class ProjectMetadata(db.Document):
    tenant = db.ReferenceField(Tenant)
    local_csv_file = db.StringField()
    s3_location = db.StringField()
    model_evaluation_results = db.DictField()
