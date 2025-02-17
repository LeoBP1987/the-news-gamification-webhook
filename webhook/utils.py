from rest_framework import status
from rest_framework.response import Response
import string
import secrets


def custon_permission_denied(message=None):
        return Response(
            {"error": message or "Ação não permitida para esse usuário."},
            status=status.HTTP_403_FORBIDDEN
        )

def gerar_senha(tamanho=10):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        senha = ''.join(secrets.choice(caracteres) for _ in range(10))
        return senha