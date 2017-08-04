## How-to

### DockerfileAgent image and AgentHandler
This image create a docker container in which an AgentHandler is available from python
AgentHandler can be used by the agent to register any method he wants to expose

ex.

```python
from AgentHandler import AgentHandler

agentHandler = AgentHandler()
agentHandler.register_function("method_name",method_function)
agentHandler.start("agent_id")
```


### DockerfileReferee image and RefereeHandler
This image create a docker container in which a RefereeHandler is available from python
RefereeHandler can be used by the referee (aka game runner?) to invoke different methods 
from the pool of available agents

ex.
```python
from RefereeHandler import RefereeHandler

referee_handler = RefereeHandler()

#invoke the method move on the agent with agent_id ag1
response_ag1 = referee_handler.call("ag1","move")

```


#### A real and complete (though really simple) example is available in this folder.

In order to launch it you first  **need to change the paths** of the volumes mapped in the 
docker-compose.yml then launch with docker-compose up