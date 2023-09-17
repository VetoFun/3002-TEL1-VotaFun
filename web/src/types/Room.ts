import { User } from "./User";

type Room = {
    id: string;
    activity : string;
    location : string;
    users: User[];
    host: User | null;
}

export type { Room }