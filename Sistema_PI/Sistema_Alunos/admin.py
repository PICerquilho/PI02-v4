from django.contrib import admin

from .models import Aluno  # Importe o modelo que você quer exibir no admin

# Registro do modelo Aluno no Django Admin
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id_aluno', 'nome', 'nome_social', 'rg', 'cpf', 'serie', 'periodo')  # Campos a serem exibidos na lista
    search_fields = ('nome', 'nome_social', 'id_aluno', 'rg', 'cpf')  # Campos que você pode pesquisar no admin
    list_filter = ('serie', 'periodo')  # Campos para filtro rápido na interface
    ordering = ('nome',)  # Ordenação padrão na listagem