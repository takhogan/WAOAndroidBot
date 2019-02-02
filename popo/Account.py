class Account:
    #farmtypes:
        #MINMAX = 1
        #DEFENDER = 2
        #RALLY_OWNER = 3
    def __init__(self, name, farmtype, collect_rss, upgrade_mode, research_mode, monster_mode, gather_mode):
        self.name = name
        self.farmtype = farmtype
        self.collect_rss = collect_rss
        self.upgrade_mode = upgrade_mode
        self.research_mode = research_mode
        self.monster_mode = monster_mode
        self.gather_mode = gather_mode