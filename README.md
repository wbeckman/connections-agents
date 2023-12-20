## Connections Agents

This is a repo that provides an agent interface for the New York Times game of Connections. Please feel free to use it to develop AI related to the game.

### Usage

First, clone the repository with 

```
git clone git@github.com:wbeckman/connections-agents.git
```

Then, `cd connections-agents`. There are currently no external dependencies for the project, but I imagine that will change when you actually build an agent.

### Developing an Agent

All Connections agents will derive from the `agents.Agent` class. This class contains a `solve` function that will call `guess` until the agent is either out of guesses or the puzzle is solved. 

I will assume that you are familiar with the rules of Connections here. If you are not, [play a game](https://www.nytimes.com/games/connections) at the New York Times puzzles site and come back here. 

When developing an agent, all you need to do is to implement the `guess` function. The agent is initially given a list of 16 words (the words in the puzzle) and has to produce a guess (a list of 4 words) that it believes are grouped together. If this is correct, 12 words will be passed into the agent next time. Otherwise, the agent will be forced to produce another guess.

The agent has access to one piece of state at an instance level (`self.guesses`) when solving a puzzle:
- This is a map from a **guess** (tuple of four words in the puzzle) to a tuple of the following:
  - **list of colors** that that guess solved (empty list if the guess did not solve any colors)
  - **boolean** flag, whether or not the guess was "one away" (three of the words in the guess were in a category, but a fourth word was in a different category)

So, for the following puzzle:

```
IGNITE - BURN, KINDLE, LIGHT, TORCH
INFORMATION - DATA, INFO, INTEL, NEWS
SMALL WOODED AREA - DELL, GLEN, HOLLOW, VALLEY
THINGS WITH CORES - APPLE, COMPUTER, PLANET, REACTOR
```

an example of what `guesses`` could look like after three gueeses is as follows:
```
{
    ('DELL', 'GLEN', 'HOLLOW', 'VALLEY'): ([Color.BLUE], False), # Correct guess
    ('INTEL', 'APPLE', 'DATA', 'COMPUTER'): ([], False), # Incorrect guess (more than one away)
    ('COMPUTER', 'PLANET', 'REACTOR', 'BURN'): ([], True) # Incorrect guess - one away
}

```

This piece of state can be useful to see if a guess has already guessed or to perform a process of elimination based on previously guessed 'one away' guesses.

At the entry point in `main.py`, simply change the agent that you want from `RandomAgent` to the agent class that you develop. This will test the agent against 183 previous connections puzzles from the NYT to assess its performance. If the agent even gets a few puzzles correct, that's awesome - and WAY better than a random guessing agent. 

Have fun! Let me know if you would like me to change anything or open a PR to fix things that seem to be wrong.
