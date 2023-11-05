import pytest

import http_brute_force

def test_request_data():
    data = "userkey=^USER^&passkey=^PASS^&ANYTHING=anything&SOMETHINGELSE=somethingelse"
    assert http_brute_force.RequestData(data).format("user", "pass") == {"userkey": "user", "passkey":"pass","ANYTHING":"anything","SOMETHINGELSE":"somethingelse"}
