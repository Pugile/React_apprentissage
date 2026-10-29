import React from 'react';
import ReactDOM from 'react-dom/client';
import './Styles/style.css';
import Page1 from "./View/Page1";
import Page2 from "./View/Page2";
import Layout from "./Components/Layout";
import { BrowserRouter, Routes, Route } from "react-router";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Page1 />} />
                    <Route path="/page2" element={<Page2 />} />
                </Route>
            </Routes>
        </BrowserRouter>
    </React.StrictMode>
);