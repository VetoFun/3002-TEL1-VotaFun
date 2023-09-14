from typing import List, Dict, Union, Optional
from option_class import Option


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
            "question": self.question_text,
            "options": [option.to_dict() for option in self.options],
        }
