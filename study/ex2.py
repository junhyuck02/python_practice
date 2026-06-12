class Player:

    def __init__(self, name, team):
        self.name = name
        self.xp = 1500
        self.team = team

    def introduce(self):
        print(f"Hello! I'm {self.name} and I play for {self.team}")


class Team:

    def __init__(self, team_name):
        self.team_name = team_name
        self.players = [] 

    def show_players(self):
        for player in self.players:
            player.introduce()

    def add_player(self, name):
        new_player = Player(name, self.team_name)
        self.players.append(new_player)

    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
    
    def total_xp(self):
        total = 0
        for player in self.players:
            total += player.xp
        return total


Chelsea = Team("Chelsea FC")
Chelsea.add_player("James")
Chelsea.add_player("Caicedo")
Chelsea.add_player("Palmer")


Aresnal = Team("Aresnal FC")
Aresnal.add_player("Rice")
Aresnal.add_player("Saliba")
