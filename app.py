from flask import Flask
from extensions import db, login_manager
from models import User, Stock, Portfolio, Transaction, Watchlist, Prediction

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocksense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

@app.route('/')
def index():
    return "<h1>Welcome to StockSense! 📈</h1><p>Your stock prediction platform is running.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
