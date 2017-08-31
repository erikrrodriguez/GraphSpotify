from track import Track

class Album:
    
    def __init__(self, result=None):
        if result:
            self.load(result)

    # Sets this object's properties according to the dictionary in result
    # E.g., { "title" : "The xx" } -> self.title = "The xx"
    def load(self, result):
        for key, value in result.items():
            setattr(self, key, value)
