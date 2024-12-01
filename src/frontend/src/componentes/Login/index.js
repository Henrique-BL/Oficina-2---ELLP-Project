import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Login.css";

function Login() {
    const [isRegistering, setIsRegistering] = useState(false);
    const [formData, setFormData] = useState({ nome: "", email: "", senha: "" });
    const navigate = useNavigate();

    const toggleForm = () => {
        setIsRegistering(!isRegistering);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isRegistering) {
                // Chamada para a rota de cadastro
                const response = await axios.post("http://localhost:8000/register", {
                    name: formData.nome,
                    email: formData.email,
                    password: formData.senha,
                });
                alert("Cadastro realizado com sucesso!");
                console.log(response.data);
                setIsRegistering(false); // Alterna para a tela de login após o cadastro
            } else {
                // Chamada para a rota de login
                const response = await axios.post("http://localhost:8000/login", {
                    email: formData.email,
                    password: formData.senha,
                });
                alert("Login realizado com sucesso!");
                console.log(response.data);
                navigate("/home");
            }
        } catch (error) {
            if (error.response) {
                alert(`Erro: ${error.response.data.detail}`);
            } else {
                alert("Erro ao conectar ao servidor. Tente novamente mais tarde.");
            }
            console.error(error);
        }
    };

    return (
        <div className="container">
            <div className="card">
                <div className="card-left">
                    <h1>ELLP</h1>
                    <p>ensino.lúdico(lógica.programação)</p>
                    <button onClick={toggleForm}>{isRegistering ? "Login" : "Cadastrar-se"}</button>
                    <img src="/imagens/elpinho-reto.png" alt="Robô ELLP" />
                </div>

                <div className="card-right">
                    <form onSubmit={handleSubmit}>
                        <h2>{isRegistering ? "Cadastro" : "Login"}</h2>

                        {isRegistering && (
                            <>
                                <label>Nome</label>
                                <input
                                    type="text"
                                    name="nome"
                                    placeholder="Digite seu nome"
                                    value={formData.nome}
                                    onChange={handleChange}
                                    required
                                    pattern="^[a-zA-ZÀ-ÿ\s]+$"
                                    title="O nome deve conter apenas letras e espaços."
                                />
                            </>
                        )}

                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            placeholder="Digite seu email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            title="Digite um email válido no formato exemplo@dominio.com"
                        />

                        <label>Senha</label>
                        <input
                            type="password"
                            name="senha"
                            placeholder="Digite sua senha"
                            value={formData.senha}
                            onChange={handleChange}
                            required
                            minLength="8"
                            title="A senha deve ter pelo menos 8 caracteres."
                        />

                        {!isRegistering && <a href="#">Esqueceu sua senha?</a>}

                        <button type="submit">{isRegistering ? "Cadastrar" : "Entrar"}</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Login;
