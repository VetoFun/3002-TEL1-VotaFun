import { Option } from './Option';

type Question = {
  question_id: string;
  question_text: string;
  options: Option[];
};

export type { Question };
