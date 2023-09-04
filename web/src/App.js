import { Participant } from './components/Participant';
import { VoteButton } from './components/VoteButton';
import logo from './logo.svg';

function App() {
  return (
    <div className='flex flex-col w-screen h-screen bg-secondary-content'>
      <nav className="navbar flex justify-between bg-base-200">
        <a className="btn btn-ghost normal-case text-base" href="#menu">VetoFun</a>
        <div>
          <a className="btn btn-ghost normal-case text-base" href="create">Create Room</a>
          <a className="btn btn-ghost normal-case text-base" href="join">Join Room</a>
        </div>
      </nav>
      <div id='container' className='flex-grow flex'>
        <main className='flex-grow py-6'>
          <p className='text-center text-2xl mb-8'>Please select your preferred activity</p>
          <div className='mx-auto w-1/3 grid grid-cols-2 grid-rows-2 gap-2'>
            <VoteButton id='1' text='Option 1' />
            <VoteButton id='2' text='Option 2' />
            <VoteButton id='3' text='Option 3' />
            <VoteButton id='4' text='Option 4' />
          </div>
        </main>
        <aside className='flex-none w-60 bg-base-100'>
          <h2 className='text-xl mx-4 mt-4 mb-2 font-semibold'>Participants</h2>
          <Participant initial={'A'} name={'Alice'}/>
          <Participant initial={'B'} name={'Bob'}/>
          <Participant initial={'C'} name={'Charlie'}/>
        </aside>
      </div>
    </div>
  );
}

export default App;
