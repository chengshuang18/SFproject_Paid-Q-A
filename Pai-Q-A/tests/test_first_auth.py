"""
test the api of user management
"""


class TestAuth():
    @staticmethod
    def test_register(client):
        """
        Test normal post method.
        """
        photo = open('tests/logo.png', 'rb')
        data = {"username": "zhangsan", "password": "123", "email": "123@qq.com", "photo": photo}
        response = client.post('/api/register', data=data)
        assert response.status_code == 201
        assert response.json['state'] == 'Register Success!'

        # User already exists!
        photo = open('tests/logo.png', 'rb')
        data = {"username": "zhangsan", "password": "123", "email": "12345@qq.com", "photo": photo}
        response = client.post('/api/register', data=data)
        assert response.status_code == 403
        assert response.json['state'] == 'Username or email already exits!'

        # Email already exists!
        photo = open('tests/logo.png', 'rb')
        data = {"username": "lisi", "password": "123", "email": "123@qq.com", "photo": photo}
        response = client.post('/api/register', data=data)
        assert response.status_code == 403
        assert response.json['state'] == 'Username or email already exits!'

    @staticmethod
    def test_login(client):
        """
        Test normal post method.
        """
        # "zhangsan" has already rigistered.
        data = {"username": "zhangsan", "password": "123"}
        response = client.post('/api/login', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

        # user does not exist!
        data = {"username": "lisi", "password": "123"}
        response = client.post('/api/login', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'Login Verification Error!'

        # password verification Error!
        data = {"username": "zhangsan", "password": "123456"}
        response = client.post('/api/login', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'Login Verification Error!'

    @staticmethod
    def test_upgrade(client):
        """
        Test normal post method.
        """
        # "lisi" has not rigistered.
        data = {"username": "lisi", "resume": "hello, i am a math teacher!", "field": 1, "price": 19.9}
        response = client.post('/api/upgrade', data=data)
        assert response.status_code == 402
        assert response.json['state'] == 'User Not Exist!'

        # "lisi" has not rigistered.
        data = {"username": "zhangsan", "resume": "hello, i am a math teacher!", "field": 1, "price": 19.9}
        response = client.post('/api/upgrade', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'User Upgrade Success!'

    @staticmethod
    def test_sendansinfo(client):
        """
        Test normal get method.
        """
        # register and upgrade some users
        photo = open('tests/logo.png', 'rb')
        data = {"username": "lisi", "password": "123", "email": "1234@qq.com", "photo": photo}
        response = client.post('/api/register', data=data)
        photo = open('tests/logo.png', 'rb')
        data = {"username": "wangwu", "password": "123", "email": "12345@qq.com", "photo": photo}
        response = client.post('/api/register', data=data)

        data = {"username": "lisi", "resume": "hello, i am a math teacher!", "field": 1, "price": 19.9}
        response = client.post('/api/upgrade', data=data)
        data = {"username": "wangwu", "resume": "hello, i am a math teacher!", "field": 1, "price": 19.9}
        response = client.post('/api/upgrade', data=data)

        # User already exists!
        response = client.get('/api/sendansinfo')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        assert response.json['res'][0]['username'] == 'zhangsan'
        assert response.json['res'][1]['username'] == 'lisi'
        assert response.json['res'][2]['username'] == 'wangwu'

    @staticmethod
    def test_walletmanagement(client):
        """
        Test normal get method.
        """
        # "zhangsan" "lisi" "wangwu" have already rigistered.
        data = {"username": "zhangsan"}
        response = client.get('/api/walletmanagement', data=data)
        assert response.status_code == 200
        assert response.json['balance'] == 0
        assert response.json['state'] == 'Successful Operation!'

        # user does not exist!
        data = {"username": "maliu"}
        response = client.get('/api/walletmanagement', data=data)
        assert response.status_code == 402
        assert response.json['state'] == 'User Empty!'

        """
        Test normal post method.
        """
        # "zhangsan" "lisi" "wangwu" have already rigistered.
        data = {"username": "zhangsan", "money": 200}
        response = client.post('/api/walletmanagement', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        # query verification result
        data = {"username": "zhangsan"}
        response = client.get('/api/walletmanagement', data=data)
        assert response.json['balance'] == 200

        # user does not exist!
        data = {"username": "maliu", "money": 200}
        response = client.post('/api/walletmanagement', data=data)
        assert response.status_code == 402
        assert response.json['state'] == "User Not Exist!"

    @staticmethod
    def test_genusersig(client):
        """
        Test normal get method.
        """
        # register and upgrade some users
        data = {"username": "lisi"}
        response = client.get('/api/genusersig', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

    @staticmethod
    def test_senduserlist(client):
        """
        Test normal get method.
        """
        data = {"username": "zhangsan"}
        response = client.get('/api/senduserlist', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

        data = {"username": "lisi"}
        response = client.get('/api/senduserlist', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
