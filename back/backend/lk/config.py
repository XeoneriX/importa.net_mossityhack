# -*- coding: utf-8 -*-
import os

DEBUG: bool = True
JSON_AS_ASCII: bool = False
SECRET_KEY: str = os.environ.get("FLASK_SECRET_KEY", "MYDEFAULTKEY")
SQLALCHEMY_DATABASE_URI: str = os.environ.get(
    "FLASK_SQLALCHEMY_URI",
    "postgresql+psycopg2://{user}:{pass}@{host}/{db}".format(
        **{
            "user": "importanet",
            "pass": "kC6eLNEeiPWRtctC6",
            "host": "148.253.62.46",
            "db": "postgres",
        }
    ),
)
