import pika
from random import randint
import time
from AgentHandler import AgentHandler


def action(*args):
    return randint(1,10)

if __name__=="__main__":
    time.sleep(15)
    agentHandler = AgentHandler()
    agentHandler.register_function("move",action)
    agentHandler.start("ag1")
