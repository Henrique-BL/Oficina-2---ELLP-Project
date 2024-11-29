import React, { useState } from "react";
import "./Login.css";

function Login() {
    const [isRegistering, setIsRegistering] = useState(false);

    const toggleForm = () => {
        setIsRegistering(!isRegistering);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isRegistering) {
            alert("Cadastro realizado com sucesso!");
        } else {
            alert("Login realizado com sucesso!");
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
                            required
                            title="Digite um email válido no formato exemplo@dominio.com"
                        />

                        <label>Senha</label>
                        <input
                            type="password"
                            name="senha"
                            placeholder="Digite sua senha"
                            required
                            minlength="8"
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
