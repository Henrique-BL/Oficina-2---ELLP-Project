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
        const fetchWorkshops = async () => {
            // Carregar workshops ao montar o componente
            await axios
                .get("http://localhost:8000/workshops")

            .then((response) => {
                console.log("Workshops", response.data);
                setWorkshops(response.data);
            })
            .catch((err) => {
                setError("Erro ao carregar workshops");
                    console.error(err);
                });
        };
        fetchWorkshops();
    }, []);


    // Atualiza a lista de voluntários ao selecionar um workshop
    const handleWorkshopChange = (event) => {
        const idSelecionado = event.target.value;
        console.log(idSelecionado);
        setWorkshopSelecionado(idSelecionado);

        if (idSelecionado) {
            const fetchVolunteers = async () => {
                await axios
                    .get(`http://localhost:8000/volunteers/workshops/${idSelecionado}`)
                    .then((response) => {

                    setVoluntarios(response.data);
                })

                .catch((err) => {
                    setError("Erro ao carregar voluntários");
                    console.error(err);
                });
            };
            fetchVolunteers();
        } else {
            setVoluntarios([]);
        }

    };

    // Função para gerar certificado em PDF
    const gerarCertificado = async (voluntario) => {
        if (certificadosGerados[voluntario.id]) return;

        setLoading(true);

        try {
            const workshop = workshops.find((w) => w.id === workshopSelecionado);
            if (!workshop) {
                setError("Workshop não encontrado");
                return;
            }

            // Chamada ao back-end para gerar certificado
            // const response = await axios.get(`http://localhost:8000/volunteers/${voluntario.id}/workshops/${workshop.id}`);


            setCertificadosGerados((prev) => ({
                ...prev,
                [voluntario.id]: true,
            }));

            // Supondo que o back-end retorna o PDF ou informações necessárias para gerá-lo
            // console.log("Certificado Gerado:", response.data);

            const doc = new jsPDF();

            doc.setFont("helvetica", "bold");
            doc.setFontSize(22);
            doc.text("Certificado de Participação", 50, 30);

            doc.setFont("helvetica", "normal");
            doc.setFontSize(16);
            doc.text(`Certificamos que ${voluntario.name}`, 20, 50);
            doc.text(`participou do workshop "${workshop.name}"`, 20, 60);
            doc.text(`com carga horária de ${workshop.workload} horas.`, 20, 70);


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
                            {workshop.name}
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
                                {voluntario.name}
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
