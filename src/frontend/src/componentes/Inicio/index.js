import React from "react";
import { Link } from "react-router-dom";
import "./inicio.css";

const Inicio = () => {
    return (
        <div className="home-container">
            <header className="header">
                <h1>ELLP</h1>
                <p>Bem-vindo ao sistema</p>
            </header>
            <div className="navigation">
                <Link to="/add-volunteer" className="nav-link">
                    Cadastrar Voluntário
                </Link>
                <Link to="/volunteers" className="nav-link">
                    Visualizar Voluntários
                </Link>
            </div>
        </div>
    );
};

export default Inicio;
