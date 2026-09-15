from main import SessionLocal, EquipamentoDB

db = SessionLocal()

equipamentos = [
    EquipamentoDB(
        nome="Projetor",
        descricao="Projetor multimídia para apresentações",
        quantidade=2
    ),
    EquipamentoDB(
        nome="Notebook",
        descricao="Notebook para atividades pedagógicas",
        quantidade=5
    ),
    EquipamentoDB(
        nome="Caixa de Som",
        descricao="Caixa de som para eventos e apresentações",
        quantidade=3
    ),
    EquipamentoDB(
        nome="Microfone",
        descricao="Microfone para apresentações e eventos",
        quantidade=4
    )
]

db.add_all(equipamentos)
db.commit()
db.close()

print("Equipamentos cadastrados com sucesso!")