class State():
    def __init__(self, paths, parent):
        self.paths = paths
        self.parent = parent

    def get_children(self):
        pass # not my job

    def score(self):
        pass # to be implemented