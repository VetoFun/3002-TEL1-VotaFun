from typing import Dict, Union


class Option:
    """
    Represents an option.

    Attributes:
        option_id (str): The unique identifier for the option.
        option_text (str): The option text.
        current_votes (int): The number of current votes of Option objects associated with the question.
    """

    def __init__(self, option_id: str, option_text: str, current_votes: int):
        self.option_id = option_id
        self.option_text = option_text
        self.current_votes = current_votes

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Convert Option object to a dictionary.
        Returns:
            dict: A dictionary representation of the Option.
        """
        return {
            "option_id": self.option_id,
            "option_text": self.option_text,
            "votes": self.current_votes,
        }
