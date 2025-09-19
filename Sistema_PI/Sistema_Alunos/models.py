from django.db import models
from PIL import Image
import os
from django.core.validators import MinValueValidator, MaxValueValidator

class Aluno(models.Model):
    # Definir opções pré-definidas para os campos existentes
    SERIES_CHOICES = [
        ('1ª Ano', '1ª Ano'),
        ('2ª Ano', '2ª Ano'),
        ('3ª Ano', '3ª Ano'),
        ('4ª Ano', '4ª Ano'),
        ('5ª Ano', '5ª Ano'),
        ('6ª Ano', '6ª Ano'),
        ('7ª Ano', '7ª Ano'),
        ('8ª Ano', '8ª Ano'),
        ('9ª Ano', '9ª Ano'),
    ]
    
    TURMA_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    PERIODO_CHOICES = [
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
    ]
    
    # NOVAS OPÇÕES para a coleta ética de dados
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('NI', 'Prefiro não informar'),
    ]
    
    DEFICIENCIA_CHOICES = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]

    foto = models.ImageField(upload_to='fotos/', default='fotos/default.jpg', blank=False)
    id_aluno = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True)
    rg = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField(blank=True, null=True)
    contato = models.CharField(max_length=15, blank=True, null=True)
    contato_emergencial = models.CharField(max_length=15, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    
    # NOVOS CAMPOS adicionados
    sexo = models.CharField(max_length=2, choices=SEXO_CHOICES, default='NI')
    deficiencia = models.CharField(max_length=1, choices=DEFICIENCIA_CHOICES, default='N')
    deficiencia_qual = models.CharField(max_length=255, blank=True, null=True)
    
    # Campos existentes
    serie = models.CharField(max_length=10, choices=SERIES_CHOICES)
    turma = models.CharField(max_length=1, choices=TURMA_CHOICES)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES)
    observacoes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome} - {self.serie} {self.turma} ({self.periodo})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            foto_path = self.foto.path
            if os.path.exists(foto_path):
                try:
                    with Image.open(foto_path) as img:
                        if img.size != (512, 512):
                            img = img.convert('RGB')
                            img = img.resize((512, 512))
                            img.save(foto_path)
                except Exception as e:
                    print(f"Erro ao redimensionar imagem: {e}")