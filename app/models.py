from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import app, db
from app import login
from time import time
import jwt


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    past_records = db.relationship('MealPlanRecord', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


#  net cash is the $ that, based on algorithm, is positive to signify amount saved
#  or negative to signify own amount to add into meal plan
class MealPlanRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    money_spent = db.Column(db.Float, index=True)

    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    mp_amount = db.Column(db.Float)

    net_cash = db.Column(db.Float)

    def __repr__(self):
        return "<Date: {}, MP Amount: {}, Avg Spent: {}, Gain/Loss: {}".format(\
            self.date, self.mp_amount, self.money_spent, self.net_cash)
