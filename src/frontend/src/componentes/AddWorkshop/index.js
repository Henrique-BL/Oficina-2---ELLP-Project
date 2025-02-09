import { useState, useEffect } from "react";
import axios from "axios";
import "./addWorkshop.css";

export default function CadastroWorkshop() {
    const [workshops, setWorkshops] = useState([]);
    const [volunteers, setVolunteers] = useState([]);
    const [selectedWorkshop, setSelectedWorkshop] = useState(null);
    const [selectedVolunteers, setSelectedVolunteers] = useState([]);
    const [workshopData, setWorkshopData] = useState({
        name: "",
        date: "",
        description: "",
        workload: "",
    });

    useEffect(() => {
        const fetchWorkshops = async () => {    
        // Carregar workshops existentes
        await axios
            .get("http://localhost:8000/workshops")
            .then((response) => {
                setWorkshops(response.data);
            })
            .catch((error) => {
                console.error("Erro ao carregar workshops:", error);
            });

        // Carregar voluntários cadastrados
        await axios
            .get("http://localhost:8000/volunteers")
            .then((response) => {
                setVolunteers(response.data);
            })

            .catch((error) => {
                console.error("Erro ao carregar voluntários:", error);
            });
        };
        fetchWorkshops();
    }, []);


    const handleWorkshopChange = (e) => {
        setWorkshopData({ ...workshopData, [e.target.name]: e.target.value });
    };

    const handleWorkshopSubmit = async () => {
        try {
            const response = await axios.post("http://localhost:8000/workshops/", workshopData);
            setWorkshops([...workshops, response.data]);
            setWorkshopData({ name: "", date: "", description: "", workload: "" });
        } catch (error) {
            console.error("Erro ao cadastrar workshop:", error);
        }
    };

    const handleVolunteerSelect = (volunteerId) => {
        setSelectedVolunteers((prev) =>
            prev.includes(volunteerId) ? prev.filter((id) => id !== volunteerId) : [...prev, volunteerId]
        );
    };

    const handleVolunteerSubmit = async () => {
        if (selectedWorkshop) {
            try {
                await axios.post(`http://localhost:8000/volunteers/workshops/${selectedWorkshop}`, {
                    volunteers: selectedVolunteers
                });
                // Atualiza a lista de workshops com os novos voluntários

                const updatedWorkshop = await axios.get(`http://localhost:8000/workshops/${selectedWorkshop}`);
                setWorkshops(workshops.map((w) => (w.id === selectedWorkshop ? updatedWorkshop.data : w)));
                setSelectedVolunteers([]);
            } catch (error) {
                console.error("Erro ao incluir voluntários no workshop:", error);
            }
        }
    };

    return (
        <div className="add-volunteer-container">
            <div className="header">
                <h1>Cadastro de Workshop</h1>
                <p>Cadastre um novo workshop e adicione voluntários.</p>
            </div>

            <div className="form-container">
                <h2>Cadastro de Workshop</h2>
                <fieldset>
                    <legend>Detalhes do Workshop</legend>
                    <div className="input-group">
                        <label>Nome:</label>
                        <input
                            type="text"
                            name="name"
                            placeholder="Nome do Workshop"
                            value={workshopData.name}
                            onChange={handleWorkshopChange}
                        />
                    </div>
                    <div className="input-group date-picker-container">
                        <label>Data:</label>
                        <input type="date" name="date" value={workshopData.date} onChange={handleWorkshopChange} />
                    </div>
                    <div className="input-group">
                        <label>Descrição:</label>
                        <input
                            type="text"
                            name="description"
                            placeholder="Descrição"
                            value={workshopData.description}
                            onChange={handleWorkshopChange}
                        />
                    </div>
                    <div className="input-group">
                        <label>Carga Horária:</label>
                        <input
                            type="text"
                            name="workload"
                            placeholder="Carga Horária"
                            value={workshopData.workload}
                            onChange={handleWorkshopChange}
                        />
                    </div>
                    <button className="btn-cadastrar" onClick={handleWorkshopSubmit}>
                        Cadastrar Workshop
                    </button>
                </fieldset>
            </div>

            <div className="form-container">
                <h2>Incluir Voluntários</h2>
                <fieldset>
                    <legend>Selecione um Workshop</legend>
                    <select onChange={(e) => setSelectedWorkshop(e.target.value)}>
                        <option value="">Selecione um Workshop</option>
                        {workshops.map((workshop) => (
                            <option key={workshop.id} value={workshop.id}>
                                {workshop.name}
                            </option>
                        ))}
                    </select>
                </fieldset>

                <fieldset>
                    <legend>Voluntários Cadastrados</legend>
                    {volunteers.map((volunteer) => (
                        <div key={volunteer.id}>
                            <input
                                type="checkbox"
                                checked={selectedVolunteers.includes(volunteer.id)}
                                onChange={() => handleVolunteerSelect(volunteer.id)}
                            />
                            {volunteer.name}
                        </div>
                    ))}
                </fieldset>
                <button className="btn-cadastrar" onClick={handleVolunteerSubmit} disabled={!selectedWorkshop}>
                    Incluir Voluntários
                </button>
            </div>
        </div>
    );
}
