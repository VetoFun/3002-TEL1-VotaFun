import { useRoomStore } from '@/stores/useRoomStore';
import { Participant } from './Participant';

function getInitials(username: string) {
  if (username.length === 0) return 'U';
  return username[0].toUpperCase();
}

const RoomParticipants = () => {
  const users = useRoomStore((state) => state.users);

  return (
    <aside className="flex h-screen w-80 flex-col bg-neutral py-6 text-base-100">
      <h2 className="border-b-2 pb-4 text-center text-2xl font-semibold ">Participants</h2>
      <div>
        {users.map((user) => {
          return (
            <Participant
              key={user.user_id}
              initial={getInitials(user.user_name)}
              name={user.user_name}
              host={user.is_host}
            />
          );
        })}
      </div>
    </aside>
  );
};

export { RoomParticipants };
