import {useEffect, useState} from "react";

export default function NavBar({isOpen, setIsOpen}) {
    const[theme, setTheme] = useState('light');
    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);
    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
    };
    return (
        <>
            <div className={`top_bar ${!isOpen ? 'active' : ''}`}>
                <button
                    onClick={toggleTheme}
                    className="theme-button"
                >
                    {theme === 'light' ? '🌙 Mode Sombre' : '☀️ Mode Clair'}
                </button>
            </div>

        </>
    )
}