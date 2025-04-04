from rest_framework import status
from rest_framework.response import Response
from webhook.models import Acessos
from datetime import datetime
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

def obter_horario_postagem(request):
    postar = True
    dia_postagem = datetime.today().date()
    dia_semana_postagem = datetime.today().isoweekday()
    hora_postagem = datetime.now().time().replace(microsecond=0)

    ultima_postagem = Acessos.objects.all().last()

    if ultima_postagem is not None:
        if (ultima_postagem.leitor.email == request.query_params.get('email') and 
            ultima_postagem.post.resource_id == request.query_params.get('id')):
                ultima_hora = datetime.combine(dia_postagem, ultima_postagem.abertura_hora)
                data_postagem = datetime.combine(dia_postagem, hora_postagem)
                diferenca = (data_postagem - ultima_hora).total_seconds()
                if diferenca < 30:
                        postar = False

    return {'postar': postar, 'dia': dia_postagem, 'dia_semana': dia_semana_postagem, 'hora': hora_postagem}