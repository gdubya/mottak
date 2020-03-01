#!/usr/bin/env python

from starlette.testclient import TestClient
import pytest
from requests.auth import AuthBase
import os
import base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print(f'Failed to load dotenv. Assuming we are running in production')


from app.main import app

# Super simple auth driver, injects a header with a key.

class KeyAuth(AuthBase):
    def __init__(self):
        self.key = os.getenv('API_KEY')
        self.header = os.getenv('API_KEY_NAME', 'access_token')

    def __call__(self, r):
        r.headers[self.header] = self.key
        return r

@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture
def testuuid() -> str:
    return "3fa85f64-5717-4562-b3fc-2c963f66afa6"


@pytest.fixture
def loremipsum() -> str:
    return b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse at augue viverra, ultricies nunc at, tempor justo. Aliquam mattis justo eu libero semper, sit amet volutpat diam laoreet. In tellus dui, pellentesque nec convallis ac, mattis rhoncus est. Integer interdum nunc mauris, at interdum libero vehicula tincidunt. Aliquam eget molestie ex. Nulla rutrum tortor felis. Maecenas tempus, ligula id commodo egestas, nisl ipsum aliquet lectus, eu gravida neque tortor porta ex. Aenean varius, nunc tristique dictum dignissim, mauris mauris ultrices eros, vitae viverra massa quam quis neque. Sed accumsan facilisis velit non vestibulum. Curabitur vulputate, nunc ac venenatis imperdiet, ipsum arcu malesuada mi, eu rutrum risus tellus sit amet nunc. Integer tempus viverra tortor, non auctor diam vehicula elementum.'


@pytest.mark.dependency
def test_stupid():
    print("Out main tests are OK")
    assert 0 == 0


@pytest.mark.dependency()
def test_read_root(client: TestClient):
    response = client.get("/", )
    assert response.status_code == 404


@pytest.mark.dependency()
def test_read_health(client: TestClient):
    response = client.get("/")


@pytest.mark.dependency()
def test_send_msg1(mocker, client: TestClient,
                   testuuid: str,
                   loremipsum):
    mock = mocker.patch('app.main.dbc')
    mock.cursor.execute = mocker.MagicMock(return_value=15)
    mock.side_effect = Exception

    msg = {
        "archuuid": testuuid,
        "sender": "lorem ipsum generator",
        "time_recorded": "2020-02-17T16:42:48.093Z",
        "message": "1",
        "condition": "ok",
        "attachment": base64.b64encode(loremipsum).decode('utf-8'),
        "attachment_mime": "text/plain",
        "attachment_name": "lorem.txt"
    }
    response = client.post("/ingest", json=msg, auth=KeyAuth())
    assert response.status_code == 200


@pytest.mark.dependency()
def test_send_msg2(mocker,
                   client: TestClient,
                   testuuid: str,
                   loremipsum):
    mock = mocker.patch('app.main.dbc')
    mock.cursor.execute = mocker.MagicMock(return_value=16)
    mock.side_effect = Exception

    msg = {
        "archuuid": testuuid,
        "sender": "spam detector 2000",
        "time_recorded": "2020-02-17T18:42:48.093Z",
        "message": "2",
        "condition": "warning",
    }
    response = client.post("/ingest", json=msg, auth=KeyAuth())
    assert response.status_code == 200


@pytest.mark.dependency()
def test_send_msg3(mocker,
                   client: TestClient,
                   testuuid: str,
                   loremipsum):
    mock = mocker.patch('app.main.dbc')
    mock.cursor.execute = mocker.MagicMock(return_value=17)
    mock.side_effect = Exception

    msg = {
        "archuuid": testuuid,
        "sender": "failure inducer 3000",
        "time_recorded": "2020-02-17T18:42:48.093Z",
        "message": "3",
        "condition": "error",
    }
    response = client.post("/ingest", json=msg, auth=KeyAuth())
    assert response.status_code == 200


@pytest.fixture
def query_response() -> list:

    return [{'attachment': 74,
             'condition': 'ok',
             'id': 257,
             'message': '1',
             'sender': 'lorem ipsum generator',
             'time_recorded': '2020-02-17T17:42:48.093000+01:00',
             'timestamp': '2020-02-21T18:15:15.118433+01:00'},
            {'attachment': None,
             'condition': 'warning',
             'id': 258,
             'message': '2',
             'sender': 'spam detector 2000',
             'time_recorded': '2020-02-17T19:42:48.093000+01:00',
             'timestamp': '2020-02-21T18:15:15.132681+01:00'},
            {'attachment': None,
             'condition': 'error',
             'id': 259,
             'message': '3',
             'sender': 'failure inducer 3000',
             'time_recorded': '2020-02-17T19:42:48.093000+01:00',
             'timestamp': '2020-02-21T18:15:15.140153+01:00'}]


@pytest.fixture
def attachment_resp( loremipsum ) -> list:
    return ['lorem.txt', 'text/plain', memoryview(loremipsum)]

def get_lorem_ipsum(c, id: int, loremipsum: str):
    response = c.get(f'/attachments/{id}', auth=KeyAuth())
    assert response.status_code == 200
    assert response.content == loremipsum

@pytest.mark.dependency(depends=["test_send_msg1", "test_send_msg2", "test_send_msg3"])
def test_get_logs(mocker,
                  testuuid : str,
                  loremipsum : loremipsum,
                  client : TestClient,
                  query_response: list,
                  attachment_resp: list):
    mock = mocker.patch('app.main.dbc')
    mock.cursor.return_value.fetchall.return_value = query_response
    mock.cursor.return_value.fetchone.return_value = attachment_resp
    response = client.get(f'/query/{testuuid}', auth=KeyAuth())
    r = response.json()
    # pp.pprint(r)
    assert len(r) == 3
    for logentry in r:
        if logentry['message'] == '1':
            assert logentry['attachment'] != 'null'
            assert logentry['condition'] == 'ok'
            get_lorem_ipsum(client, logentry['attachment'], loremipsum)
        elif logentry['message'] == '2':
            assert logentry['condition'] == 'warning'
        elif logentry['message'] == '3':
            assert logentry['condition'] == 'error'
        else:
            print("Unknown message. Should be 1, 2 or 3.")
            assert 0
