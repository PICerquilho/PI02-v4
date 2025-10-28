from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Aluno
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_social': forms.TextInput(attrs={'class': 'form-control'}),
            'id_aluno': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_emergencial': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'serie': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'deficiencia': forms.Select(attrs={'class': 'form-control'}),
            'deficiencia_qual': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['foto'].required = True

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        nome_social = cleaned_data.get('nome_social')

        if nome and not nome_social:
            cleaned_data['nome_social'] = nome

        if cleaned_data.get('deficiencia') == 'S' and not cleaned_data.get('deficiencia_qual'):
            cleaned_data['deficiencia_qual'] = 'Não Informado'

        return cleaned_data
