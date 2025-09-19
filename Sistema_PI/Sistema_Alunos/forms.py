from django import forms
from .models import Aluno
from .models import Nota

class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Aluno
        fields = '__all__'  # Isto garante que todos os campos, incluindo o 'endereco', sejam exibidos no formulário.
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
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['foto'].required = True


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['bimestre1', 'bimestre2', 'bimestre3', 'bimestre4']
        widgets = {
            'bimestre1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0, 'max': 10}),
            'bimestre2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0, 'max': 10}),
            'bimestre3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0, 'max': 10}),
            'bimestre4': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0, 'max': 10}),
        }