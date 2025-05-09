from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Horario
from .forms import HorarioForm
from django.contrib import messages
from django.contrib.messages import get_messages
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Função para exibir a página principal com a tabela dia e horário
def index(request):
    dias_da_semana = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    horarios = [
        '07h', '08h', '09h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '00h'
    ]
    # busca todos os objetos
    horarios_cadastrados = Horario.objects.all()
    # Cria um dicionário de contexto pra passar dados para ao template
    context = {
        'dias_da_semana': dias_da_semana,
        'dias': [dia[0].lower() for dia in dias_da_semana], # Lista abreviada em minúsculo para facilitar a comparação
        'horarios': horarios,
        'horarios_cadastrados': horarios_cadastrados,
    }
    
    return render(request, 'desafios/index.html', context)

# cadastrar uma nova entrada no horário e dia cadastrado no banco
def cadastrar_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save()  # salva o horário original

            # Se o usuário escolheu repetir o horário em outros dias
            if form.cleaned_data.get('repetir'):
                dias_repetir = form.cleaned_data.get('dias_repetir', [])
                for dia in dias_repetir:
                    # Evita cadastrar duplicatas
                    if not Horario.objects.filter(dia=dia, hora_inicio=horario.hora_inicio).exists():
                        Horario.objects.create(
                            dia=dia,
                            hora_inicio=horario.hora_inicio,
                            descricao=horario.descricao
                        )

            messages.success(request, 'Horário cadastrado com sucesso!')
            return redirect('index')
    else:
        # Limpa mensagens pendentes
        storage = messages.get_messages(request)
        for msg in storage:
            pass
        form = HorarioForm()

    return render(request, 'form_horario.html', {'form': form})

# Excluir uma descrição de um horário específico
def excluir_descricao(request, horario_id):
    if request.method == 'POST':
        # Obtém o obj Horário com o id fornecido ou retorna ero 404
        horario = get_object_or_404(Horario, id=horario_id)

        # Define o campo 'descricao' do objeto Horario como None.
        horario.descricao = None  
        horario.save()

        return redirect('index')  
    else:
        return redirect('index')

# Listar os horarios para exclusão
def listar_horarios(request):
    horarios = Horario.objects.all().order_by('dia', 'hora_inicio')
    return render(request, 'desafios/listar_horarios.html', {'horarios': horarios})

# Função para exibir o formulário de edição de um horário específico.
def editar_horario(request, horario_id):
    # Obtém o objeto Horario com o ID fornecido ou retorna um erro 404 se não encontrado.
    horario = get_object_or_404(Horario, id=horario_id)

    # Cria uma instância do formulário HorarioForm preenchida com os dados do horário existente.
    form = HorarioForm(instance=horario)

    # Cria um dicionário de contexto com o formulário e o ID do horário.
    context = {
        'form': form,
        'horario_id': horario_id,
    }
    
    return render(request, 'desafios/editar_horario.html', context)

# Atualiza um horário que existe no Banco
def atualizar_descricao(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)

    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            descricao = form.cleaned_data.get('descricao', '').strip()
            if descricao:  # Garante que não está vazio ou só espaços
                horario.descricao = descricao
                horario.save(update_fields=['descricao'])
                messages.success(request, 'Descrição atualizada com sucesso!')
                return redirect('index')
            else:
                messages.warning(request, 'A descrição não pode estar em branco.')
        else:
            messages.error(request, 'Erro ao atualizar a descrição. Verifique os dados.')

        context = {
            'form': form,
            'horario_id': horario_id,
        }
        return render(request, 'index.html', context)

    else:
        form = HorarioForm(instance=horario)
        context = {
            'form': form,
            'horario_id': horario_id,
        }
        return render(request, 'desafios/editar_horario.html', context)


def excluir_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    if request.method == 'POST':
        horario.delete()
        messages.success(request, f'O horário com ID {horario_id} foi excluído com sucesso!')
        return redirect('index')
    else:
        messages.warning(request, f'Acesso inválido para excluir o horário com ID {horario_id}. Use o formulário de exclusão.')
        return redirect('index')
    
def lista_para_exclusao(request):
    # Mapeamento de códigos dos dias para nomes completos
    dias_da_semana = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    codigo_para_nome = dict(dias_da_semana)

    if request.method == 'POST':
        ids_para_excluir = request.POST.getlist('horarios')
        Horario.objects.filter(id__in=ids_para_excluir).delete()
        messages.success(request, 'Descrição excluída com sucesso.')
        return redirect('index')

    # Após possível exclusão, carrega novamente os dados atualizados
    horarios_queryset = Horario.objects.all().order_by('hora_inicio')

    horarios_por_dia = defaultdict(list)
    for h in horarios_queryset:
        nome_dia = codigo_para_nome.get(h.dia.upper())
        if nome_dia:
            horarios_por_dia[nome_dia].append(h)

    ordem_dias = [nome for _, nome in dias_da_semana]
    dias_ordenados = [(dia, horarios_por_dia[dia]) for dia in ordem_dias if dia in horarios_por_dia]

    return render(request, 'exclusao_horarios.html', {
        'horarios_por_dia': dias_ordenados
    })

# Vai para a página "index" se tiver tudo certo
def lista_para_edicao(request):
    dias_da_semana = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    codigo_para_nome = dict(dias_da_semana)

    horarios_queryset = Horario.objects.all().order_by('hora_inicio')

    # Agrupando os horários por dia (nome completo)
    horarios_por_dia = defaultdict(list)
    for h in horarios_queryset:
        nome_dia = codigo_para_nome.get(h.dia.upper())
        if nome_dia:
            horarios_por_dia[nome_dia].append(h)

    ordem_dias = [nome for _, nome in dias_da_semana]
    dias_ordenados = [(dia, horarios_por_dia[dia]) for dia in ordem_dias if dia in horarios_por_dia]

    campos_com_erro = []

    if request.method == 'POST':
        erro = False

        # Obtem apenas o horário que foi alterado
        horario_id = request.POST.get('horario_id')
        descricao = request.POST.get('descricao', '').strip()

        if horario_id:
            try:
                horario = Horario.objects.get(id=horario_id)

                if not descricao:
                    erro = True
                    campos_com_erro.append(horario.id)
                    messages.error(request, f'A descrição para o horário das {horario.hora_inicio} está em branco.')
                else:
                    horario.descricao = descricao
                    horario.save()
                    messages.success(request, f'Descrição do horário {horario.hora_inicio} atualizada com sucesso!')

            except Horario.DoesNotExist:
                messages.error(request, 'Horário não encontrado.')
                erro = True

        if erro:
            return render(request, 'desafios/editar_horario.html', {
                'horarios_por_dia': dias_ordenados,
                'campos_com_erro': campos_com_erro
            })

        return redirect('index')  # Recarrega a própria página

    return render(request, 'desafios/editar_horario.html', {
        'horarios_por_dia': dias_ordenados,
        'campos_com_erro': []
    })