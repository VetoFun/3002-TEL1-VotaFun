import { useRoomStore } from '@/stores/useRoomStore';
import { Participant } from './Participant';
import { useDebugStore } from '@/stores/useDebugStore';

function getInitials(username: string) {
  if (username.length === 0) return 'U';
  return username[0].toUpperCase();
}

const RoomParticipants = () => {
  const room = useRoomStore((state) => state.room!);
  const host = useDebugStore((state) => state.admin);

  return (
    <aside className="flex h-screen w-80 flex-col bg-neutral py-6 text-base-100">
      <h2 className="border-b-2 pb-4 text-center text-2xl font-semibold ">Participants</h2>
      <div>
        {room.users.map((user, index) => {
          return <Participant key={index} initial={getInitials(user.username)} name={user.username} host={host} />;
        })}
      </div>
    </aside>
  );
};

export { RoomParticipants };
