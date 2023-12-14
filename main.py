from bots.random_bot import RandomBot
import assess.assess



if __name__ == '__main__':
    rb = RandomBot()
    s = assess.assess.assess_all(rb)
    assess.assess.detailed_stat_overview(s, just_any_category=True)
    assess.assess.stat_summary(s)
