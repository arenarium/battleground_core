import pika
import uuid

class RefereeHandler():

    def __init__(self,agent_name):
        self.agent_name = agent_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.__on_response, no_ack=True,
                                   queue=self.callback_queue)


    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = int(body)



    def move(self, param):
        routing_key = None

        routing_key="rpc_queue_"+self.agent_name
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         type='move'
                                         ),
                                   body=param)
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)