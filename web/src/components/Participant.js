
function Participant({ initial, name }) {
    return (
    <div className='flex gap-4 px-4 py-2 align-middle w-full hover:bg-base-content hover:text-neutral-focus transition-colors'>
        <div className="avatar placeholder">
        <div className="bg-neutral-focus text-neutral-content rounded-full w-10">
            <span className="inline text-base">{initial}</span>
        </div>
        </div> 
        <div className='flex-grow flex'>
        <p className='my-auto'>{name}</p>
        </div>
    </div>
    )
}

export { Participant }