import os
import unittest

basedir = os.path.abspath(os.path.dirname(__file__))

from app import app, db

TEST_DB = 'test.db'
 

 ##############################################


class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        def tearDown(self):
            pass

    def test_index_route(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_groups_route(self):
        response = self.app.get('/groups', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_joingroup_route(self):
        response = self.app.get('/joingroup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_addingentry_route(self):
        response = self.app.get('/addingentry', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_more_route(self):
        response = self.app.get('/more', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_index_route(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_groups_route(self):
        response = self.app.get('/groups', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_joingroup_route(self):
        response = self.app.get('/joingroup', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_addingentry_route(self):
        response = self.app.get('/addingentry', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_more_route(self):
        response = self.app.get('/more', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_signup_route(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)

    def test_invalid_login_route(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertNotEqual(response.status_code, 400)


##############################################


    
class TestAccounts(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        def tearDown(self):
            pass

    def signup(self, username, email, password, confirmPassword):
        return self.app.post(
            '/signup',
            data=dict(username=username, email=email, password=password, confirmPassword=confirmPassword),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
    )

    def test_invalid_signup_password_invalid(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'Hello', 'Hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be at least 8 characters long.', response.data)

    def test_signup_email_invalid(self):
        response = self.signup('user101', 'examplename12', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)

    def test_signup_confirmPassword_invalid(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'blue1638', 'Hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_signup_username_invalid(self):
        response = self.signup(' ', 'examplename12@gmail.com', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_signup_password(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Field must be at least 8 characters long.', response.data)

    def test_signup_email(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid email address.', response.data)

    def test_signup_confirmPassword(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Field must be equal to password.', response.data)

    def test_signup_username(self):
        response = self.signup('user101', 'examplename12@gmail.com', 'blue1638', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'This field is required.', response.data)

    def test_invalid_login_email(self):
        response = self.login('examplename12', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)

    def test_login_email(self):
        response = self.login('examplename12@gmail.com', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid email address.', response.data)
        
    def test_invalid_login_password(self):
        response = self.login('examplename12@gmail.com', 'blue1638888')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wrong Username or Password', response.data)

    def test_invalid_login_email_two(self):
        response = self.login('thisemaildoesntexist@gmail.com', 'blue1638')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wrong Username or Password', response.data)


##############################################
    




    

if __name__ == "__main__":
    unittest.main()