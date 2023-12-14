from bots.bot import Bot
import random

class RandomBot(Bot):
    """
    Random bot that will just guess randomly. This bot is not intended to do
    well, it's just a test of the bot class and the test bed.
    """

    def __init__(self) -> None:
        super().__init__()

    def guess(self, words) -> list[str]:
        # Resample until guess comes up that hasn't been guessed
        # Inefficient, but shouldn't take too long
        guess = tuple(sorted(random.sample(words, 4)))
        
        while guess in self.guesses:
            guess = tuple(sorted(random.sample(words, 4)))
            
        return guess

