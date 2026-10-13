from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================
# BANCO DE DADOS
# =========================

DATABASE_URL = "sqlite:///./reservas.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# =========================
# TABELA DE EQUIPAMENTOS
# =========================

class EquipamentoDB(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    quantidade = Column(Integer)


# =========================
# TABELA DE RESERVAS
# =========================

class ReservaDB(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    nome_aluno = Column(String)
    matricula = Column(String)
    equipamento = Column(String)
    data = Column(String)
    hora_retirada = Column(String)
    hora_devolucao = Column(String)
    status = Column(String, default="Ativa")
# =========================
# CRIAR TABELAS
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="ReservaEdu",
    description="Sistema de Reserva de Equipamentos Pedagógicos",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# =========================
# MODELO DO EQUIPAMENTO
# =========================

class Equipamento(BaseModel):
    nome: str
    descricao: str
    quantidade: int


# =========================
# MODELO DA RESERVA
# =========================

class Reserva(BaseModel):
    nome_aluno: str
    matricula: str
    equipamento: str
    data: str
    hora_retirada: str
    hora_devolucao: str

# =========================
# PÁGINA INICIAL
# =========================

@app.get("/")
def inicio():
    return FileResponse("index.html")


# =========================
# PÁGINA DE RESERVAS
# =========================

@app.get("/reservas", response_class=HTMLResponse)
def pagina_reservas():

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Fazer Reserva - ReservaEdu</title>

        <style>

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, Helvetica, sans-serif;
                background: #f3f6fa;
                color: #1e293b;
            }

            header {
                background: #075985;
                color: white;
                padding: 20px 40px;
            }

            header h1 {
                font-size: 28px;
            }

            header p {
                margin-top: 5px;
                opacity: 0.9;
            }

            .container {
                width: 90%;
                max-width: 700px;
                margin: 40px auto;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 16px;

                box-shadow:
                    0 8px 25px rgba(0, 0, 0, 0.08);
            }

            h2 {
                color: #075985;
                margin-bottom: 25px;
            }

            label {
                display: block;
                margin-bottom: 7px;
                font-weight: bold;
            }

            input,
            select {
                width: 100%;
                padding: 13px;
                margin-bottom: 20px;

                border: 1px solid #cbd5e1;
                border-radius: 8px;

                font-size: 16px;
            }

            input:focus,
            select:focus {
                outline: none;
                border-color: #16a34a;
            }

            button {
                width: 100%;
                padding: 14px;

                border: none;
                border-radius: 8px;

                background: #16a34a;
                color: white;

                font-size: 16px;
                font-weight: bold;

                cursor: pointer;
            }

            button:hover {
                background: #15803d;
            }

            .voltar {
                display: inline-block;
                margin-top: 20px;

                color: #075985;
                text-decoration: none;
                font-weight: bold;
            }

            .mensagem {
                display: none;

                margin-bottom: 20px;
                padding: 15px;

                border-radius: 8px;

                background: #dcfce7;
                color: #166534;
            }

        </style>

    </head>

    <body>

        <header>

            <h1>ReservaEdu</h1>

            <p>Reserva de Equipamentos Pedagógicos</p>

        </header>


        <div class="container">

            <div class="card">

                <h2>📅 Fazer uma reserva</h2>

                <div id="mensagem"
                     class="mensagem">
                </div>


                <form id="formReserva">

                    <label for="nome">
                        Nome do aluno
                    </label>

                    <input
                        type="text"
                        id="nome"
                        placeholder="Digite seu nome"
                        required
                    >


                    <label for="matricula">
                        Matrícula
                    </label>

                    <input
                        type="text"
                        id="matricula"
                        placeholder="Digite sua matrícula"
                        required
                    >


                    <label for="equipamento">
                        Equipamento
                    </label>

                    <select
                        id="equipamento"
                        required
                    >

                        <option value="">
                            Carregando equipamentos...
                        </option>

                    </select>


                    <label for="data">
                        Data da reserva
                    </label>

                    <input
                        type="date"
                        id="data"
                        required
                    >


                   <label for="hora_retirada">Horário de retirada</label>
<input type="time" id="hora_retirada" required>

<label for="hora_devolucao">Horário de devolução</label>
<input type="time" id="hora_devolucao" required>

                    <button type="submit">
                        Confirmar reserva
                    </button>

                </form>


                <a href="/" class="voltar">
                    ← Voltar para a página inicial
                </a>

            </div>

        </div>


        <script>

            // =========================
            // CARREGAR EQUIPAMENTOS
            // =========================

            async function carregarEquipamentos() {

                const select =
                    document.getElementById("equipamento");

                try {

                    const resposta =
                        await fetch("/equipamentos");

                    const equipamentos =
                        await resposta.json();

                    select.innerHTML =
                        '<option value="">Selecione um equipamento</option>';

                    equipamentos.forEach(equipamento => {

                        const option =
                            document.createElement("option");

                        option.value =
                            equipamento.nome;

                        option.textContent =
                            equipamento.nome +
                            " - " +
                            equipamento.quantidade +
                            " disponível(is)";

                        select.appendChild(option);

                    });

                } catch (erro) {

                    select.innerHTML =
                        '<option value="">Erro ao carregar equipamentos</option>';

                }

            }


            // =========================
            // ENVIAR RESERVA
            // =========================

            document
                .getElementById("formReserva")
                .addEventListener("submit", async function(event) {

                    event.preventDefault();

                    const dados = {

    nome_aluno:
        document.getElementById("nome").value,

    matricula:
        document.getElementById("matricula").value,

    equipamento:
        document.getElementById("equipamento").value,

    data:
        document.getElementById("data").value,

    hora_retirada:
        document.getElementById("hora_retirada").value,

    hora_devolucao:
        document.getElementById("hora_devolucao").value

};

                    try {

                        const resposta =
                            await fetch("/reservas", {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(dados)

                            });


                        const resultado =
                            await resposta.json();


                        const mensagem =
                            document.getElementById("mensagem");


                        if (resposta.ok) {

                            mensagem.style.display = "block";

                            mensagem.textContent =
                                "✅ " +
                                resultado.mensagem;

                            document
                                .getElementById("formReserva")
                                .reset();

                        } else {

                            mensagem.style.display = "block";

                            mensagem.textContent =
                                "❌ Não foi possível realizar a reserva.";

                        }

                    } catch (erro) {

                        alert(
                            "Erro ao conectar com o servidor."
                        );

                    }

                });


            // Carregar equipamentos
            carregarEquipamentos();

        </script>

    </body>

    </html>
    """


# =========================
# LISTAR EQUIPAMENTOS
# =========================

@app.get("/equipamentos")
def listar_equipamentos():

    db = SessionLocal()

    equipamentos = db.query(EquipamentoDB).all()

    resultado = []

    for equipamento in equipamentos:

        resultado.append({

            "id": equipamento.id,

            "nome": equipamento.nome,

            "descricao": equipamento.descricao,

            "quantidade": equipamento.quantidade,

        })

    db.close()

    return resultado


# =========================
# CRIAR RESERVA
# =========================

@app.post("/reservas")
def criar_reserva(reserva: Reserva):
    db = SessionLocal()

    nova_reserva = ReservaDB(
        nome_aluno=reserva.nome_aluno,
        matricula=reserva.matricula,
        equipamento=reserva.equipamento,
        data=reserva.data,
        hora_retirada=reserva.hora_retirada,
        hora_devolucao=reserva.hora_devolucao,
        status="Ativa"
    )

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    resultado = {
        "id": nova_reserva.id,
        "nome_aluno": nova_reserva.nome_aluno,
        "matricula": nova_reserva.matricula,
        "equipamento": nova_reserva.equipamento,
        "data": nova_reserva.data,
        "hora_retirada": nova_reserva.hora_retirada,
        "hora_devolucao": nova_reserva.hora_devolucao,
        "status": nova_reserva.status
    }

    db.close()

    return {
        "mensagem": "Reserva realizada com sucesso!",
        "reserva": resultado
    }


# =========================
# PÁGINA DE RESERVAS REALIZADAS
# =========================

@app.get("/reservas-realizadas", response_class=HTMLResponse)
def pagina_reservas_realizadas():
    return """
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Reservas Realizadas - ReservaEdu</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #075985, #16a34a);
            padding: 40px 20px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
        }

        .topo {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            gap: 20px;
        }

        h1 {
            color: white;
            font-size: 32px;
        }

        .subtitulo {
            color: #e0f2fe;
            margin-top: 8px;
        }

        .voltar {
            text-decoration: none;
            background: white;
            color: #075985;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: bold;
        }

        .voltar:hover {
            background: #f1f5f9;
        }

        #lista {
            display: grid;
            gap: 18px;
        }

        .reserva {
            background: white;
            border-radius: 15px;
            padding: 22px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }

        .reserva h2 {
            color: #075985;
            margin-bottom: 15px;
        }

        .informacao {
            margin: 8px 0;
            color: #334155;
        }

        .informacao strong {
            color: #0f172a;
        }

        .acoes {
            margin-top: 18px;
            display: flex;
            justify-content: flex-end;
        }

        .excluir {
            border: none;
            background: #dc2626;
            color: white;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }

        .excluir:hover {
            background: #b91c1c;
        }

        .vazio {
            background: white;
            padding: 40px;
            text-align: center;
            border-radius: 15px;
            color: #475569;
        }

        .carregando {
            color: white;
            text-align: center;
            font-size: 18px;
        }
    </style>
