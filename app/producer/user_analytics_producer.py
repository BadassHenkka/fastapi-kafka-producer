from os import getcwd
import asyncio
import json
from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from app.config import settings


# make sure you have the required credential files
# in the credentials folder
credentials_folder = f"{getcwd()}/app/credentials"
cafile = f"{credentials_folder}/ca.pem"
certfile = f"{credentials_folder}/service.cert"
keyfile = f"{credentials_folder}/service.key"

kafka_ssl_context = create_ssl_context(
    cafile=cafile,  # CA used to sign certificate.
    certfile=certfile,  # Signed certificate
    keyfile=keyfile,  # Private Key file of `certfile` certificate
)


loop = asyncio.get_event_loop()


user_producer = AIOKafkaProducer(
    loop=loop,
    client_id=settings.KAFKA_CLIENT_ID,
    bootstrap_servers=settings.KAFKA_SERVICE_URI,
    security_protocol="SSL",
    ssl_context=kafka_ssl_context,
    value_serializer=lambda val: json.dumps(val).encode('ascii'),
    key_serializer=lambda key: json.dumps(key).encode('ascii')
)
