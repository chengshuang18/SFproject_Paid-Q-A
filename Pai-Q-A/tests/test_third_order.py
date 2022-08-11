"""
Test the api for order
"""


class TestOrder():
    @staticmethod
    def test_addorder(client):
        """
        Test normal post method.
        """

        data = {"title": "question4",
                "questioner": "zhangsan",
                "answerer": "lisi",
                "content": "The secret of universe"}
        response = client.post('/api/ask', data=data)
        assert response.status_code == 201
        assert response.json['state'] == 'ASK SUCCESS'

    @staticmethod
    def test_orderlist(client):
        """
        Test normal post method.
        """
        response = client.get('/api/orders')
        assert response.status_code == 200

    @staticmethod
    def test_refuseask(client):
        """
        Test normal post method.
        """
        data = {"order_id": 1}
        response = client.post('/api/refuseask', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_checkorderlist(client):
        """
        Test normal post method.
        """
        data = {"field": 1}
        response = client.get('/api/checkorderlist', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_selectorderbyanswerer(client):
        """
        Test normal post method.
        """
        # answerer not match
        data = {"answerer": "Alice"}
        response = client.get('/api/selectorderbyanswerer', data=data)
        assert response.status_code == 500

        # correct
        data = {"answerer": "lisi"}
        response = client.get('/api/selectorderbyanswerer', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_selectorderbyid(client):
        """
        Test normal post method.
        """
        data = {"order_id": 1}
        response = client.get('/api/selectorderbyid', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_cancelquestion(client):
        """
        Test normal post method.
        """
        # success operation
        data = {"order_id": 1}
        response = client.post('/api/cancelquestion', data=data)
        assert response.status_code == 200

        # data empty
        data = {"order_id": 9}
        response = client.post('/api/cancelquestion', data=data)
        assert response.status_code == 402

    @staticmethod
    def test_hiddencheckorder(client):
        """
        Test normal post method.
        """
        data = {"order_id": 1}
        response = client.post('/api/hiddencheckorder', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_checkorder(client):
        """
        Test normal post method.
        """
        data = {"order_id": 1, "check_mark": 1}
        response = client.post('/api/checkorder', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_selectorderbyquestioner(client):
        """
        Test normal post method.
        """
        data = {"questioner": "zhangsan"}
        response = client.get('/api/selectorderbyquestioner', data=data)
        assert response.status_code == 200

    @staticmethod
    def test_completeorder(client):
        """
        Test normal post method.
        """
        data = {"order_id": 1}
        response = client.get('/api/completeorder', data=data)
        assert response.status_code == 200
