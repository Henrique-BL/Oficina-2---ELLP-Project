import React, { useState, useEffect } from "react";
import axios from "axios";
import "./listavoluntarios.css";

const ListaVoluntarios = () => {
    const [volunteers, setVolunteers] = useState([]);

    useEffect(() => {
        const fetchVolunteers = async () => {
            try {
                const response = await axios.get("http://localhost:8000/volunteers/");
                setVolunteers(response.data);
            } catch (error) {
                console.error("Erro ao buscar voluntários:", error);
            }
        };

        fetchVolunteers();
    }, []);

    return (
        <div className="volunteer-list-container">
            <header className="header">
                <h1>ELLP</h1>
                <p>Lista de Voluntários</p>
            </header>
            <div className="list-container">
                {volunteers.length === 0 ? (
                    <p>Nenhum voluntário cadastrado.</p>
                ) : (
                    <ul>
                        {volunteers.map((volunteer) => (
                            <li key={volunteer.id}>
                                <p>
                                    <strong>Nome:</strong> {volunteer.name}
                                </p>
                                <p>
                                    <strong>RA:</strong> {volunteer.student_code}
                                </p>
                                <p>
                                    <strong>Email:</strong> {volunteer.email}
                                </p>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default ListaVoluntarios;
