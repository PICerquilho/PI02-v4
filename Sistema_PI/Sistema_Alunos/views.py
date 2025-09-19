from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlunoForm
from .models import Aluno
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date

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

# AQUI ESTÁ A VIEW DO DASHBOARD MODIFICADA
@login_required(login_url='login')
def dashboard(request):
    total_alunos = Aluno.objects.count()
    
    # NOVAS ESTATÍSTICAS
    alunos_masculino = Aluno.objects.filter(sexo='M').count()
    alunos_feminino = Aluno.objects.filter(sexo='F').count()
    alunos_nao_informado = Aluno.objects.filter(sexo='NI').count()
    alunos_com_deficiencia = Aluno.objects.filter(deficiencia='S').count()
    
    # NOVAS ESTATÍSTICAS: FAIXA ETÁRIA
    hoje = date.today()
    alunos_ate_7 = 0
    alunos_8_a_10 = 0
    alunos_11_a_13 = 0
    alunos_14_acima = 0
    
    for aluno in Aluno.objects.all():
        if aluno.data_nascimento:
            idade = hoje.year - aluno.data_nascimento.year - ((hoje.month, hoje.day) < (aluno.data_nascimento.month, aluno.data_nascimento.day))
            if idade <= 7:
                alunos_ate_7 += 1
            elif 8 <= idade <= 10:
                alunos_8_a_10 += 1
            elif 11 <= idade <= 13:
                alunos_11_a_13 += 1
            elif idade >= 14:
                alunos_14_acima += 1
    
    # O dashboard agora terá um novo contexto
    context = {
        'total_alunos': total_alunos,
        'alunos_masculino': alunos_masculino,
        'alunos_feminino': alunos_feminino,
        'alunos_nao_informado': alunos_nao_informado,
        'alunos_com_deficiencia': alunos_com_deficiencia,
        'alunos_ate_7': alunos_ate_7,
        'alunos_8_a_10': alunos_8_a_10,
        'alunos_11_a_13': alunos_11_a_13,
        'alunos_14_acima': alunos_14_acima,
    }
    return render(request, 'dashboard.html', context)