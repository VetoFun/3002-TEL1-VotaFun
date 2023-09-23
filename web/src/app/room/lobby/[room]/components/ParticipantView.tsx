import { useRoomStore } from '@/stores/useRoomStore';
import { Label } from './Label';

const ParticipantView = () => {
  const [room, user] = useRoomStore((state) => [state.room, state.user]);
  console.log(`in participant view, socketID: ${user?.id}`);

  return (
    <>
      <Label label="Location" text={room?.location || ''} />
      <Label label="Activity" text={room?.activity || ''} />
    </>
  );
};

export { ParticipantView };
