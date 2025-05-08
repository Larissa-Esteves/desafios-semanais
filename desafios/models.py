from django.db import models

# Opções de dias da semana
DIAS_DA_SEMANA = [
    ('SEG', 'Segunda-feira'),
    ('TER', 'Terça-feira'),
    ('QUA', 'Quarta-feira'),
    ('QUI', 'Quinta-feira'),
    ('SEX', 'Sexta-feira'),
    ('SAB', 'Sábado'),
    ('DOM', 'Domingo'),
]

# Lista de horários no formato '07h', '08h', etc.
HORARIO = [
    (f"{h:02}h", f"{h:02}h") for h in range(7, 24)
] + [('00h', '00h')]  # Para adicionar a opção '00h'

class Horario(models.Model):
    dia = models.CharField(max_length=3, choices=DIAS_DA_SEMANA, verbose_name="Dia da Semana")
    hora_inicio = models.CharField(max_length=5, choices=HORARIO, verbose_name="Horário Inicial")  # Usar CharField para armazenar horários como string
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return f'{self.hora_inicio}'
