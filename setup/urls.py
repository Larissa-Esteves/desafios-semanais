from django.contrib import admin
from django.urls import path, include

#####
# Adicione as rotas sempre na aplicação e NÂO aqui
#
# Inclua somente as rotas da aplicação
#####

# admin -> nome da rota
# admin.site.urls -> função para renderizar a rota
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('desafios.urls')),
]
