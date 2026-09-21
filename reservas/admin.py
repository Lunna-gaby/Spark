from django.contrib import admin
from django.utils.html import format_html
from .models import Equipamento, Reserva


admin.site.register(Equipamento)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_responsavel',
        'equipamento',
        'data',
        'hora',
        'hora_devolucao',
        'status_colorido',
    )

    list_filter = ('status', 'data')

    @admin.display(description='Status', ordering='status')
    def status_colorido(self, obj):
        cores = {
            'Pendente': '#f1c40f',
            'Aprovada': '#2ecc71',
            'Recusada': '#e74c3c',
            'Concluída': '#3498db',
        }

        cor = cores.get(obj.status, '#808080')

        return format_html(
            '<span style="color: {}; font-size: 18px;">●</span> {}',
            cor,
            obj.status
        )