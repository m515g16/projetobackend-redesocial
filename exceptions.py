class FollowExistsError(Exception):
    def __init__(self, message) -> None:
        self.message = message

class FriendshipExistsError(Exception):
    def __init__(self, message) -> None:
        self.message = message

