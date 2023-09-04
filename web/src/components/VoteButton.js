
function VoteButton({ id, text }) {
    return <button className="btn btn-neutral h-fit py-4 text-lg" value={id}>{text}</button>;
}

export { VoteButton };