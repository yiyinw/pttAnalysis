class User:
    def __init__(self, id, ip, action_time):
        self.id = id
        self.ip = ip
        self.action_time = action_time


class Author(User):
    def __init__(self, id, ip, action_time, action_type):
        User.__init__(self, id, ip, action_time)
        assert action_type in ["OP", "RE"]
        self.action = "post"
        self.action_type = action_type

class Commentor(User):
    def __init__(self, id, ip, action_time, action_type):
        User.__init__(self, id, ip, action_time)
        assert action_type in ["pos", "neg", "neutral"]
        self.action = "comment"
        self.action_type = action_type