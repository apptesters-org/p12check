from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///device_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Device model
class Device(db.Model):
    __tablename__ = 'devices'
    udid = db.Column(db.String, unique=True, primary_key=True)
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
        current_date = datetime.now().date()
        return render_template('info.html', device=device, current_date=current_date)
    else:
        return render_template('notfound.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
