import { Participant } from "./Participant";

const RoomParticipants = () => {
  return (
    <aside className="flex h-screen w-80 flex-col bg-neutral-focus py-6">
      <h2 className="border-b-2 pb-4 text-center text-2xl font-semibold">Participants</h2>
      <div>
        <Participant initial="A" name="Alice" host />
        <Participant initial="B" name="Bob" />
        <Participant initial="C" name="Charlie" />
        <Participant initial="D" name="Donki" />
      </div>
    </aside>
  );
};

export { RoomParticipants };
