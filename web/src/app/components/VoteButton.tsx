
interface VoteButtonProps {
    id: string,
    text: string
}

function VoteButton({ id, text } : VoteButtonProps) {
    return <button className="btn btn-neutral h-fit py-4 text-lg" value={id}>{text}</button>;
}

export { VoteButton };