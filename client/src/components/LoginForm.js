import React, { useState } from "react";
//import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import { useHistory } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";


function LoginForm({ onLogin}) {
    const [errors, setErrors] = useState([]);
    const { login } = useAuth();
    //const navigate = useNavigate()
    const history = useHistory();

    const formik = useFormik({
        initialValues: {
            email: "",
            password: ""
        },
    
        onSubmit: async (values) => {
            console.log(values);
            try {
                setErrors([]);

                const response = await fetch("/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(values),
                });

                if (response.ok) {
                    const user = await response.json();
                    login(user);
                    onLogin(user);
                    history.push("/dashboard/" + user.id);
                } else {
                    const errorData = await response.json();
                    setErrors(errorData);
                }
            } catch (error) {
                console.error("Error Loggin In:", error);
                setErrors([
                    {
                        message:
                            "You have entered an invalid email or password.",
                    },
                ]);
            }
        },
    });
    return (
        <form onSubmit={formik.handleSubmit}>
            <div className="input-container">
                <input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="Email"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.email}
                />
                {formik.errors.email && formik.touched.email ? (
                    <p className="error">{formik.errors.email}</p>
                ) : null}
            </div>
          
            <div className="input-container">
                <input
                    id="password"
                    name="password"
                    type="text"
                    placeholder="Password"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.password}
                />
                {formik.errors.password && formik.touched.password ? (
                    <p className="error">{formik.errors.password}</p>
                ) : null}
            </div>
            <div id="submit-button">
                <button type="submit">Submit</button>
            </div>
            <div id="errors">{errors.error}</div>
        </form>
    );
}
export default LoginForm;
