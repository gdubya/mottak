from dotenv import load_dotenv
from starlette.testclient import TestClient
import sys
import psycopg2
import base64
import os
from main import app

import pytest
import pytest_dependency

client = TestClient(app)

test_uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

lorem_ipsum = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse at augue viverra, ultricies nunc at, tempor justo. Aliquam mattis justo eu libero semper, sit amet volutpat diam laoreet. In tellus dui, pellentesque nec convallis ac, mattis rhoncus est. Integer interdum nunc mauris, at interdum libero vehicula tincidunt. Aliquam eget molestie ex. Nulla rutrum tortor felis. Maecenas tempus, ligula id commodo egestas, nisl ipsum aliquet lectus, eu gravida neque tortor porta ex. Aenean varius, nunc tristique dictum dignissim, mauris mauris ultrices eros, vitae viverra massa quam quis neque. Sed accumsan facilisis velit non vestibulum. Curabitur vulputate, nunc ac venenatis imperdiet, ipsum arcu malesuada mi, eu rutrum risus tellus sit amet nunc. Integer tempus viverra tortor, non auctor diam vehicula elementum.'

load_dotenv()

def _delete_uuids():
    conn = psycopg2.connect(os.getenv('DSN'))
    cur = conn.cursor()
    cur.execute("""DELETE FROM attachments 
                    USING attachments AS a LEFT OUTER JOIN msgs on a.msgs_id = msgs.id 
                    WHERE msgs.archuuid = %s""", (test_uuid,))
    conn.commit()
    cur.execute("DELETE FROM msgs WHERE msgs.archuuid = %s", (test_uuid,))
    conn.commit()

@pytest.fixture(scope="session", autouse=True)
def delete_uuids():
    """Delete the test UUID from the database before and after"""
    _delete_uuids()
    yield
    _delete_uuids()
    return True


@pytest.mark.dependency()
def test_read_main():
    response = client.get("/")
    assert response.status_code == 404

@pytest.mark.dependency()
def test_send_msg1():
    msg = {
        "archuuid": test_uuid,
        "sender": "lorem ipsum generator",
        "time_recorded": "2020-02-17T16:42:48.093Z",
        "message": "1",
        "condition": "ok",
        "attachment": base64.b64encode(lorem_ipsum).decode('utf-8'),
        "attachment_mime": "text/plain",
        "attachment_name": "lorem.txt"
    }
    response = client.post("/ingest", json=msg)
    print(response)
    assert response.status_code == 200

@pytest.mark.dependency()
def test_send_msg2():
    msg = {
        "archuuid": test_uuid,
        "sender": "spam detector 2000",
        "time_recorded": "2020-02-17T18:42:48.093Z",
        "message": "2",
        "condition": "warning",
    }
    response = client.post("/ingest", json=msg)
    print(response.content)
    assert response.status_code == 200

@pytest.mark.dependency()
def test_send_msg3():
    msg = {
        "archuuid": test_uuid,
        "sender": "failure inducer 3000",
        "time_recorded": "2020-02-17T18:42:48.093Z",
        "message": "3",
        "condition": "error",
    }
    response = client.post("/ingest", json=msg)
    assert response.status_code == 200

def _get_lorem_ipsum(id : int):
    response = client.get(f'/attachments/{id}')
    assert response.content == lorem_ipsum

@pytest.mark.dependency(depends=["test_send_msg1", "test_send_msg2", "test_send_msg3"])
def test_get_logs():
    response = client.get(f'/query/{test_uuid}')
    r = response.json()
    assert len(r) == 3
    for logentry in r:
        if logentry['message'] == '1':
            assert logentry['attachment'] != 'null'
            assert logentry['condition'] == 'ok'
            _get_lorem_ipsum(logentry['attachment'])
        elif logentry['message'] == '2':
            assert logentry['condition'] == 'warning'
        elif logentry['message'] == '3':
            assert logentry['condition'] == 'error'
        else:
            print("Unknown message. Should be 1, 2 or 3.")
            assert 0