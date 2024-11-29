import React, { useState } from "react";
import "./addVoluntarios.css";

const AddVolunteer = () => {
    const [formData, setFormData] = useState({
        nome: "",
        ra: "",
        email: "",
        telefone: "",
        dataIngresso: "",
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "telefone") {
            setFormData({ ...formData, [name]: formatPhone(value) });
        } else {
            setFormData({ ...formData, [name]: value });
        }
    };

    // Função para formatar o telefone
    const formatPhone = (value) => {
        const cleanedValue = value.replace(/\D/g, "");

        if (cleanedValue.length <= 2) {
            return `(${cleanedValue}`;
        } else if (cleanedValue.length <= 6) {
            return `(${cleanedValue.slice(0, 2)}) ${cleanedValue.slice(2)}`;
        } else if (cleanedValue.length <= 10) {
            return `(${cleanedValue.slice(0, 2)}) ${cleanedValue.slice(2, 6)}-${cleanedValue.slice(6)}`;
        } else {
            return `(${cleanedValue.slice(0, 2)}) ${cleanedValue.slice(2, 7)}-${cleanedValue.slice(7, 11)}`;
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Dados enviados:", formData);
        // Enviar dados para o backend aqui
    };

    return (
        <div className="add-volunteer-container">
            <header className="header">
                <h1>ELLP</h1>
                <p>início &gt; cadastro de voluntários</p>
            </header>
            <div className="form-container">
                <h2>Adicionar colaborador voluntário</h2>
                <form onSubmit={handleSubmit}>
                    <fieldset>
                        <legend>Dados Pessoais</legend>

                        <div className="input-group">
                            <label htmlFor="nome">Nome:</label>
                            <input
                                type="text"
                                id="nome"
                                name="nome"
                                value={formData.nome}
                                onChange={handleChange}
                                placeholder="Digite o nome"
                                required
                                pattern="^[a-zA-ZÀ-ÿ\s]+$"
                                title="O nome deve conter apenas letras."
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="ra">RA:</label>
                            <input
                                type="text"
                                id="ra"
                                name="ra"
                                value={formData.ra}
                                onChange={handleChange}
                                placeholder="Digite o RA"
                                required
                                pattern="^\d+$"
                                title="O RA deve conter apenas números."
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="email">Email:</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="seuemail@exemplo.com.br"
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="telefone">Telefone:</label>
                            <input
                                type="tel"
                                id="telefone"
                                name="telefone"
                                value={formData.telefone}
                                onChange={handleChange}
                                placeholder="(XX) XXXXX-XXXX"
                                pattern="^\(\d{2}\)\s\d{4,5}-\d{4}$"
                                title="Digite um número de telefone válido, como (11) 98765-4321."
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="dataIngresso">Data de ingresso:</label>
                            <div className="date-picker-container">
                                <input
                                    type="date"
                                    id="dataIngresso"
                                    name="dataIngresso"
                                    value={formData.dataIngresso}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </div>
                    </fieldset>

                    <button type="submit" className="btn-cadastrar">
                        Cadastrar
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddVolunteer;
