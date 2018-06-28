.. Arenarium documentation master file, created by
   sphinx-quickstart on Sat Jun 16 09:52:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Arenarium!
=====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Getting Started
---------------

You are probably here because you want to get started playing `Arenarium <http://www.arenarium.com/>`_.
Arenarium is a game you play by writing code, and this guide explains how.

Rules
*********

The rules of the basic Arena game are simple. The game starts with two or more gladiators (agents)
inside a dungeon. On each turn, your gladiator has the option between three types of moves:

1. **Move** to a neighboring grid points.
#. **Attack** another gladiator within range.
#. **Stay** in the same place (and do nothing).

A fourth move will be coming soon :

(4.) **Boost** a stat of your gladiator to improve its accuracy, evasion, damage, protection or speed.

**Objective:** The last gladiator to survive wins.

**Score:** For each gladiator that your gladiator kills it receives one point. However, the score is set to zero if your gladiator dies.

Under the Hood
******************

On a more detailed level, the Arena game is operating on an event queue system.
Each move is queued and then processed after some time, which is influenced by a gladiator's speed.
The base speed is 23 ticks. This is how much 'time' it takes for a queued move to resolve.
After a move is resolved, the agent can queue the next move and so on.

Attacks are handled on a competitive d10 dice roll.
The attacker and defender each roll a die, to which attacker adds their accuracy (base 0) and the defender their evasion (base 0).
If the attacker's total is at least as high as the defender's one, the attack hits.
The amount of lost hit points of the defender is given by subtracting the defender's protection (base 0) from the attacker's damage (base 5), to a minimum of zero.

(Coming soon:) Boosts let you change certain stats of your gladiator. Improve your accuracy or evasion, hit harder by adding some points to your damage, reduce the amount of damage you take by strengthening your protection, or get faster by improving your speed.
For that, each gladiator has ten spirit points, which can be allocated to boost the aforementioned stats.
Raising a stat by one point costs one spirit point, raising it by two however costs three, raising it by three costs six, and raising it by four points costs ten spirit points.
You can also lower previously raised stats again to free up spirit points and re-allocate them.
Though all of this takes time and you will have to decide what is worth investing in!

Writing your own agent
***************************

In principle, all you need is a text editor. However, we recommend getting started with the `agent development template <https://github.com/arenarium/battleground_agent_template>`_ because it allows you to test your agents locally before uploading it to the Arenarium website.

Once you have set up your environment, it is time to learn about the basic anatomy of an agent.

Every agent you write should derive from the :py:class:`~battleground.agent.Agent` class.
Don't worry, the only thing you have to implement is the `move` function.
A minimal agent implementation would look like this:

.. literalinclude :: ../battleground/games/arena/agents/minimal_agent.py
   :language: python

This agent just sits still for one turn. You are free to read the game state directly and process it however you like.
However, it is easiest to start with the basic building blocks provided by the :py:mod:`~battleground.games.arena.building_blocks` module.

The following example aggressively attacks the nearest other player.

.. literalinclude :: ../battleground/games/arena/agents/aggressive_attacker.py
   :language: python

From here it is up to you. Enjoy!

Agent Memory
-------------

Agents have the ability to remember information from previous games.
This enables them to learn and improve over time.

You can get/set this memory using the :py:meth:`~battleground.agent.Agent.get_memory` and
:py:meth:`~battleground.agent.Agent.set_memory` methods of the agent class.

A simple example would look like this:

.. literalinclude :: ../examples/external_agent/basic_persistent_agent.py
   :language: python


Modules
-------

.. autosummary::
  :toctree: modules

  battleground.agent
  battleground.game_engine
  battleground.games.arena.building_blocks

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
