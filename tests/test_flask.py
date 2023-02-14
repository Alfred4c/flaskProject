import pytest, requests
from app import *
class Test_flask:
    def setup(self):
        
        self.app = app
        app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_add(self):
        resp1 = self.client.post("/add", data={"text": "akjsdhaja"})
        resp2 = self.client.post(
            "/add",
            data={"text": "123456789123456789123456789123456789123456789123456789"},
        )

        assert resp1.status_code == 302 and resp2.status_code == 404

    def test_finish(self):
        resp1 = self.client.post("/finished", data={"id": 41})
        assert resp1.status_code == 302

    def test_delete(self):
        resp = self.client.post("/delete", data={"id": 41})
        assert resp.status_code == 302

    def teardown(self):
        pass


if __name__ == "__main__":
    pytest.main("-s test_flask.py")
