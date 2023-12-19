## Connections Bots

This is a repo that provides an agent interface for the New York Times game of Connections. Please feel free to use it to develop AI related to the game.

### Usage

First, clone the repository with 

```
git clone git@github.com:wbeckman/connections-bots.git
```

Then, `cd connections-bots`. There are currently no external dependencies for the project, but I imagine that will change when you actually build an agent.

### Developing an Agent

All Connections agents will derive from the `bots.Bot` class. This class contains a `solve` function that will call `guess` until the bot is either out of guesses or the puzzle is solved. 

I will assume that you are familiar with the rules of Connections here. If you are not, [play a game](https://www.nytimes.com/games/connections) at the New York Times puzzles site and come back here. 

When developing a bot, all you need to do is to implement the `guess` function. The bot is initially given a list of 16 words (the words in the puzzle) and has to produce a guess (a list of 4 words) that it believes are grouped together. If this is correct, 12 words will be passed into the bot next time. Otherwise, the bot will be forced to produce another guess.

The bot has access to one piece of state at an instance level (`self.guesses`) when solving a puzzle:
- This is a map from a **guess** (tuple of four words in the puzzle) to a tuple of the following:
  - **list of colors** that that guess solved (empty list if the guess did not solve any colors)
  - **boolean** flag, whether or not the guess was "one away" (three of the words in the guess were in a category, but a fourth word was in a different category)

So, an example of what guesses could look like is this:
```
{
    ('DELL', 'GLEN', 'HOLLOW', 'VALLEY'): ([Color.BLUE], False), # Correct guess
    ('INTEL', 'APPLE', 'DATA', 'COMPUTER'): ([], False), # Incorrect guess (more than one away)
    ('COMPUTER', 'PLANET', 'REACTOR', 'BURN'): ([], True) # Incorrect guess - one away
}

```

At the entry point in `main.py`, simply change the bot that you want from `RandomBot` to the bot class that you develop. This will test the bot against 183 previous connections puzzles from the NYT to assess its performance. If the bot even gets a few puzzles correct, that's awesome - and WAY better than a random guessing bot. 

Have fun! Let me know if you would like me to change anything or open a PR to fix things that seem to be wrong.
