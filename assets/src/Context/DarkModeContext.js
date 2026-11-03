import {createContext, useEffect, useState} from "react"

export const DarkModeContext = createContext();

export default function DarkModeProvider({ children }) {
    const [darkMode, setDarkMode] = useState(() => {
        const savedTheme = localStorage.getItem('darkMode');
        return savedTheme === 'true';
    });

    useEffect(() => {
        localStorage.setItem('darkMode', darkMode);
    }, [darkMode]);

    function toggleDarkMode() {
        setDarkMode(prev => !prev);
    }

    return (
        <DarkModeContext.Provider
            value={ {darkMode, toggleDarkMode} }>
            {children}
        </DarkModeContext.Provider>
    )
}