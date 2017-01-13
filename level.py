class Level:
    def __init__(self, filename):
        f = open("levels/" + filename, 'r+')
        lines = f.readlines()
        self.layout = []
        for line in lines:
            self.layout.append(line.split())

    def get_layout(self):
        return self.layout
