from typing import List, Dict, Union, Optional
from src.database.option_class import Option


class Question:
    """
    Represents a question with options in a room.

    Attributes: question_id (str): The unique identifier for the question.
    question_text (str): The question text. options (List[Option]): A list
    of Option objects associated with the question.
    """

    def __init__(
        self,
        question_id: str,
        question_text: str,
        options: Optional[List[Option]] = None,
    ):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options or []

    def __eq__(self, other):
        if not isinstance(other, Question):
            return False
        return (
            self.question_id == other.question_id
            and self.question_text == other.question_text
            and self.options == other.options
        )

    def add_option(self, option: Option) -> None:
        """
        Adds an Option to the list of options for this question.

        Args:
            option (Option): The Option object to add.
        """
        self.options.append(option)

    def to_dict(self) -> Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]:
        """
        Converts the Question object to a dictionary.
        Returns:
            dict: A dictionary representation of the Question.

        """
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "options": [option.to_dict() for option in self.options],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Question object from a dictionary.

        Args:
            data (dict): A dictionary containing question data.

        Returns:
            Question: A Question object.
        """
        question_id = data.get("question_id", "")
        question_text = data.get("question_text", "")
        options_data = data.get("options", [])
        options = [Option.from_dict(option_data) for option_data in options_data]
        return cls(
            question_id=question_id, question_text=question_text, options=options
        )
