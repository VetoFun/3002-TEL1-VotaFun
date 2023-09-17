import { useRoomStore } from "@/stores/useRoomStore";
import { Room } from "@/types/Room";
import { User } from "@/types/User";

const joinRoom = (user: User, id: string) : Room => {
    // [todo] call endpoint to join room
    let room = useRoomStore.getState().room;
    
    if(room == null || room.id != id)
        room = { id: id, activity: '', location: '', users: [], host: null}

    if(room.users.length == 0)
        room.host = user

    room.users.push(user);
    return room;
}

export {joinRoom}