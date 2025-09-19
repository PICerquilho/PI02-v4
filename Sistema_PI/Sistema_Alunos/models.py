from django.db import models
from PIL import Image
import os
from django.core.validators import MinValueValidator, MaxValueValidator

class Aluno(models.Model):
    # Definir opções predefinidas
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
    

    # Agora os campos abaixo têm valores pré-definidos
    serie = models.CharField(max_length=10, choices=SERIES_CHOICES)
    turma = models.CharField(max_length=1, choices=TURMA_CHOICES)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES)

    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.serie} {self.turma} ({self.periodo})"
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        fotoorigi = Image.open(self.foto.path)
        print(f"Tamanho original: {fotoorigi.width}x{fotoorigi.height}")
        if self.foto:
            foto_path = self.foto.path

            if os.path.exists(foto_path):
                try:
                    with Image.open(foto_path) as img:
                        if img.size != (512, 512):
                            img = img.convert('RGB')
                            img = img.resize((512, 512))
                            img.save(foto_path)
                        print(f"Tamanho alterado: {img.width}x{img.height}")

                except Exception as e:
                    print(f"Erro ao redimensionar imagem: {e}")
    
    def __str__(self):
        return f"{self.nome} - {self.serie} {self.turma} ({self.periodo})"

# Adicione esta classe para o modelo de notas
class Nota(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name="notas")
    bimestre1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    bimestre2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    bimestre3 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    bimestre4 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    media = models.FloatField(null=True, blank=True)

    def calcular_media(self):
        notas = [n for n in [self.bimestre1, self.bimestre2, self.bimestre3, self.bimestre4] if n is not None]
        if notas:
            self.media = sum(notas) / len(notas)
        else:
            self.media = None
        return self.media

    def save(self, *args, **kwargs):
        self.calcular_media()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notas de {self.aluno.nome}"