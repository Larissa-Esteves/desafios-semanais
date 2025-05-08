from django.urls import path
from .views import index, cadastrar_horario, excluir_descricao, editar_horario, atualizar_descricao, excluir_horario
from . import views
from .views import lista_para_edicao

urlpatterns = [
    path("", index, name="index"),
    path('cadastrar/', cadastrar_horario, name='cadastrar_horario'),
    path('excluir/', views.lista_para_exclusao, name='lista_para_exclusao'),
    path('alterar/', views.lista_para_edicao, name='lista_para_edicao'),
    #path('excluir_descricao/<int:horario_id>/', views.excluir_descricao, name='excluir_descricao'),
    path('editar/<int:horario_id>/', views.editar_horario, name='editar_horario'),
    path('atualizar_descricao/<int:horario_id>/', views.atualizar_descricao, name='atualizar_descricao'),
    path('excluir/<int:horario_id>/', views.excluir_horario, name='excluir_horario'),
    path('listar/', views.listar_horarios, name='listar_horarios'),
    path('alterar/', views.lista_para_edicao, name='lista_para_edicao'),# USO
]