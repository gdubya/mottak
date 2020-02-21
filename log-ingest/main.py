#!/usr/bin/env python

from starlette.responses import Response

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.responses import RedirectResponse, JSONResponse

from typing import Optional
from pydantic import BaseModel, ValidationError
from enum import Enum

import datetime
import os     # for ENV access
import uuid

import psycopg2
import psycopg2.extras

import base64

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
psycopg2.extras.register_uuid()

API_KEY = os.getenv('API_KEY')
API_KEY_NAME = os.getenv('API_KEY_NAME', default='access_token')
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', default="localtest.me")

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# todo:
# add error handling

class ConditionEnum(str, Enum):
    ok = 'ok'
    warning = 'warning'
    error = 'error'


class LogMessage(BaseModel):
    archuuid:        uuid.UUID
    sender:          str
    time_recorded:   datetime.datetime
    message:         str
    condition:       ConditionEnum
    attachment:      Optional[str]
    attachment_mime: Optional[str]
    attachment_name: Optional[str]



async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    # print(f"get_api_key:{api_key_query} : {api_key_header} : {api_key_cookie}")
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )



def _get_db_conn():
    if not os.environ.get('TEST'):
        conn = psycopg2.connect(os.getenv('DSN'))
        conn.autocommit = True
        return conn
    else:
        return None

dbc = _get_db_conn()

@app.get("/healthz")
async def health_check():
    cur = dbc.cursor()
    try:
        cur.execute('SELECT 1')
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database exception: {e}")
    return(Response("Hunky dory"))


@app.post("/ingest")
def ingest(msg: LogMessage, api_key: APIKey = Depends(get_api_key)):
    cur = dbc.cursor()
    id_att = None
    cur.execute("""INSERT INTO msgs (archuuid, sender, time_recorded, message, condition) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (msg.archuuid, msg.sender, msg.time_recorded, msg.message, msg.condition))
    id_msg = cur.fetchone()[0]
    if (msg.attachment):
        content = base64.b64decode(msg.attachment)
        cur.execute("""INSERT into attachments (msgs_id, name, mime, content)
            VALUES (%s, %s, %s, %s)
            RETURNING id""",
                    (id_msg, msg.attachment_name, msg.attachment_mime, content))
        id_att = cur.fetchone()[0]
    return {"status": "Log message ingested.",
            "id":  id_msg,
            "attachment_id": id_att}


@app.get("/query/{UUID}")
def query(UUID: uuid.UUID, api_key: APIKey = Depends(get_api_key)):
    cur = dbc.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""SELECT 
                   msgs.id, sender, message, time_recorded, timestamp, condition, attachments.id attachment
                   FROM msgs 
                   LEFT JOIN attachments on msgs.id = attachments.msgs_id
                   WHERE archuuid=%s""", (UUID,))
    ret = cur.fetchall()
    if not len(ret):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No entries found for {UUID}")
    return ret


@app.get("/attachments/{id}")
def get_attachment(id: int, api_key: APIKey = Depends(get_api_key) ):
    cur = dbc.cursor()
    cur.execute("SELECT name,mime,content FROM attachments where id=%s", (id,))
    if (cur.rowcount == 0):
        raise HTTPException(
            status_code=404, detail=f"Attachment {id} not found")

    name, mime, content = cur.fetchone()
    headers = {}
    headers['Content-Disposition'] = f'attachment; filename="{name}"'
    return Response(content=content.tobytes(),
                    headers=headers,
                    media_type=mime)


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


@app.get("/secure")
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        {'message': "Hello secure world"}
    )
    return response
