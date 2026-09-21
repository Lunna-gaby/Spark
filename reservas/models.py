from django.db import models


class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    nome_responsavel = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovada', 'Aprovada'),
        ('Recusada', 'Recusada'),
        ('Concluída', 'Concluída'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente'
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE
    )

    data = models.DateField()
    hora = models.TimeField()
    hora_devolucao = models.TimeField()

    def __str__(self):
        return f"{self.nome_responsavel} - {self.equipamento.nome}"