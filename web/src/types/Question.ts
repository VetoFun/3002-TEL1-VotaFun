import { Option } from './Option';

type Question = {
  question_id: string;
  question_text: string;
  options: Option[];
  voted: boolean;
};

export type { Question };
