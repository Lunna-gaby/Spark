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
    hora = Column(String)


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
    hora: str


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


                    <label for="hora">
                        Horário
                    </label>

                    <input
                        type="time"
                        id="hora"
                        required
                    >


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

                        hora:
                            document.getElementById("hora").value

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

            "quantidade": equipamento.quantidade

        })

    db.close()

    return resultado
   
# =========================
# PÁGINA DE EQUIPAMENTOS
# =========================

@app.get("/ver-equipamentos", response_class=HTMLResponse)
def pagina_equipamentos():

    db = SessionLocal()

    equipamentos = db.query(EquipamentoDB).all()

    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Equipamentos - ReservaEdu</title>

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
                background: linear-gradient(
                    135deg,
                    #075985,
                    #0e7490,
                    #15803d
                );

                color: white;
                padding: 30px 20px;
                text-align: center;
            }

            header h1 {
                font-size: 32px;
                margin-bottom: 8px;
            }

            header p {
                opacity: 0.9;
            }

            .container {
                width: 90%;
                max-width: 1000px;
                margin: 40px auto;
            }

            .grid {
                display: grid;

                grid-template-columns:
                    repeat(auto-fit, minmax(250px, 1fr));

                gap: 20px;
            }

            .card {
                background: white;

                padding: 25px;

                border-radius: 16px;

                box-shadow:
                    0 8px 25px rgba(0, 0, 0, 0.08);

                transition: 0.2s;
            }

            .card:hover {
                transform: translateY(-3px);

                box-shadow:
                    0 12px 30px rgba(0, 0, 0, 0.12);
            }

            .icone {
                width: 55px;
                height: 55px;

                display: flex;
                align-items: center;
                justify-content: center;

                background: #dcfce7;

                border-radius: 12px;

                font-size: 27px;

                margin-bottom: 18px;
            }

            .card h2 {
                color: #075985;

                margin-bottom: 10px;

                font-size: 21px;
            }

            .descricao {
                color: #64748b;

                line-height: 1.5;

                margin-bottom: 15px;
            }

            .quantidade {
                display: inline-block;

                background: #dcfce7;

                color: #166534;

                padding: 7px 12px;

                border-radius: 20px;

                font-size: 14px;

                font-weight: bold;
            }

            .vazio {
                background: white;

                padding: 40px;

                border-radius: 16px;

                text-align: center;

                color: #64748b;
            }

            .voltar {
                display: inline-block;

                margin-top: 30px;

                color: #075985;

                text-decoration: none;

                font-weight: bold;
            }

        </style>

    </head>

    <body>

        <header>

            <h1>📦 Equipamentos pedagógicos</h1>

            <p>
                Confira os equipamentos disponíveis para reserva.
            </p>

        </header>


        <div class="container">

            <div class="grid">
    """

    if equipamentos:

        for equipamento in equipamentos:

            html += f"""
                <div class="card">

                    <div class="icone">
                        📦
                    </div>

                    <h2>
                        {equipamento.nome}
                    </h2>

                    <p class="descricao">
                        {equipamento.descricao}
                    </p>

                    <span class="quantidade">
                        {equipamento.quantidade} disponível(is)
                    </span>

                </div>
            """

    else:

        html += """
            </div>

            <div class="vazio">

                <h2>Nenhum equipamento cadastrado.</h2>

                <p>
                    Ainda não existem equipamentos disponíveis.
                </p>

            </div>
        """

    html += """
            </div>

            <a href="/" class="voltar">
                ← Voltar para a página inicial
            </a>

        </div>

    </body>

    </html>
    """

    db.close()

    return HTMLResponse(content=html)


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

        hora=reserva.hora

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

        "hora": nova_reserva.hora

    }

    db.close()

    return {

        "mensagem":
            "Reserva realizada com sucesso!",

        "reserva":
            resultado

    }


# =========================
# LISTAR RESERVAS
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
            "hora": reserva.hora
        })

    db.close()

    return resultado
    # =========================
# PÁGINA DE RESERVAS REALIZADAS
# =========================

@app.get("/reservas-realizadas", response_class=HTMLResponse)
def pagina_reservas_realizadas():

    db = SessionLocal()

    reservas = db.query(ReservaDB).all()

    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Reservas Realizadas - ReservaEdu</title>

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
                background: linear-gradient(
                    135deg,
                    #075985,
                    #0e7490,
                    #15803d
                );

                color: white;
                padding: 30px 20px;
                text-align: center;
            }

            header h1 {
                font-size: 32px;
                margin-bottom: 8px;
            }

            header p {
                opacity: 0.9;
            }

            .container {
                width: 90%;
                max-width: 1000px;
                margin: 40px auto;
            }

            .grid {
                display: grid;

                grid-template-columns:
                    repeat(auto-fit, minmax(280px, 1fr));

                gap: 20px;
            }

            .card {
                background: white;

                padding: 25px;

                border-radius: 16px;

                box-shadow:
                    0 8px 25px rgba(0, 0, 0, 0.08);
            }

            .icone {
                width: 55px;
                height: 55px;

                display: flex;
                align-items: center;
                justify-content: center;

                background: #dbeafe;

                border-radius: 12px;

                font-size: 27px;

                margin-bottom: 18px;
            }

            .card h2 {
                color: #075985;

                margin-bottom: 15px;

                font-size: 21px;
            }

            .informacao {
                margin-bottom: 10px;

                color: #475569;
            }

            .informacao strong {
                color: #1e293b;
            }

            .vazio {
                background: white;

                padding: 40px;

                border-radius: 16px;

                text-align: center;

                color: #64748b;
            }

            .voltar {
                display: inline-block;

                margin-top: 30px;

                color: #075985;

                text-decoration: none;

                font-weight: bold;
            }

        </style>

    </head>

    <body>

        <header>

            <h1>📅 Reservas realizadas</h1>

            <p>
                Confira as reservas cadastradas no sistema.
            </p>

        </header>


        <div class="container">

    """

    if reservas:

        html += '<div class="grid">'

        for reserva in reservas:

            html += f"""
                <div class="card">

                    <div class="icone">
                        📅
                    </div>

                    <h2>
                        {reserva.equipamento}
                    </h2>

                    <p class="informacao">
                        <strong>Aluno:</strong>
                        {reserva.nome_aluno}
                    </p>

                    <p class="informacao">
                        <strong>Matrícula:</strong>
                        {reserva.matricula}
                    </p>

                    <p class="informacao">
                        <strong>Data:</strong>
                        {reserva.data}
                    </p>

                    <p class="informacao">
                        <strong>Horário:</strong>
                        {reserva.hora}
                    </p>

                </div>
            """

        html += "</div>"

    else:

        html += """
            <div class="vazio">

                <h2>Nenhuma reserva realizada.</h2>

                <p>
                    Ainda não existem reservas cadastradas.
                </p>

            </div>
        """

    html += """

            <a href="/" class="voltar">
                ← Voltar para a página inicial
            </a>

        </div>

    </body>

    </html>
    """

    db.close()

    return HTMLResponse(content=html)
