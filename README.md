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
to start a development server:
```
cd ui/frontent
npm start
```

then navigate to http://localhost:3000

## Getting Started With Development
We reccomend you set up a virtual machine using [Vagrant](https://www.vagrantup.com/) and the provided Vagrantfile. Once you have Vagrant (and its requirements) installed you can use vagrant to run unit-tests.


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

...More to come.
