from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = [
            'nome_responsavel',
            'matricula',
            'equipamento',
            'data',
            'hora',
            'hora_devolucao',
        ]

        labels = {
            'nome_responsavel': 'Nome do responsável',
            'matricula': 'Matrícula',
            'equipamento': 'Equipamento desejado',
            'data': 'Data da reserva',
            'hora': 'Horário de retirada',
            'hora_devolucao': 'Horário de devolução',
        }

        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'hora': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time', 'step': '60'}
            ),

            'hora_devolucao': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time', 'step': '60'}
            ),
        }