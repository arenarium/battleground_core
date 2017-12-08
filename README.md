[![Build Status](https://travis-ci.org/vincentropy/battleground.svg?branch=master)](https://travis-ci.org/vincentropy/battleground)

# battleground

A platform for light-weight multi-player online games. Easy creation of games, user-interfaces, and automated NPCs.

To get started all you need to do is write a simple python script that describes your game or NPC logic. Examples to follow.

### requirements:
- Vagrant

## Running games
### backend
which game should be played and what players and NPCs should be included can be configured in
```
config/*.json
```

To run this configuration, start the database server (if you have not yet done so):
```
docker-compose -f docker-compose.ui.yml up -d
```

then start the site runner:
```
python start.py --dynamic
```

or, if you want to use a different config file:
```
python start.py --config path/to/configfile.json
```

or, if you want to run the site continiously:
```
python start.py --dynamic -d
```

### frontend
first time?:
```
cd ui/frontend
npm install
```

to start a development server:
```
cd ui/frontend
npm start
```

then navigate to http://localhost:3000

## Getting Started With Development
We recommend you set up a virtual machine using [Vagrant](https://www.vagrantup.com/) and the provided Vagrantfile. Once you have Vagrant (and its requirements) installed you can use vagrant to run unit-tests.


### Unit tests

start the database server (if you have not yet done so):
```
docker-compose -f docker-compose-ui.yml up -d
```

for all the tests to pass, there should be some data in the database, to do this run
```
python start.py
```

next, to run tests:
```
pytest
```

## Developing your own games and NPCs

### adding an external agent from the command line to run locally

in order to add agents that are not part of the core platform you need:
- a python file that contains the code for your agent
- a game configuration file

examples of these can be found in
```
examples/external_agent/
```

first upload your agent code to the database:
```
python battleground/utils/save_agent.py \
--owner my_name \
--name my_external_agent \
--type basic_game \
examples/external_agent/basic_persistent_agent.py
```

then adjust create a game configuration you want to play for example like
```
examples/external_agent/game_config.json
```

start the game:
```
python start.py --config examples/external_agent/game_config.json
```
