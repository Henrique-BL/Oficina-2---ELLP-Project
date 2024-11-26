import React, { useState } from "react";
import "./Login.css"; // Importa o CSS específico do componente

function Login() {
    const [isRegistering, setIsRegistering] = useState(false);

    const toggleForm = () => {
        setIsRegistering(!isRegistering);
    };

    return (
        <div className="container">
            <div className="card">
                {/* Card Esquerdo */}
                <div className="card-left">
                    <h1>ELLP</h1>
                    <p>ensino.lúdico(lógica.programação)</p>
                    <button onClick={toggleForm}>{isRegistering ? "Login" : "Cadastrar-se"}</button>
                    <img src="/imagens/elpinho-reto.png" alt="Robô ELLP" />
                </div>

                {/* Card Direito */}
                <div className="card-right">
                    {isRegistering ? (
                        <div>
                            <h2>Cadastro</h2>
                            <label>Nome</label>
                            <input type="text" placeholder="Digite seu nome" />
                            <label>Email</label>
                            <input type="email" placeholder="Digite seu email" />
                            <label>Senha</label>
                            <input type="password" placeholder="Digite sua senha" />
                            <button>Cadastrar</button>
                        </div>
                    ) : (
                        <div>
                            <h2>Login</h2>
                            <label>Email</label>
                            <input type="email" placeholder="Digite seu email" />
                            <label>Senha</label>
                            <input type="password" placeholder="Digite sua senha" />
                            <a href="#">Esqueceu sua senha?</a>
                            <button>Entrar</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Login;
