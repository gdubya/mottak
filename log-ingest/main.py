#!/usr/bin/env python

from fastapi import FastAPI, HTTPException
from starlette.responses import Response

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


# todo:
# add error handling
# make tests.

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


@app.post("/ingest")
def ingest(msg: LogMessage):

    conn = psycopg2.connect(os.getenv('DSN'))
    cur = conn.cursor()

    id_att = None

    cur.execute("""INSERT INTO msgs (archuuid, sender, time_recorded, message, condition) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (msg.archuuid, msg.sender, msg.time_recorded, msg.message, msg.condition ))
    conn.commit()
    id_msg = cur.fetchone()[0]

    if (msg.attachment):
        content = base64.b64decode(msg.attachment)
        cur.execute("""
            INSERT into attachments (msgs_id, name, mime, content)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """,
                    (id_msg, msg.attachment_name, msg.attachment_mime, content))
        conn.commit()
        id_att = cur.fetchone()[0]


    return {"status": "Log message ingested.",
            "id":  id_msg,
            "attachment_id": id_att }


@app.get("/query/{UUID}")
def query(UUID: uuid.UUID):
    conn = psycopg2.connect(os.getenv('DSN'))
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""SELECT 
                   msgs.id, sender, message, time_recorded, timestamp, condition, attachments.id attachment
                   FROM msgs 
                   LEFT JOIN attachments on msgs.id = attachments.msgs_id
                   WHERE archuuid=%s""", (UUID,))
    ret = cur.fetchall()
    if not len(ret):
        raise HTTPException(
            status_code=404, detail=f"No entries found for {UUID}")
    return ret


@app.get("/attachments/{id}")
def get_attachment(id: int):
    conn = psycopg2.connect(os.getenv('DSN'))
    cur = conn.cursor()
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
