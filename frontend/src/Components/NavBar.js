export default function NavBar({isOpen, setIsOpen}) {
    return (
        <>
            <div className={`top_bar ${!isOpen ? 'active' : ''}`}></div>
        </>
    )
}