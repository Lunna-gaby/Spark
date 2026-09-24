from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipamento, Reserva
from .forms import ReservaForm


@login_required
def inicio(request):
    return render(request, 'reservas/index.html')

@login_required
def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all()

    return render(request, 'reservas/equipamentos.html', {
        'equipamentos': equipamentos
    })

@login_required
def fazer_reserva(request):
    sucesso = False

    if request.method == 'POST':
        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()

            sucesso = True
            form = ReservaForm()
    else:
        form = ReservaForm()

    return render(request, 'reservas/reserva.html', {
        'form': form,
        'sucesso': sucesso
    })
@login_required
def reservas_realizadas(request):
    reservas = Reserva.objects.filter(
        usuario=request.user
    ).order_by('-id')

    return render(request, 'reservas/reservas_realizadas.html', {
        'reservas': reservas
    })

@login_required
def excluir_reserva(request, id):
    if request.method == 'POST':
        reserva = get_object_or_404(
            Reserva,
            id=id,
            usuario=request.user
        )
        reserva.delete()

    return redirect('reservas_realizadas')

def fazer_login(request):
    erro = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')
        else:
            erro = 'Usuário ou senha incorretos.'

    return render(request, 'reservas/login.html', {
        'erro': erro
    })


def fazer_cadastro(request):
    erro = ''

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')

        if senha != confirmar_senha:
            erro = 'As senhas não coincidem.'

        elif User.objects.filter(username=username).exists():
            erro = 'Esse nome de usuário já está em uso.'

        elif User.objects.filter(email=email).exists():
            erro = 'Esse e-mail já está cadastrado.'

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=nome
            )

            return redirect('login')

    return render(request, 'reservas/cadastro.html', {
        'erro': erro
    })