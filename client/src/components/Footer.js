import React from "react";
import { NavLink, Link } from "react-router-dom";

function Footer() {
    return (
        <nav>
            <ul>
                <li>
                    <NavLink exact to="/">Home</NavLink>
                </li>
                <li>
                    <NavLink exact to="/about">About</NavLink>
                </li>
                <li>
                    <NavLink exact to="/contact">Contact</NavLink>
                </li>
            </ul>
        </nav>
    );
}

export default Footer;

