from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, MealPlanRecord


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='marlon')
        u.set_password('cat')

        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_empty_meal_records(self):
        u1 = User(username='marlon', email='marlon@test.com', current_amount=350)
        u2 = User(username='johnny', email='johnny@test.com', current_amount=500)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        #  testing empty records at start
        self.assertEqual(u1.past_records.all(), [])
        self.assertEqual(u2.past_records.all(), [])

    def test_meal_records(self):
        u1 = User(username='marlon', email='marlon@test.com', current_amount=350.0)
        u2 = User(username='johnny', email='johnny@test.com', current_amount=500.0)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # create four posts, using timedelta to have different times
        now = datetime.utcnow()
        m1 = MealPlanRecord(avg_spent=7.5, student=u1, mp_amount=350.0,
                            date=now + timedelta(days=1))
        #m1.set_mp_amount()
        m1.set_end_and_money_to_add()
        m1.update_user_mp_amount()

        m2 = MealPlanRecord(avg_spent=7.5, student=u1, mp_amount=350.0,
                            date=now + timedelta(days=2))
        #m2.set_mp_amount()
        m2.set_end_and_money_to_add()
        m2.update_user_mp_amount()

        m3 = MealPlanRecord(avg_spent=7.5, student=u1, mp_amount=350.0,
                            date=now + timedelta(days=3))
        #m3.set_mp_amount()
        m3.set_end_and_money_to_add()
        m3.update_user_mp_amount()

        m4 = MealPlanRecord(avg_spent=7.5, student=u2, mp_amount=350.0,
                            date=now + timedelta(days=2))
        #m4.set_mp_amount()
        m4.set_end_and_money_to_add()
        m4.update_user_mp_amount()

        db.session.add_all([m1, m2, m3, m4])
        db.session.commit()

        self.assertEqual(u1.past_records.count(), 3)
        self.assertEqual(u2.past_records.count(), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
