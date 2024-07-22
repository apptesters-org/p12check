import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Get the absolute path of the database file
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'device_data.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Device(db.Model):
    __tablename__ = 'devices'  # Update the table name here
    id = db.Column(db.Integer, primary_key=True)
    udid = db.Column(db.String, unique=True, nullable=False)
    certificate_purchase_date = db.Column(db.Date, nullable=False)
    plan = db.Column(db.String, nullable=False)
    certificate_expiry_date = db.Column(db.Date, nullable=False)
    developer_account_name = db.Column(db.String, nullable=False)
    developer_account_renewal_date = db.Column(db.Date, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    udid = request.form['udid']
    device = Device.query.filter_by(udid=udid).first()
    if device:
        return render_template('info.html', device=device)
    else:
        return "Device not found"

if __name__ == '__main__':
    app.run(debug=True)
