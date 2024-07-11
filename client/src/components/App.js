import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import Home from "./Home";
import Dashboard from "./Dashboard";
import About from "./About";
import Contact from "./Contact";
import SignUpReceiver from "./SignUpReceiver";
import SignUpGiver from "./SignUpGiver";
import LoginForm from "./LoginForm";
import { useAuth } from "../contexts/AuthContext";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [user, setUser] = useState(null);

  
  
  return (
    <div className="App">
      <Header setUser = {setUser} user = {user} />
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/signupreceiver">
          <SignUpReceiver onSignUp={setUser}/>
        </Route>
        <Route exact path="/signupgiver">
          <SignUpGiver onSignUp={setUser}/>
        </Route>
        <Route exact path="/dashboard">
          <Dashboard user={user} />
        </Route>
        <Route exact path="/about">
          <About />
        </Route>
        <Route exact path="/contact">
          <Contact />
        </Route>
        <Route exact path="/loginform">
          <LoginForm onLogin={setUser} /> 
        </Route>          
      </Switch>
      <Footer />
    </div>
  );
};
//      <div classname="MainContainer">
//        {user ? 
//          { user.user_type ? 
//              <Routes>
//                <Route path='/dashboard/{user.user_id}' element={<h1>Welcome Back {user.first_name}</h1>} /> 
//: 
//            <Routes>
//                <Route exact path='/' element={<SignUpForm onLogin={setUser} />}>
//        <div className="logged-in-landing">
//                        <h1>Acts Of Kindness</h1></div>
//            </Routes> :
//        <>
//        <div className="no-session-landing">
//            <h1>Acts Of Kindness</h1>
//            <div className="links">
//                <Link to='/signup' className="link">Sign Up</Link>
//                <Link to='/login' className="link">Login</Link>
//            </div>
//            </div>
//        </div>
//    </div>
//  );
//}

export default App;
