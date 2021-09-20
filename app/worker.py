from asyncworker import App
from asyncworker.connections import AMQPConnection


amqp_conn = AMQPConnection(
    hostname="127.0.0.1",
    username="admin", 
    password="admin", 
    prefetch_count=256
    )

app = App(connections=[amqp_conn])

@app.amqp.consume(["codementoring.students"])
async def drain_handler(message):
    print(message)


app.run()