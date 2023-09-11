import { Participant } from "./components/Participant";
import { VoteButton } from "./components/VoteButton";

export default function Home() {
  return (
    <div className="flex h-screen w-screen flex-col bg-secondary-content">
      <nav className="navbar flex justify-between bg-base-200">
        <a className="btn btn-ghost text-base normal-case" href="#menu">
          VotaFun
        </a>
        <div>
          <a className="btn btn-ghost text-base normal-case" href="create">
            Create Room
          </a>
          <a className="btn btn-ghost text-base normal-case" href="join">
            Join Room
          </a>
        </div>
      </nav>
      <div id="container" className="flex flex-grow">
        <main className="flex-grow py-6">
          <p className="mb-8 text-center text-2xl">
            Please select your preferred activity
          </p>
          <div className="mx-auto grid w-1/3 grid-cols-2 grid-rows-2 gap-2">
            <VoteButton id="1" text="Option 1" />
            <VoteButton id="2" text="Option 2" />
            <VoteButton id="3" text="Option 3" />
            <VoteButton id="4" text="Option 4" />
          </div>
        </main>
        <aside className="w-60 flex-none bg-base-100">
          <h2 className="mx-4 mb-2 mt-4 text-xl font-semibold">Participants</h2>
          <Participant initial={"A"} name={"Alice"} />
          <Participant initial={"B"} name={"Bob"} />
          <Participant initial={"C"} name={"Charlie"} />
        </aside>
      </div>
    </div>
  );
}
