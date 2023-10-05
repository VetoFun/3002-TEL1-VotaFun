from typing import List, Dict, Union
from src.database.Option import Option


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
        options: List[Option] = [],
        last_question: bool = False,
    ):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options
        self.last_question = last_question

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

    def get_option_by_id(self, option_id: str) -> Option:
        for option in self.options:
            if option.option_id == option_id:
                return option
        raise KeyError(
            f"Option {option_id} does not exist in question {self.question_id}"
        )

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
            'last_question': self.last_question,
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
        last_question = data.get("last_question", False)
        return cls(
            question_id=question_id, question_text=question_text, options=options, last_question=last_question
        )

    def get_most_voted_option(self) -> Option:
        """
        Returns the option with the most votes.

        Returns:
            Option: The option with the most votes.
        """
        return max(self.options, key=lambda option: option.current_votes)
