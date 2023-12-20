from agents.agent import Agent
import random

class RandomAgent(Agent):
    """
    Random agent that will just guess randomly. This agent is not intended to do
    well, it's just a test of the Agent class and the test bed.
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
