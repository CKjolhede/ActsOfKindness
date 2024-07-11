import React from "react";
import { useContext } from "react";
import { NavLink, Link } from "react-router-dom";
import { Switch, Route } from "react-router-dom";
import SignUpReceiver  from "./SignUpReceiver";
import LoginForm from "./LoginForm";
import { useAuth } from "../contexts/AuthContext";
function Header({ setUser, user }) {
    const { logout } = useAuth();
    
    return (
        <div className="Header">
            {user ?
                <div className="logged-in-landing">
                    <h1>Acts Of Kindness</h1>
                    <h1>Welcome {user.first_name}</h1>
                    <div id="links">
                        <h3><Link to='/' onClick={logout}>Logout</Link></h3>
                        <NavLink to='/dashboard' className="link">Dashboard</NavLink>
                    </div>
                </div>
                :
                <div className="no-session-landing">
                    <Link to="/"><img src={(".../public/girl_avatar.jpg")} alt="logo"/></Link><h1>Acts Of Kindness</h1>
                    <div className="links">
                        <NavLink to='/signupreceiver' className="link">Sign UP to Recieve Kindness</NavLink>
                        <NavLink to='/signupgiver' className="link">Sign Up to Offer Kindness</NavLink>
                        <NavLink to='/loginform' className="link">Login</NavLink>
                    </div>
                <Switch>
                    <Route path='/signupreceiver'>
                        {/*<SignUpReceiver onSignUp={setUser} />*/}
                    </Route>
                    <Route path='/loginform'>
                        {/*element={<LoginForm onLogin={setUser} />}>*/}
                    </Route>
                </Switch>
                </div>
            }
        </div>);
}

export default Header;
