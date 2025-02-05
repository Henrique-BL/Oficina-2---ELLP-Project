import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./componentes/Login";
import AddVolunteer from "./componentes/AddVoluntarios";
import Home from "./componentes/Inicio";
import VolunteerList from "./componentes/ListaVoluntarios";
import AddWorkshop from "./componentes/AddWorkshop";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/home" element={<Home />} />
                <Route path="/add-volunteer" element={<AddVolunteer />} />
                <Route path="/volunteers" element={<VolunteerList />} />
                <Route path="/add-workshop" element={<AddWorkshop />} />
            </Routes>
        </Router>
    );
}

export default App;
