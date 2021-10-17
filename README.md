### fastapi-kafka-producer

Simple kafka producer created with aiokafka and used together with fastapi websocket endpoint. The example use case here is to send user analytics from frontend to a kafka cluster.

[Here's an example frontend](https://github.com/BadassHenkka/shared-worker) that connects to this server using a [SharedWorker](https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker) + Websocket.
