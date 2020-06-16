from rest_framework.test import APITestCase
from .models import User


class UserTestCase(APITestCase):
    users = (
        ('test_user1', 'password1'),
        ('test_user2', 'password2')
    )

    def _login(self, login, password):
        response = self.client.post('/user/v1/login/', data={"username": login, "password": password})
        self.assertEqual(response.status_code, 200)
        return response.json()

    @staticmethod
    def _headers(access):
        return {
            "HTTP_AUTHORIZATION": f"Bearer {access}",
            # "content_type": "application/json"
        }

    def setUp(self) -> None:
        for credentials in self.users:
            User.objects.create_user(credentials[0], credentials[1])

    def test_login_1(self):
        login = 'test_user1'
        password = 'password1'
        response = self.client.post('/user/v1/login/', data={"username": login, "password": password})
        self.assertEqual(response.status_code, 200)

    def test_login_2(self):
        login = 'error_test_user1'
        password = 'password1'
        response = self.client.post('/user/v1/login/', data={"username": login, "password": password})
        self.assertEqual(response.status_code, 403)

    def test_login_3(self):
        login = 'test_user1'
        password = 'error_password1'
        response = self.client.post('/user/v1/login/', data={"username": login, "password": password})
        self.assertEqual(response.status_code, 403)

    def test_login_4(self):
        password = 'error_password1'
        response = self.client.post('/user/v1/login/', data={"password": password})
        self.assertEqual(response.status_code, 400)

    def test_login_5(self):
        login = 'test_user1'
        response = self.client.post('/user/v1/login/', data={"username": login})
        self.assertEqual(response.status_code, 400)

    def test_signup_1(self):
        username = 'nabakirov'
        password = 'password1'
        interests = 'interests in SC:GO'
        signup_response = self.client.post('/user/v1/signup/', data={
            "username": username,
            "password": password,
            "interests": interests
        })
        self.assertEqual(signup_response.status_code, 200)

        login_response = self.client.post('/user/v1/login/', data={'username': username, 'password': password})
        self.assertEqual(login_response.status_code, 200)

    def test_signup_2(self):
        username = 'test_user1'
        password = 'password1'
        signup_response = self.client.post('/user/v1/signup/', data={
            "username": username,
            "password": password,
        })
        self.assertEqual(signup_response.status_code, 400)

    def test_signup_3(self):
        password = 'password1'
        signup_response = self.client.post('/user/v1/signup/', data={
            "password": password,
        })
        self.assertEqual(signup_response.status_code, 400)

    def test_signup_4(self):
        username = 'username'
        signup_response = self.client.post('/user/v1/signup/', data={
            "username": username,
        })
        self.assertEqual(signup_response.status_code, 400)

    def test_refresh_1(self):
        login = 'test_user1'
        password = 'password1'
        data = self._login(login, password)
        refresh_token = data['refresh']
        response = self.client.post('/user/v1/refresh/', data={'refresh': refresh_token})
        self.assertEqual(response.status_code, 200)

    def test_refresh_2(self):
        refresh_token = 'invalid token'
        response = self.client.post('/user/v1/refresh/', data={'refresh': refresh_token})
        self.assertEqual(response.status_code, 401)

    def test_refresh_3(self):
        response = self.client.post('/user/v1/refresh/', data={})
        self.assertEqual(response.status_code, 400)

    def test_profile_1(self):
        login = 'test_user1'
        password = 'password1'
        data = self._login(login, password)
        headers = self._headers(data['access'])
        response = self.client.get('/user/v1/profile/', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], login)

    def test_profile_2(self):
        response = self.client.get('/user/v1/profile/')
        self.assertEqual(response.status_code, 401)

    def test_update_profile_1(self):
        login = 'test_user1'
        password = 'password1'
        interests = "new name"
        data = self._login(login, password)
        headers = self._headers(data['access'])
        body = {"interests": interests}
        response = self.client.patch('/user/v1/profile/', body, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['interests'], interests)

    def test_password_1(self):
        login = 'test_user2'
        password = 'password2'
        new_password = 'password3'
        data = self._login(login, password)
        headers = self._headers(data['access'])
        response = self.client.post('/user/v1/profile/password/', {
            'old_password': password,
            'new_password': new_password}, **headers)
        self.assertEqual(response.status_code, 200)
        self._login(login, new_password)

    def test_password_2(self):
        login = 'test_user2'
        password = 'password2'
        new_password = 'password4'
        data = self._login(login, password)
        headers = self._headers(data['access'])
        response = self.client.post('/user/v1/profile/password/', {
            'old_password': 'incorrect password',
            'new_password': new_password}, **headers)
        self.assertEqual(response.status_code, 400)

    def test_password_3(self):
        login = 'test_user2'
        password = 'password2'
        new_password = 'password4'
        data = self._login(login, password)
        headers = self._headers(data['access'])
        response = self.client.post('/user/v1/profile/password/', {
            'new_password': new_password}, **headers)
        self.assertEqual(response.status_code, 400)

    def test_password_4(self):
        login = 'test_user2'
        password = 'password2'
        data = self._login(login, password)
        headers = self._headers(data['access'])
        response = self.client.post('/user/v1/profile/password/', {
            'old_password': password}, **headers)
        self.assertEqual(response.status_code, 400)