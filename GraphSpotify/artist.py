from album import Album

class Artist:
    
    def __init__(self, result=None):
        if result:
            self.load(result)


    def load(self, result):
        for key, value in result.items():
            setattr(self, key, value)
