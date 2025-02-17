from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webhook.models import Acessos, Posts
from webhook.serializers import AcessosSerializers
from datetime import datetime

class AcessosTestCase(APITestCase):
    '''
        Classe para testar os métodos do viewset AcessosViewset.

        - Métodos permitidos:
            GET, POST, PUT e DELETE

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):

        self.usuario = User.objects.get(username='admin')
        self.url = reverse('Acessos-list')
        self.client.force_authenticate(self.usuario)

        self.usuario_1 = User.objects.get(pk=9)
        self.post_1 = Posts.objects.get(pk=1123)

        self.acesso_1 = Acessos.objects.get(pk=5)
        self.acesso_2 = Acessos.objects.get(pk=7)

    def test_verifica_requisicao_get_lista_acessos(self):
        'Teste que verifica requisição GET para listar Acessos'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_um_acesso(self):
        'Teste que verifica requisição GET para um acesso'
        
        response = self.client.get(f'{self.url}{self.acesso_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_criatura = self.acesso_1
        dados_serializados = AcessosSerializers(dados_criatura).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['leitor'], dados_serializados['leitor'])
        self.assertEqual(response.data['post'], dados_serializados['post'])
        self.assertEqual(response.data['abertura_dia'], dados_serializados['abertura_dia'])
        self.assertEqual(response.data['abertura_hora'], dados_serializados['abertura_hora'])
        self.assertEqual(response.data['abertura_dia_semana'], dados_serializados['abertura_dia_semana'])

    def test_verifica_requisicao_post_um_acesso(self):
        'Teste que verifica requisição POST para um acesso'

        dados = {
            "leitor": self.usuario_1.id,
            "post": self.post_1.id,
            "abertura_dia": datetime.today().date(),
            "abertura_hora": datetime.now().time(),
            "abertura_dia_semana": datetime.today().isoweekday()
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_um_acesso(self):
        '''Teste que verifica requisição DELETE para um acesso'''

        response = self.client.delete(f'{self.url}{self.acesso_2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_um_acesso(self):
        '''Teste que verifica requisição PUT para um acesso'''

        dados = {
            "leitor": self.usuario_1.id,
            "post": self.post_1.id,
            "abertura_dia": datetime.today().date(),
            "abertura_hora": datetime.now().time(),
            "abertura_dia_semana": 5
        }

        response = self.client.put(f'{self.url}{self.acesso_1.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)