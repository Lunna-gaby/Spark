from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipamento, Reserva
from .forms import ReservaForm


# =========================
# VERIFICAÇÃO DA DIREÇÃO
# =========================

def is_direcao(user):
    return user.is_authenticated and user.is_staff


# =========================
# PÁGINA INICIAL
# =========================

@login_required
def inicio(request):
    return render(request, 'reservas/index.html')


# =========================
# EQUIPAMENTOS
# =========================

@login_required
def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all()

    return render(request, 'reservas/equipamentos.html', {
        'equipamentos': equipamentos
    })


# =========================
# RESERVA
# =========================

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


# =========================
# MINHAS RESERVAS
# =========================

@login_required
def reservas_realizadas(request):
    reservas = Reserva.objects.filter(
        usuario=request.user
    ).order_by('-id')

    return render(request, 'reservas/reservas_realizadas.html', {
        'reservas': reservas
    })


# =========================
# EXCLUIR MINHA RESERVA
# =========================

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


# =========================
# LOGIN
# =========================

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

            if usuario.is_staff:
                return redirect('area_direcao')

            return redirect('equipamentos')

        else:
            erro = 'Usuário ou senha incorretos.'

    return render(request, 'reservas/login.html', {
        'erro': erro
    })


# =========================
# CADASTRO
# =========================

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


# =========================
# ÁREA DA DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def area_direcao(request):
    return render(request, 'reservas/direcao.html')


# =========================
# RESERVAS DA DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def direcao_reservas(request):
    reservas = Reserva.objects.all().order_by('-id')

    return render(request, 'reservas/direcao_reservas.html', {
        'reservas': reservas
    })


# =========================
# APROVAR RESERVA
# =========================

@user_passes_test(is_direcao)
def aprovar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    reserva.status = 'Aprovada'
    reserva.save()

    messages.success(
        request,
        'Reserva aprovada com sucesso!'
    )

    return redirect('direcao_reservas')


# =========================
# RECUSAR RESERVA
# =========================

@user_passes_test(is_direcao)
def recusar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    reserva.status = 'Recusada'
    reserva.save()

    messages.error(
        request,
        'Reserva recusada.'
    )

    return redirect('direcao_reservas')


# =========================
# EXCLUIR RESERVA - DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def excluir_reserva_direcao(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        reserva.delete()

    return redirect('direcao_reservas')


# =========================
# EQUIPAMENTOS - DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def direcao_equipamentos(request):
    equipamentos = Equipamento.objects.all().order_by('nome')

    return render(request, 'reservas/direcao_equipamentos.html', {
        'equipamentos': equipamentos
    })


# =========================
# USUÁRIOS - DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def direcao_usuarios(request):
    usuarios = User.objects.all().order_by('username')

    return render(request, 'reservas/direcao_usuarios.html', {
        'usuarios': usuarios
    })


# =========================
# EXCLUIR USUÁRIO - DIREÇÃO
# =========================

@user_passes_test(is_direcao)
def excluir_usuario_direcao(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        usuario.delete()

    return redirect('direcao_usuarios')