import { Question } from './Question';
import { User } from './User';

type Room = {
  room_id: string;
  number_of_user: number;
  max_capacity: number;
  last_activity: string;
  questions: Question[];
  host_id: string;
  status: string;
  room_location: string;
  room_activity: string;
  users: User[];
};

export type { Room };
