import { useState } from "react";
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
        workload: "", // Novo campo para carga horária
    });

    const handleWorkshopChange = (e) => {
        setWorkshopData({ ...workshopData, [e.target.name]: e.target.value });
    };

    const handleWorkshopSubmit = () => {
        const newWorkshop = { ...workshopData, id: Date.now() };
        setWorkshops([...workshops, newWorkshop]);
        setWorkshopData({ name: "", date: "", description: "", workload: "" }); // Limpa o campo de carga horária também
    };

    const handleVolunteerSelect = (volunteerId) => {
        setSelectedVolunteers((prev) =>
            prev.includes(volunteerId) ? prev.filter((id) => id !== volunteerId) : [...prev, volunteerId]
        );
    };

    const handleVolunteerSubmit = () => {
        if (selectedWorkshop) {
            const updatedWorkshops = workshops.map((w) =>
                w.id === selectedWorkshop ? { ...w, volunteers: [...(w.volunteers || []), ...selectedVolunteers] } : w
            );
            setWorkshops(updatedWorkshops);
            setSelectedVolunteers([]);
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
                <button className="btn-cadastrar" onClick={handleVolunteerSubmit}>
                    Incluir Voluntários
                </button>
            </div>
        </div>
    );
}
