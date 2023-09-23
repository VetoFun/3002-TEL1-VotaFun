import { User } from "@/types/User";

const createUser = (username: string) : User => {
    // [todo] establish socket connection and 'create user'
    return{ id: 1, username: username }
}

export {createUser}