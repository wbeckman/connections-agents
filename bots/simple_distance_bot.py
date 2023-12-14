from bots.bot import Bot

class SimpleDistanceBot(Bot):
    """
    Bot that greedily calculates inter-cluster distance between sets
    of four nodes and takes the most tightly clustered words. 

    Based on the embedding distance of the words. Has no real concept
    of polysemy, and is likely to be fooled by red herrings.
    """

    def __init__(self, embeddings) -> None:
        super().__init__()
        self.embeddings = embeddings

    def guess(self, words) -> list[str]:
        pass
