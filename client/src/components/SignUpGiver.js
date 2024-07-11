import React, { useState } from "react";
//import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { useHistory } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Header from "./Header";

function SignUpGiver({ onSignUp }) {
    const [errors, setErrors] = useState([]);

    //const navigate = useNavigate()
    const history = useHistory();

    const formik = useFormik({
        initialValues: {
            email: "",
            firstName: "",
            lastName: "",
            password: "",
            phone: "",
            street: "",
            city: "",
            state: "",
            zip: "",
            user_type: false,
        },
        validationSchema: yup.object().shape({
            email: yup
                .string()
                .email("Email must be a valid email address")
                .required("Required"),
            first_name: yup.string().required("Required"),
            last_name: yup.string().required("Required"),
            password: yup
                .string()
                .min(8, "Password must be at least 6 characters long")
                .required("Required")
                .matches(
                    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/,
                    "Password must contain at least one uppercase letter, one lowercase letter, and one number"
                ),
            street: yup.string().required("Required"),
            city: yup.string().required("Required"),
            state: yup.string().max(2).required("Required"),
            zip_code: yup
                .string()
                .required("Required")
                .matches(/^\d{5}$/, "Zip code must be 5 digits long"),
            phone: yup
                .string()
                .required("Required")
                .matches(/^\d{10}$/, "Phone number must be 10 digits long"),
        }),
        onSubmit: async (values) => {
            console.log(values);
            try {
                setErrors([]);

                const response = await fetch("/signup", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(values),
                });

                if (response.ok) {
                    const user = await response.json();
                    onSignUp(user);
                    history.push("/dashboard/" + user.id);
                } else {
                    const errorData = await response.json();
                    setErrors(errorData);
                }
            } catch (error) {
                console.error("Error signing up:", error);
                setErrors([
                    {
                        message:
                            "An error occurred while signing up. Please try again later.",
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
                    id="first_name"
                    name="first_name"
                    type="text"
                    placeholder="First Name"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.first_name}
                />
                {formik.errors.first_name && formik.touched.first_name ? (
                    <p className="error">{formik.errors.first_name}</p>
                ) : null}
            </div>
            <div className="input-container">
                <input
                    id="last_name"
                    name="last_name"
                    type="text"
                    placeholder="Last Name"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.last_name}
                />
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
            <div className="input-container">
                <input
                    id="phone"
                    name="phone"
                    type="text"
                    placeholder="Phone Number"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.phone}
                />
                {formik.errors.phone && formik.touched.phone ? (
                    <p className="error">{formik.errors.phone}</p>
                ) : null}
            </div>
            <div className="input-container">
                <input
                    id="street"
                    name="street"
                    type="text"
                    placeholder="Street Address"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.street}
                />
                {formik.errors.street && formik.touched.street ? (
                    <p className="error">{formik.errors.street}</p>
                ) : null}
            </div>
            <div className="input-container">
                <input
                    id="city"
                    name="city"
                    type="text"
                    placeholder="City"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.city}
                />
                {formik.errors.city && formik.touched.city ? (
                    <p className="error">{formik.errors.city}</p>
                ) : null}
            </div>
            <div className="input-container">
                <input
                    id="state"
                    name="state"
                    type="text"
                    placeholder="State"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.state}
                />
                {formik.errors.state && formik.touched.state ? (
                    <p className="error">{formik.errors.state}</p>
                ) : null}
            </div>
            <div className="input-container">
                <input
                    id="zip_code"
                    name="zip_code"
                    type="text"
                    placeholder="Zip Code"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.zip_code}
                />
                {formik.errors.zip_code && formik.touched.zip_code ? (
                    <p className="error">{formik.errors.zip_code}</p>
                ) : null}
            </div>
            <div id="submit-button">
                <button type="submit">Submit</button>
            </div>
            <div id="errors">{errors.error}</div>
        </form>
    );
}
export default SignUpGiver;
