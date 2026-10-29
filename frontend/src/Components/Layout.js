import NavBar from "./NavBar";
import Menu from "./Menu";
import { Outlet } from "react-router";
import {useState} from "react";

export default function Layout() {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <>
            <div><Menu isOpen={isOpen} setIsOpen={setIsOpen} /></div>
            <div><NavBar isOpen={isOpen} setIsOpen={setIsOpen}/></div>
            <div className={`container ${!isOpen ? 'active' : ''}`}>
                <Outlet />
            </div>
        </>
    )

}