from typing import Dict


class User:
    """
    Represents a User object.

    Attributes:
        user_id (str): The unique identifier for the user.
        user_name (str): The user's name.
        is_host (bool): Whether the user is the host of the room.
    """

    def __init__(self, user_id: str, user_name: str, is_host: bool = False):
        self.user_id = user_id
        self.user_name = user_name
        self.is_host = is_host

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id and self.user_name == other.user_name

    def __len__(self):
        return 1

    def to_dict(self) -> Dict[str, str]:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "is_host": self.is_host,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a User object from a dictionary.

        Args:
            data (dict): A dictionary containing user data.

        Returns:
            User: A User object.
        """
        user_id = data.get("user_id", "")
        user_name = data.get("user_name", "")
        user_is_host = data.get("is_host", False)
        return cls(user_id=user_id, user_name=user_name, is_host=user_is_host)
