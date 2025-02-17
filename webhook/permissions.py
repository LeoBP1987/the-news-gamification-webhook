from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.urls import resolve

class GroupPermissions(BasePermission):
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        url_acessada = resolve(request.path)
        modelo_acessado = url_acessada.url_name.split('-')[0].lower()

        mapa_metodo_permissao = {
            'GET': f'view_{modelo_acessado}',
            'POST': f'add_{modelo_acessado}',
            'PUT': f'change{modelo_acessado}',
            'PATCH': f'change{modelo_acessado}',
            'DELETE': f'delete{modelo_acessado}',
        }

        permissao_necessaria = mapa_metodo_permissao.get(request.method)

        if not permissao_necessaria:
            raise PermissionDenied(f'A ação {request.method} não foi reconhecida.')

        if not request.user.groups.filter(permissions__codename=permissao_necessaria).exists():
            raise PermissionDenied("Essa ação não é permitida para esse usuário.")
        
        return True