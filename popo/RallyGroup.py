class RallyGroup:
    def __init__(self):
        self.leader = None
        self.followers = []

    def __init__(self, leader,followers):
        self.leader = leader
        self.followers = followers

    def add_follower(self,follower):
        self.followers.append(follower)

    def add_leader(self, leader):
        self.leader = leader