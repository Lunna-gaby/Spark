from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        equipamento = cleaned_data.get('equipamento')
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        hora_devolucao = cleaned_data.get('hora_devolucao')

        if not all([equipamento, data, hora, hora_devolucao]):
            return cleaned_data

        if hora_devolucao <= hora:
            self.add_error(
                'hora_devolucao',
                'A devolução deve ser após o horário de retirada.'
            )
            return cleaned_data

        conflitos = Reserva.objects.filter(
            equipamento=equipamento,
            data=data,
            hora__lt=hora_devolucao,
            hora_devolucao__gt=hora,
            status__in=['Pendente', 'Aprovada']
        )

        if conflitos.count() >= equipamento.quantidade:
            raise forms.ValidationError(
                'Não há unidades disponíveis desse equipamento '
                'nesse horário. Escolha outro horário.'
            )

        return cleaned_data

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