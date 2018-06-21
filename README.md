[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e2e2e8f830f4cdd9b7f2425a070adc2)](https://www.codacy.com/app/0d26ae7a/battleground?utm_source=github.com&utm_medium=referral&utm_content=vincentropy/battleground&utm_campaign=badger)
[![Build Status](https://travis-ci.org/arenarium/battleground_core.svg?branch=master)](https://travis-ci.org/arenarium/battleground_core)
[![Documentation Status](https://readthedocs.org/projects/arenarium/badge/?version=latest)](https://arenarium.readthedocs.io/en/latest/?badge=latest)

# Arenarium: battleground-core

Arenarium is a platform for automated multi-player online games: write code to play.

To get started all you need to do is write a simple python script that describes your agent's logic.

**[Join Arenarium here.](http://www.arenarium.com/)**

To get started writing your own agent, head over to the
[agent development template](https://github.com/arenarium/battleground_agent_template)
for all the tools you need.

[Read the documentation here.](https://arenarium.readthedocs.io/)



## Getting Started With Development

If you want to contribute to the Arenarium core engine, read on.
If you're interested in contributing to the UI/UX, head over to [the UI repo](https://github.com/arenarium/battleground_ui).

### Core Tech Stack:
- Python 3
- MongoDB
- Docker
- Travis CI
- Vagrant


We recommend you set up a virtual machine using [Vagrant](https://www.vagrantup.com/) and the provided Vagrantfile. Once you have Vagrant (and its requirements) installed you can use vagrant to run unit-tests.


### Unit tests

Start the database server (if you have not yet done so):
```
docker-compose -f docker-compose.dev.yml up -d
```

For all the tests to pass, there should be some data in the database, to do this run
```
python battleground/utils/start.py
```

next, to run tests:
```
pytest
```

The battleground runs by default the basic game. You can change to the arena game by using a different config file:
```
python battleground/utils/start.py --config basic_arena_config.json
```
