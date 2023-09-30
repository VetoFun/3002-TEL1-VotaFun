import { RoomParticipants } from '../common/RoomParticipants';

interface RoomLayoutProps {
  children?: React.ReactNode;
}

const RoomLayout = ({ children }: RoomLayoutProps) => {
  return (
    <div className="flex h-screen w-screen">
      <div className="flex-1">{children}</div>
      <RoomParticipants />
    </div>
  );
};

export { RoomLayout };
