from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipamento, Reserva
from .forms import ReservaForm


def inicio(request):
    return render(request, 'reservas/index.html')


def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all()

    return render(request, 'reservas/equipamentos.html', {
        'equipamentos': equipamentos
    })


def fazer_reserva(request):
    sucesso = False

    if request.method == 'POST':
        form = ReservaForm(request.POST)

        if form.is_valid():
            form.save()
            sucesso = True
            form = ReservaForm()
    else:
        form = ReservaForm()

    return render(request, 'reservas/reserva.html', {
        'form': form,
        'sucesso': sucesso
    })


def reservas_realizadas(request):
    reservas = Reserva.objects.all().order_by('-id')

    return render(request, 'reservas/reservas_realizadas.html', {
        'reservas': reservas
    })
def excluir_reserva(request, id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=id)
        reserva.delete()

    return redirect('reservas_realizadas')