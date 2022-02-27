import pytest


@pytest.mark.django_db
def test_login(selenium, chromedriver_fixture):

    selenium.get("http://127.0.0.1:8000/deets/test-1")
    import pdb

    pdb.set_trace()
