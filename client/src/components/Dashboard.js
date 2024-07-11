import React from "react";
import { NavLink, Link } from "react-router-dom";
import { Routes, Route } from "react-router-dom";

function Dashboard({ user }) {
    return (
        <div>
            <h1>{user.first_name}'s Dashboard</h1>
        </div>
    );
}

export default Dashboard;
