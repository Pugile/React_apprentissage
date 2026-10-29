import { Link } from 'react-router';
import '../Styles/style.css';

export default function Menu({isOpen, setIsOpen}) {
    let contenu = null;
    if (isOpen) {
        contenu =
        <div className="menu-item">
            <Link to="/ " onClick={() => setIsOpen(!isOpen)}>Page 1</Link>
            <Link to="/page2" onClick={() => setIsOpen(!isOpen)}>Page 2</Link>
        </div>
    }
    return (
        <>
            <div>
                <button
                    className={`hamburger`}
                    onClick={() => setIsOpen(!isOpen)}
                    aria-label="Menu de navigation"
                >
                    ☰
                </button>
            </div>
            <nav className="navbar" style={{ display: isOpen ? 'inline' : 'none' }}>
                {contenu}
            </nav>

            {isOpen && <div className="menu-overlay" onClick={() => setIsOpen(!isOpen)}></div>}
        </>
    );
}
