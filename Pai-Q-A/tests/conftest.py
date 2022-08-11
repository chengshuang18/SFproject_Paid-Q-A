"""
the entrypoint of unit-test
"""
from textwrap import dedent
import pytest
from api import create_app
from utils.ext import my_celery

pytest_plugins = "pytester"


@pytest.fixture(scope="session")
def app():
    app = create_app(my_celery=my_celery,
                     template_folder='../vue/dist',
                     static_folder='../vue/dist/static',
                     USERNAME='root',
                     PASSWORD='123456',
                     HOST='mysql:3306',
                     DB='mysql_for_unittest')
    # app = create_app(my_celery=my_celery)
    return app


@pytest.fixture
def appdir(testdir):
    app_root = testdir.tmpdir
    test_root = app_root.mkdir("tests")

    def create_test_module(code, filename="test_app.py"):
        my_file = test_root.join(filename)
        my_file.write(dedent(code), ensure=True)
        return my_file

    testdir.create_test_module = create_test_module

    testdir.create_test_module(
        """
        import pytest
        from api import create_app
        @pytest.fixture(scope="session")
        def application():
            app = create_app(template_folder='../vue/dist',
                             static_folder='../vue/dist/static',
                             USERNAME='root',
                             PASSWORD='123456',
                             HOST='mysql:3306',
                             DB= 'mysql_for_unittest')
            return app
    """,
        filename="conftest.py",
    )
    return testdir
