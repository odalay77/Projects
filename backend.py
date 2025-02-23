from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Database Model
class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(10), unique=True, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    date_collected = db.Column(db.String(10), nullable=False)
    time_collected = db.Column(db.String(5), nullable=False)
    date_frozen = db.Column(db.String(10), nullable=False)
    time_frozen = db.Column(db.String(5), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Generate a Unique Sample ID
def generate_sample_id():
    last_entry = PatientRecord.query.order_by(PatientRecord.id.desc()).first()
    if last_entry:
        return f"SID{last_entry.id + 1:05d}"
    return "SID00001"

# Endpoint to Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    new_record = PatientRecord(
        sample_id=generate_sample_id(),
        glucose=data['glucose'],
        date_collected=data['dateCollected'],
        time_collected=data['timeCollected'],
        date_frozen=data['dateFrozen'],
        time_frozen=data['timeFrozen']
    )

    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Data added successfully!"})

# Endpoint to Retrieve Data
@app.route('/data', methods=['GET'])
def get_data():
    records = PatientRecord.query.all()
    return jsonify([
        {
            "sample_id": rec.sample_id,
            "glucose": rec.glucose,
            "date_collected": rec.date_collected,
            "time_collected": rec.time_collected,
            "date_frozen": rec.date_frozen,
            "time_frozen": rec.time_frozen
        }
        for rec in records
    ])

if __name__ == '__main__':
    app.run(debug=True)