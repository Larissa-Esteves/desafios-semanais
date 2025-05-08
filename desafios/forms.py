from django import forms
from .models import Horario

DIAS_DA_SEMANA = [
    ('SEG', 'Segunda-feira'),
    ('TER', 'Terça-feira'),
    ('QUA', 'Quarta-feira'),
    ('QUI', 'Quinta-feira'),
    ('SEX', 'Sexta-feira'),
    ('SAB', 'Sábado'),
    ('DOM', 'Domingo'),
]

class HorarioForm(forms.ModelForm):
    repetir = forms.BooleanField(required=False, label='Deseja repetir em outros dias?')
    dias_repetir = forms.MultipleChoiceField(
        required=False,
        choices=DIAS_DA_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label='Selecionar dias adicionais'
    )

    class Meta:
        model = Horario
        fields = ['dia', 'hora_inicio', 'descricao']

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao', '').strip()
        if not descricao:
            raise forms.ValidationError('A descrição não pode estar em branco.')
        return descricao

    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get("dia")
        hora = cleaned_data.get("hora_inicio")

        instance = getattr(self, 'instance', None)
        if instance and Horario.objects.filter(dia=dia, hora_inicio=hora).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("Já existe um cadastro para esse dia e horário.")

        return cleaned_data
