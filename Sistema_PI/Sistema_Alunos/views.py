from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlunoForm
from .models import Aluno, Nota # <-- AQUI ESTÁ A CORREÇÃO
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NotaForm # <-- Importe NotaForm aqui

def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

@login_required(login_url='login')
def index(request):
    anos = [f"{i}ª Ano" for i in range(1, 10)]
    return render(request, 'index.html', {'anos': anos})

@login_required(login_url='login')
def cadastro(request):
    return render(request, 'cadastro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@permission_required('Sistema_Alunos.add_aluno', raise_exception=True)
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AlunoForm()
    return render(request, 'cadastro.html', {'form': form})

@login_required(login_url='login')
def buscar_aluno(request):
    query = request.GET.get('q', '').strip()
    serie = request.GET.get('serie', '').strip()
    turma = request.GET.get('turma', '').strip()
    periodo = request.GET.get('periodo', '').strip()
    filtros = Q()
    if query:
        query_sem_acento = remover_acentos(query).lower()
        filtros &= (
            Q(nome__icontains=query_sem_acento) |
            Q(nome_social__icontains=query_sem_acento) |
            Q(id_aluno__icontains=query_sem_acento)
        )
    if serie:
        filtros &= Q(serie=serie)
    if turma:
        filtros &= Q(turma=turma)
    if periodo:
        filtros &= Q(periodo=periodo)
    alunos = Aluno.objects.filter(filtros)
    resultado = [
        {
            'id_aluno': aluno.id_aluno,
            'nome': aluno.nome,
            'nome_social': aluno.nome_social,
            'serie': aluno.serie,
            'turma': aluno.turma,
            'periodo': aluno.periodo,
            'foto': aluno.foto.url if aluno.foto else ''
        }
        for aluno in alunos
    ]
    return JsonResponse(resultado, safe=False)

@login_required(login_url='login')
def detalhes_aluno(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    return render(request, 'detalhes_aluno.html', {'aluno': aluno})

@login_required(login_url='login')
@permission_required('Sistema_Alunos.change_aluno', raise_exception=True)
def editar_aluno(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('detalhes_aluno', id_aluno=aluno.id_aluno)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'editar_aluno.html', {'form': form, 'aluno': aluno})

@login_required(login_url='login')
@permission_required('Sistema_Alunos.delete_aluno', raise_exception=True)
def excluir_aluno(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    if request.method == 'POST':
        aluno.delete()
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'aluno': aluno})

@login_required(login_url='login')
def editar_notas(request, id_aluno):
    aluno = get_object_or_404(Aluno, id_aluno=id_aluno)
    nota, created = Nota.objects.get_or_create(aluno=aluno)

    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('detalhes_aluno', id_aluno=aluno.id_aluno)
    else:
        form = NotaForm(instance=nota)

    return render(request, 'editar_notas.html', {'aluno': aluno, 'form': form})

# AQUI ESTÁ A VIEW DO DASHBOARD ADICIONADA
@login_required(login_url='login')
def dashboard(request):
    total_alunos = Aluno.objects.count()
    total_notas = Nota.objects.count()
    percent_otimo = 0
    percent_bom = 0
    percent_ruim = 0

    if total_notas > 0:
        alunos_otimos = Nota.objects.filter(media__gte=8).count()
        alunos_bons = Nota.objects.filter(media__lt=8, media__gte=5).count()
        alunos_ruins = Nota.objects.filter(media__lt=5).count()
        percent_otimo = (alunos_otimos / total_notas) * 100
        percent_bom = (alunos_bons / total_notas) * 100
        percent_ruim = (alunos_ruins / total_notas) * 100

    stats_por_serie = {}
    series_distintas = Aluno.objects.values_list('serie', flat=True).distinct().order_by('serie')
    
    for serie in series_distintas:
        alunos_na_serie = Aluno.objects.filter(serie=serie)
        total_alunos_serie = alunos_na_serie.count()
        notas_na_serie = Nota.objects.filter(aluno__in=alunos_na_serie)
        total_notas_serie = notas_na_serie.count()

        if total_notas_serie > 0:
            alunos_otimos_serie = notas_na_serie.filter(media__gte=8).count()
            alunos_bons_serie = notas_na_serie.filter(media__lt=8, media__gte=5).count()
            alunos_ruins_serie = notas_na_serie.filter(media__lt=5).count()

            stats_por_serie[serie] = {
                'total_alunos': total_alunos_serie,
                'percent_otimo': (alunos_otimos_serie / total_notas_serie) * 100,
                'percent_bom': (alunos_bons_serie / total_notas_serie) * 100,
                'percent_ruim': (alunos_ruins_serie / total_notas_serie) * 100,
            }
        else:
            stats_por_serie[serie] = {
                'total_alunos': total_alunos_serie,
                'percent_otimo': 0,
                'percent_bom': 0,
                'percent_ruim': 0,
            }

    labels = ["Média ≥ 8", "Média 5 a 8", "Média < 5"]
    totals = [round(percent_otimo, 2), round(percent_bom, 2), round(percent_ruim, 2)]
    colors = ['#11998e', '#f7971e', '#e53935']
    detalhes = [
        [nota.aluno.nome for nota in Nota.objects.filter(media__gte=8).select_related('aluno')],
        [nota.aluno.nome for nota in Nota.objects.filter(media__lt=8, media__gte=5).select_related('aluno')],
        [nota.aluno.nome for nota in Nota.objects.filter(media__lt=5).select_related('aluno')],
    ]

    context = {
        'total_alunos': total_alunos,
        'percent_otimo': percent_otimo,
        'percent_bom': percent_bom,
        'percent_ruim': percent_ruim,
        'stats_por_serie': stats_por_serie,
        'labels': labels,
        'totals': totals,
        'colors': colors,
        'detalhes': detalhes,
    }
    return render(request, 'dashboard.html', context)