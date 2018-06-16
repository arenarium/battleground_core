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

You're probably here because you want to get started playing Arenarium.
Arenarium is a game you play by writing code, this guide explains how.

In principle, all you need is a text editor. However, we recommend getting started with the `agent development template <https://github.com/arenarium/battleground_agent_template>`_ because it allows you to test your agents locally before uploading it to the Arenarium website.

Once you've set up your environment, it's time to learn about the basic anatomy of an agent.

Every agent you write should derive from the :py:class:`~battleground.agent.Agent` class. Don't worry, the only thing you have to implement is the `move` function. A minimal agent implementation would look like this:

.. literalinclude :: ../battleground/games/arena/agents/minimal_agent.py
   :language: python

This agent just sits still for one turn. You are free to read the game state directly and process it however you like.  You can see examples of the `state` dictionary
However, it's easiest to start with a few basic building blocks.

Modules
-------

.. autosummary::
  :toctree: modules

  battleground.agent
  battleground.game_engine

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
