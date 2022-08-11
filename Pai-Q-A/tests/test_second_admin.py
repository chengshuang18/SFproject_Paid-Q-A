"""
test the api of check system
"""
from api.admin.model import Admin, SystemConfigration


def insert_basic_param():
    # add basic parameters
    Admin.insert_root()
    SystemConfigration.insert_sysparam()


class TestAdmin():
    @staticmethod
    def test_initial(client):
        insert_basic_param()

    @staticmethod
    def test_add_admin(client):
        """
        Test normal post method.
        """
        # 添加用户zhangsan
        data = {"username": "zhangsan"}
        response = client.post('/api/admin/addadmin', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        originalpassword = response.json['password']
        # 为zhangsan修改密码
        data = {"username": "zhangsan", "originalpassword": originalpassword, "newpassword": "123456"}
        response = client.post('/api/admin/changepassword', data=data)
        # 再次添加zhangsan
        data = {"username": "zhangsan"}
        response = client.post('/api/admin/addadmin', data=data)
        assert response.status_code == 403
        assert response.json['state'] == 'username has already existed!'
        # 添加用户lisi
        data = {"username": "lisi"}
        response = client.post('/api/admin/addadmin', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        originalpassword = response.json['password']
        # 为lisi修改密码
        data = {"username": "lisi", "originalpassword": originalpassword, "newpassword": "123456"}
        response = client.post('/api/admin/changepassword', data=data)

    @staticmethod
    def test_login(client):
        """
        Test normal post method.
        """

        # Login Verification Error!
        data = {"username": "zhangsan", "password": "12345"}
        response = client.post('/api/admin/login', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'Login Verification Error!'

        # User does not exist!
        data = {"username": "zhangsi", "password": "123456"}
        response = client.post('/api/admin/login', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'Login Verification Error!'

        # Email already exists!
        data = {"username": "zhangsan", "password": "123456"}
        response = client.post('/api/admin/login', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

    @staticmethod
    def test_sysparam(client):

        """
        Test normal get method(SendSysParam).
        """
        response = client.get('/api/admin/sendsysparam')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

        """
        Test normal post method(SystemConfig).
        """
        data = {"lowest_prices": 20,
                "top_prices": 200,
                "wait_receive": 20,
                "wait_answer": 20,
                "times_AQ": 20,
                "time_service": 20}
        response = client.post('/api/admin/systemconfig', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

        # check the modification result
        response = client.get('/api/admin/sendsysparam')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        assert response.json['doc'] == {"top_prices": 200,
                                        "wait_answer": 20,
                                        "time_service": 20,
                                        "wait_receive": 20,
                                        "lowest_prices": 20,
                                        "times_AQ": 20}

    @staticmethod
    def test_admin_management(client):
        """
        Test normal post method(AdminPermission).
        """
        data = {"username": "zhangsa", "field": 2}  # 用户名不存在
        response = client.post('/api/admin/adminpermission', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'username does not exist!'

        data = {"username": "zhangsan", "field": 2}
        response = client.post('/api/admin/adminpermission', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'

        """
        Test normal get method(SendAdminInfo).
        """
        response = client.get('/api/admin/sendadmininfo')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        assert len(response.json['userList']) == 2  # 包含zhangsan和lisi的列表

        """
        Test normal get method(DeleteAdmin).
        """
        data = {"username": "zhangsa"}  # 用户名不存在
        response = client.get('/api/admin/deleteadmin', data=data)
        assert response.status_code == 401
        assert response.json['state'] == 'admin does not exist!'
        # 删除寻找不到用户名，此时管理员数量（非root）依然是两个
        response = client.get('/api/admin/sendadmininfo')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        assert len(response.json['userList']) == 2  # 包含zhangsan和lisi的列表

        data = {"username": "zhangsan"}  # 删除zhangsan
        response = client.get('/api/admin/deleteadmin', data=data)
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        # 删除管理员张三，此时管理员数量（非root）为1个
        response = client.get('/api/admin/sendadmininfo')
        assert response.status_code == 200
        assert response.json['state'] == 'Successful Operation!'
        assert len(response.json['userList']) == 1  # 包含zhangsan和lisi的列表
