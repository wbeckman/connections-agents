from agents.random_agent import RandomAgent
import assess.assess



if __name__ == '__main__':
    rb = RandomAgent()
    s = assess.assess.assess_all(rb)
    assess.assess.detailed_stat_overview(s)
    assess.assess.stat_summary(s)
