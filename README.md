# battleground

A platform for light-weight multi-player online games. Easy creation of games, user-interfaces, and automated NPCs.

To get started all you need to do is write a simple python script that describes your game or NPC logic. Examples to follow.

### requirements:
- Vagrant

## Running a game
which game should be played and what players and NPCs should be included can be configured in
```
config/basic_config.json
```

To run this configuration, start the database server (if you have not yet done so):
```
docker-compose -f docker-compose-ui.yml up -d
```

then start the site runner:
```
python start.py
```

or, if you want to use a different config file:
```
python start.py --config path/to/configfile.json
```

## Getting Started With Development
We reccomend you set up a virtual machine using [Vagrant](https://www.vagrantup.com/) and the provided Vagrantfile. Once you have Vagrant (and its requirements) installed you can open a terminal and in the project folder run

```
vagrant up
```

this will provision a virtual machine and install all the dependencies for battleground in the virtual machine. Once this completes you can run

```
vagrant ssh
```

to connect to the virtual machine. Your default path in the virtual machine is /vagrant, this folder is linked with the project folder on the host machine: any changes made in the virtual machine here will also change the corresponding file on the host machine.

when you're done, stop the virtual machine.

```
vagrant halt
```


### Unit tests

start the database server (if you have not yet done so):
```
docker-compose -f docker-compose-ui.yml up -d
```

to run tests:
```
pytest
```

## Developing your own games and NPCs

...More to come.
