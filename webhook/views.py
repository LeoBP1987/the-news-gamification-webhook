from rest_framework import viewsets, filters, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from webhook.permissions import GroupPermissions
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from datetime import datetime
from webhook.models import Posts, Acessos, UTM
from webhook.serializers import PostsSerializers, AcessosSerializers, UTMSerializers, UserSerializers
from django_filters.rest_framework import DjangoFilterBackend
from webhook.utils import gerar_senha, custon_permission_denied

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet para gerenciar as operações relacionadas ao modelo Users.

    Este ViewSet permite criar, listar, atualizar e deletar
    instâncias do modelo Users. Os usuarios podem ser filtrados e ordenados
    com base em seu grupo ou username e também podem ser buscados pelos mesmos campos.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['grupo', 'username']
    search_fields = ['grupo', 'username']
    permission_classes = [IsAuthenticated, GroupPermissions]

    def permission_denied(self, request, message=None, code=None):
        return custon_permission_denied(message)    

class PostsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet para gerenciar as operações relacionadas ao modelo Posts.

    Este ViewSet permite criar, listar, atualizar e deletar
    instâncias do modelo Posts. Os posts podem ser filtrados e ordenados
    com base em seu ID.
    """
    queryset = Posts.objects.all().order_by('id')
    serializer_class = PostsSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['resource_id', ]
    permission_classes = [IsAuthenticated, GroupPermissions]

    def permission_denied(self, request, message=None, code=None):
        return custon_permission_denied(message)

class AcessosViewSet(viewsets.ModelViewSet):
    """
    A ViewSet para gerenciar as operações relacionadas ao modelo Acessos.

    Este ViewSet permite criar, listar, atualizar e deletar
    instâncias do modelo Acessos. Os acessos podem ser filtrados e ordenados
    com base em seu leitor, post ou acesso e também podem ser buscados pelos mesmo campos.
    """
    queryset = Acessos.objects.all().order_by('leitor')
    serializer_class = AcessosSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['leitor', 'post', 'abertura_dia']
    ordering_fields = ['leitor', 'post', 'abertura_dia']
    search_fields = ['leitor', 'post', 'abertura_dia']
    permission_classes = [IsAuthenticated, GroupPermissions]

    def permission_denied(self, request, message=None, code=None):
        return custon_permission_denied(message)
        
class AcessosPorPeriodoViewSet(generics.ListAPIView):
    """
    Este ViewSet permite listar as instâncias do modelo Acessos filtrados por um período de tempo entre datas enviadas como parâmetro. 
    Os Acessos podem ser filtrados e ordenados com base em seus leitores, posts e também podem ser buscados pelos mesmos campos.

    - **Parâmetros Esperados**:
        - `dataInicial`: String - (obrigatório) - Data Inicio do perído pelo qual os Acessos serão filtrados.
        - `dataFinal`: String - (obrigatório) - Data Final do período pelo qual os Acessos serão filtrados.

    - Para solicitar a lista de acessos por usuários:
      ```
      GET /acessos/DATAINICIAL/DATAFINAL/data/        
    """
    def get_queryset(self):

        data_inicial_str = str(self.kwargs['dataInicial'])
        data_final_str = str(self.kwargs['dataFinal'])

        data_inicial_formatada = datetime.strptime(data_inicial_str, "%Y-%m-%d").date()
        data_final_formatada = datetime.strptime(data_final_str, "%Y-%m-%d").date()

        if data_inicial_formatada > data_final_formatada:
            return Response(
                {"error": "A data final deve ser maior que a data inicial."},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = Acessos.objects.filter(abertura_dia__range=(data_inicial_formatada, data_final_formatada)).order_by('leitor')
        return queryset
    
    serializer_class = AcessosSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['leitor', 'post', 'acessos']
    search_fields = ['leitor', 'post', 'acessos']
    permission_classes = [IsAuthenticated, GroupPermissions]

    def permission_denied(self, request, message=None, code=None):
        return custon_permission_denied(message)

class UTMViewSet(viewsets.ModelViewSet):
    """
    A ViewSet para gerenciar as operações relacionadas ao modelo UTM.

    Este ViewSet permite criar, listar, atualizar e deletar
    instâncias do modelo UTM. Os posts podem ser filtrados e ordenados
    com base em seu ID.
    """
    queryset = UTM.objects.all().order_by('acesso')
    serializer_class = UTMSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['source', 'medium', 'campaign', 'channel']
    ordering_fields = ['source', 'medium', 'campaign', 'channel']
    search_fields = [ 'source', 'medium', 'campaign', 'channel']
    permission_classes = [IsAuthenticated, GroupPermissions]

    def permission_denied(self, request, message=None, code=None):
        return custon_permission_denied(message)

class WebhookViewSet(generics.ListAPIView):
    """
    Este viewset gerencia a webhook para registro de novos acesso ao The New.
    Ele bloqueio o uso dos métodos create, update, destroy e partial_update. Ele subscreve o metodo list para salvar as informações proveniente dos acessos.

    - **Método**: GET
    - **Parâmetros Esperados**:
        - `email`: String - (obrigatório) - E-mail do leitor.
        - `id`: Int - (obrigatório) - ID da edição correspondente ao post.
        - `utm_source`: String - (opcional) - Fonte da UTM.
        - `utm_medium`: String - (opcional) - Meio da UTM.
        - `utm_campaign`: String - (opcional) - Campanha da UTM.
        - `utm_channel`: String - (opcional) - Canal da UTM.
    
     **Exemplo de Uso da Ação `webhook`**:
    - Para registrar um acesso via webhook:
      ```
      GET /webhook/?email=user@example.com&id=post_123&utm_source=source&utm_medium=medium&utm_campaign=campaign&utm_channel=channel
    """
    queryset = Acessos.objects.all().order_by('leitor')
    serializer_class = AcessosSerializers
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        email = request.query_params.get('email')
        resource_id = request.query_params.get('id')
        utm_source = request.query_params.get('utm_source')
        utm_medium = request.query_params.get('utm_medium')
        utm_campaign = request.query_params.get('utm_campaign')
        utm_channel = request.query_params.get('utm_channel')

        if not email or not resource_id:
            return Response(
                {"error": "O email e id são obrigatórios para essa requisição."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            leitor, criado = User.objects.get_or_create(
                                            username=email, 
                                            defaults={'email': email},
                                            password=gerar_senha()
                                        )

            if(criado):
                grupo = Group.objects.get(name='leitores')
                leitor.groups.add(grupo)
            
            post, _ = Posts.objects.get_or_create(resource_id=resource_id)
            acesso = Acessos.objects.create(
                leitor=leitor,
                post=post,
                abertura_dia=datetime.today().date(),
                abertura_hora= datetime.now().time(),
                abertura_dia_semana=datetime.today().isoweekday()
            )

            if utm_source or utm_medium or utm_campaign or utm_channel:
                UTM.objects.create(
                    acesso=acesso,
                    source=utm_source,
                    medium=utm_medium,
                    campaign=utm_campaign,
                    channel=utm_channel
                )
            return Response(
                {"message": "Dados salvos com sucesso."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    