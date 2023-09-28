class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.read()
    
    def read(self):
        self.names = []
        self.scores = []
        with open('leaderboard.txt', 'r') as file:
            data = file.read()
            line = ''
            for char in data:
                if char == '\n':
                    if len(self.names) > 7:
                        self.scores.append(line)
                    else:
                        self.names.append(line)
                    line = ''
                else:
                    line += char

    def add_entry(self, name):
        name_string = ''
        for i in name:
            name_string += i
        self.names.insert(self.game.player.leaderboard_index, name_string)
        self.names.pop()
        self.scores.insert(self.game.player.leaderboard_index, str(self.game.player.score))
        self.scores.pop()
        updated_leaderboard = ''
        for i in self.names:
            updated_leaderboard += i +'\n'
        for i in self.scores:
            updated_leaderboard += i +'\n'
        with open('leaderboard.txt', 'w') as file:
            file.write(updated_leaderboard)
        self.read()