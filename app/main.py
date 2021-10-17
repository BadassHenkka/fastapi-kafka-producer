from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from kafka.errors import KafkaConnectionError

from app.config import settings
from app.producer.user_analytics_producer import user_producer
from app.websocket.manager import ConnectionManager


app = FastAPI(title="fastapi-kafka-producer", redoc_url="/docs", docs_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    try:
        await user_producer.start()
    except KafkaConnectionError as err:
        print(f"Error on producer start: {err}")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await user_producer.stop()
    except KafkaConnectionError as err:
        print(f"Error on producer stop: {err}")


@app.websocket("/ws/analytics")
async def ws_endpoint(websocket: WebSocket):
    ws_manager = ConnectionManager()
    await ws_manager.connect(websocket)

    try:
        while True:
            data_dict = await websocket.receive_json()
            user_action = data_dict.get('analytics').get('data')

            await user_producer.send(settings.USER_ANALYTICS_KAFKA_TOPIC, user_action)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
