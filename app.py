import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use the os.path.join for better compatibility
db_path = os.path.join(os.path.expanduser('~'), 'Library', 'Mobile Documents', 'com~apple~CloudDocs', 'Downloads', 'udidcheck', 'device_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///device_data.db'

db = SQLAlchemy(app)

class Device(db.Model):
    __tablename__ = 'devices'
    udid = db.Column(db.String, primary_key=True)
    certificate_purchase_date = db.Column(db.String)
    plan = db.Column(db.String)
    certificate_expiry_date = db.Column(db.String)
    developer_account_name = db.Column(db.String)
    developer_account_renewal_date = db.Column(db.String)

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
        return "Device not found", 404

if __name__ == '__main__':
    app.run(debug=True)
