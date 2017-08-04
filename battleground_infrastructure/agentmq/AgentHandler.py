import pika

class AgentHandler():

    def __init__(self):
        self.__move = None
        self.__agent_id = None
        self.__functions = {}

    def __on_request(self,ch, method, props, body):
        response = selft.__functions[props.type](str(body))

        ch.basic_publish(exchange='',
             routing_key=props.reply_to,
             properties=pika.BasicProperties(correlation_id = \
                                                 props.correlation_id,
                                             type=props.type),
             body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def register_function(self,func_name,func):
        self.__functions[func_name] = func


    def start(self,agent_id):
        self.__agent_id=agent_id
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue="rpc_queue_"+self.__agent_id)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.__on_request, queue="rpc_queue_"+self.__agent_id)
        channel.start_consuming()