</head>

<body>

    <div class="container">

        <div class="topo">
            <div>
                <h1>📋 Reservas realizadas</h1>
                <p class="subtitulo">
                    Consulte e gerencie as reservas do ReservaEdu.
                </p>
            </div>

            <a href="/" class="voltar">
                ← Voltar
            </a>
        </div>

        <div id="lista">
            <p class="carregando">Carregando reservas...</p>
        </div>

    </div>

    <script>

        async function carregarReservas() {

            const lista = document.getElementById("lista");

            try {

                const resposta = await fetch("/api/reservas");

                if (!resposta.ok) {
                    throw new Error("Erro ao carregar reservas");
                }

                const reservas = await resposta.json();

                lista.innerHTML = "";

                if (reservas.length === 0) {

                    lista.innerHTML = `
                        <div class="vazio">
                            <h2>📭 Nenhuma reserva encontrada</h2>
                            <p>Quando uma reserva for realizada, ela aparecerá aqui.</p>
                        </div>
                    `;

                    return;
                }

                reservas.forEach(reserva => {

                    const card = document.createElement("div");

                    card.className = "reserva";

                    card.innerHTML = `
                        <h2>📅 Reserva #${reserva.id}</h2>

                        <p class="informacao">
                            <strong>Aluno:</strong>
                            ${reserva.nome_aluno}
                        </p>

                        <p class="informacao">
                            <strong>Matrícula:</strong>
                            ${reserva.matricula}
                        </p>

                        <p class="informacao">
                            <strong>Equipamento:</strong>
                            ${reserva.equipamento}
                        </p>

                        <p class="informacao">
                            <strong>Data:</strong>
                            ${reserva.data}
                        </p>

                       <p class="informacao">
    <strong>Retirada:</strong>
    ${reserva.hora_retirada}
</p>

<p class="informacao">
    <strong>Devolução:</strong>
    ${reserva.hora_devolucao}
</p>

<p class="informacao">
    <strong>Status:</strong>
    🟢 ${reserva.status}
</p>

                        <div class="acoes">

    <select
        onchange="alterarStatus(${reserva.id}, this.value)"
        style="
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            margin-right: 10px;
            font-weight: bold;
        "
    >
        <option value="Ativa" ${reserva.status === "Ativa" ? "selected" : ""}>
            🟢 Ativa
        </option>

        <option value="Em andamento" ${reserva.status === "Em andamento" ? "selected" : ""}>
            🟡 Em andamento
        </option>

        <option value="Devolvida" ${reserva.status === "Devolvida" ? "selected" : ""}>
            🔵 Devolvida
        </option>

        <option value="Cancelada" ${reserva.status === "Cancelada" ? "selected" : ""}>
            🔴 Cancelada
        </option>
    </select>

    <button
        class="excluir"
        onclick="excluirReserva(${reserva.id})">
        🗑️ Excluir
    </button>

</div>

                    lista.appendChild(card);

                });

            } catch (erro) {

                lista.innerHTML = `
                    <div class="vazio">
                        <h2>❌ Erro</h2>
                        <p>Não foi possível carregar as reservas.</p>
                    </div>
                `;

                console.error(erro);
            }
        }


        async function excluirReserva(id) {

            const confirmar = confirm(
                "Tem certeza que deseja excluir esta reserva?"
            );

            if (!confirmar) {
                return;
            }
async function alterarStatus(id, status) {

    try {

        const resposta = await fetch(
            `/reservas/${id}/status?status=${encodeURIComponent(status)}`,
            {
                method: "PUT"
            }
        );

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert("❌ Não foi possível alterar o status.");
            return;
        }

        alert("✅ Status alterado com sucesso!");

        carregarReservas();

    } catch (erro) {

        console.error(erro);

        alert("❌ Erro ao alterar o status.");
    }
}
            try {

                const resposta = await fetch(
                    `/reservas/${id}`,
                    {
                        method: "DELETE"
                    }
                );

                const resultado = await resposta.json();

                if (!resposta.ok) {
                    alert("Não foi possível excluir a reserva.");
                    return;
                }

                alert("✅ Reserva excluída com sucesso!");

                carregarReservas();

            } catch (erro) {

                console.error(erro);

                alert(
                    "❌ Erro ao tentar excluir a reserva."
                );
            }
        }


        carregarReservas();

    </script>

</body>
</html>
"""
@app.delete("/reservas/{reserva_id}")
def excluir_reserva(reserva_id: int):
    db = SessionLocal()

    reserva = db.query(ReservaDB).filter(
        ReservaDB.id == reserva_id
    ).first()

    if reserva is None:
        db.close()
        return {"erro": "Reserva não encontrada"}

    db.delete(reserva)
    db.commit()
    db.close()

    return {"mensagem": "Reserva excluída com sucesso!"}
@app.put("/reservas/{reserva_id}/status")
def alterar_status(reserva_id: int, status: str):
    db = SessionLocal()

    reserva = db.query(ReservaDB).filter(
        ReservaDB.id == reserva_id
    ).first()

    if reserva is None:
        db.close()
        return {"erro": "Reserva não encontrada"}

    status_validos = [
        "Ativa",
        "Em andamento",
        "Devolvida",
        "Cancelada"
    ]

    if status not in status_validos:
        db.close()
        return {"erro": "Status inválido"}

    reserva.status = status

    db.commit()
    db.refresh(reserva)

    db.close()

    return {
        "mensagem": "Status alterado com sucesso!",
        "status": reserva.status
    }
# =========================
# API PARA LISTAR RESERVAS
# =========================

@app.get("/api/reservas")
def listar_reservas():
    db = SessionLocal()
    reservas = db.query(ReservaDB).all()
    resultado = []

    for reserva in reservas:
       resultado.append({
    "id": reserva.id,
    "nome_aluno": reserva.nome_aluno,
    "matricula": reserva.matricula,
    "equipamento": reserva.equipamento,
    "data": reserva.data,
    "hora_retirada": reserva.hora_retirada,
    "hora_devolucao": reserva.hora_devolucao,
    "status": reserva.status
})

    db.close()

    return resultado