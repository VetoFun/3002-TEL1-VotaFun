export default function CreateRoomPage() {
  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <p className="text-center text-xl font-light">
          [todo] call api in this page to create room and then route this page
          to{" "}
          <code className="inline-block rounded-md bg-neutral p-1 px-2">
            /lobby
          </code>{" "}
          or use this room as lobby
        </p>
      </div>
    </main>
  );
}
