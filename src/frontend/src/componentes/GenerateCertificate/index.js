import { useState, useEffect } from "react";
import axios from "axios";
import { jsPDF } from "jspdf";
import "./generateCertificate.css";

const GerarCertificados = () => {
    const [workshopSelecionado, setWorkshopSelecionado] = useState("");
    const [voluntarios, setVoluntarios] = useState([]);
    const [workshops, setWorkshops] = useState([]);
    const [certificadosGerados, setCertificadosGerados] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Carregar workshops ao montar o componente
        axios
            .get("http://localhost:8000/api/workshops")
            .then((response) => {
                setWorkshops(response.data);
            })
            .catch((err) => {
                setError("Erro ao carregar workshops");
                console.error(err);
            });
    }, []);

    // Atualiza a lista de voluntários ao selecionar um workshop
    const handleWorkshopChange = (event) => {
        const idSelecionado = event.target.value;
        setWorkshopSelecionado(idSelecionado);

        if (idSelecionado) {
            axios
                .get(`http://localhost:8000/api/workshops/${idSelecionado}/volunteers`)
                .then((response) => {
                    setVoluntarios(response.data);
                })
                .catch((err) => {
                    setError("Erro ao carregar voluntários");
                    console.error(err);
                });
        } else {
            setVoluntarios([]);
        }
    };

    // Função para gerar certificado em PDF
    const gerarCertificado = async (voluntario) => {
        if (certificadosGerados[voluntario.id]) return;

        setLoading(true);

        try {
            const workshop = workshops.find((w) => w.id == workshopSelecionado);
            if (!workshop) {
                setError("Workshop não encontrado");
                return;
            }

            // Chamada ao back-end para gerar certificado
            const response = await axios.post("http://localhost:8000/api/certificates", {
                volunteerId: voluntario.id,
                workshopId: workshop.id,
            });

            setCertificadosGerados((prev) => ({
                ...prev,
                [voluntario.id]: true,
            }));

            // Supondo que o back-end retorna o PDF ou informações necessárias para gerá-lo
            console.log("Certificado Gerado:", response.data);

            const doc = new jsPDF();

            doc.setFont("helvetica", "bold");
            doc.setFontSize(22);
            doc.text("Certificado de Participação", 50, 30);

            doc.setFont("helvetica", "normal");
            doc.setFontSize(16);
            doc.text(`Certificamos que ${voluntario.nome}`, 20, 50);
            doc.text(`participou do workshop "${workshop.nome}"`, 20, 60);
            doc.text(`com carga horária de ${workshop.cargaHoraria} horas.`, 20, 70);

            const dataAtual = new Date();
            const dataFormatada = `${dataAtual.getDate().toString().padStart(2, "0")}/${(dataAtual.getMonth() + 1)
                .toString()
                .padStart(2, "0")}/${dataAtual.getFullYear()}`;

            doc.text(`Data de emissão: ${dataFormatada}`, 20, 90);

            // Salva o PDF
            doc.save(`Certificado_${voluntario.nome}.pdf`);
        } catch (error) {
            setError("Erro ao gerar certificado");
            console.error("Erro ao gerar certificado:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="certificados-container">
            <h1>Gerar Certificados</h1>
            {error && <p>{error}</p>}
            <div className="form-container">
                <label>Selecione o Workshop:</label>
                <select value={workshopSelecionado} onChange={handleWorkshopChange}>
                    <option value="">-- Escolha um Workshop --</option>
                    {workshops.map((workshop) => (
                        <option key={workshop.id} value={workshop.id}>
                            {workshop.nome}
                        </option>
                    ))}
                </select>
            </div>

            {voluntarios.length > 0 && (
                <div className="voluntarios-lista">
                    <h2>Voluntários Participantes</h2>
                    <ul>
                        {voluntarios.map((voluntario) => (
                            <li key={voluntario.id}>
                                {voluntario.nome}
                                {certificadosGerados[voluntario.id] ? (
                                    <span className="certificado-gerado">Certificado Gerado</span>
                                ) : (
                                    <button onClick={() => gerarCertificado(voluntario)} disabled={loading}>
                                        {loading ? "Gerando..." : "Gerar Certificado"}
                                    </button>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {!workshopSelecionado && (
                <p className="mensagem-aviso">Selecione um workshop para ver os voluntários participantes.</p>
            )}
        </div>
    );
};

export default GerarCertificados;
