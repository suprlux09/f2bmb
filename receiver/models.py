import os
from dotenv import load_dotenv
from peewee import (
    Model, CharField, BooleanField, DateTimeField,
    ForeignKeyField, AutoField, CompositeKey
)
from playhouse.mysql_ext import MySQLDatabase

# Load environment variables
load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_passwd = os.getenv("DB_PASSWD")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))

# MySQL 데이터베이스 연결 설정
database = MySQLDatabase(
    db_name,
    user=db_user,
    password=db_passwd,
    host=db_host,
    port=db_port
)

class BaseModel(Model):
    class Meta:
        database = database

# Node 테이블에 해당하는 모델
class Node(BaseModel):
    node_name = CharField(max_length=50, primary_key=True)

    class Meta:
        table_name = 'node'

# DetectedIP 테이블에 해당하는 모델
class DetectedIP(BaseModel):
    ip_addr = CharField(max_length=50, primary_key=True)
    country = CharField(max_length=50, null=True)

    class Meta:
        table_name = 'detected_ip'

# Rule 테이블에 해당하는 모델
class Rule(BaseModel):
    filter = CharField(max_length=50)
    node_name = ForeignKeyField(Node, backref='rules', column_name='node_name')
    notify_found = BooleanField()
    notify_ban = BooleanField()

    class Meta:
        table_name = 'rule'
        primary_key = CompositeKey('filter', 'node_name')

# Log 테이블에 해당하는 모델
class Log(BaseModel):
    log_id = AutoField()
    detected_at = DateTimeField()
    filter = ForeignKeyField(Rule, backref='logs', column_name='filter')
    node_name = ForeignKeyField(Node, backref='logs', column_name='node_name')
    ip_addr = ForeignKeyField(DetectedIP, backref='logs', column_name='ip_addr')
    action = CharField(max_length=10)

    class Meta:
        table_name = 'log'
        indexes = (
            (('detected_at',), False),  # Non-unique index on detected_at
        )
