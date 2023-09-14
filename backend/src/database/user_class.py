from typing import Dict


class User:
    """
    Represents a User object.

    Attributes:
        user_id (str): The unique identifier for the user.
        user_name (str): The user's name.
    """

    def __init__(self, user_id: str, user_name: str):
        self.user_id = user_id
        self.user_name = user_name

    def to_dict(self) -> Dict[str, str]:
        return {"user_id": self.user_id, "user_name": self.user_name}
