from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from webhook.serializers import UserSerializers
from webhook.utils import gerar_senha

class UserTestCase(APITestCase):
    '''
        Classe para testar os métodos do viewset UserViewSet.

        - Métodos permitidos:
            GET, POST, PUT e DELETE

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):

        self.usuario = User.objects.get(username='admin')
        self.url = reverse('Users-list')
        self.client.force_authenticate(self.usuario)

        self.usuario_1 = User.objects.get(pk=8)
        self.usuario_2 = User.objects.get(pk=9)

        self.password = gerar_senha()

    def test_verifica_requisicao_get_lista_usuarios(self):
        'Teste que verifica requisição GET para listar Usuarios'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_um_usuario(self):
        'Teste que verifica requisição GET para um usuario'

        response = self.client.get(f'{self.url}{self.usuario_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_criatura = self.usuario_1
        dados_serializados = UserSerializers(dados_criatura).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['username'], dados_serializados['username'])
        self.assertEqual(response.data['email'], dados_serializados['email'])
        self.assertEqual(response.data['grupo'], dados_serializados['grupo'])

    def test_verifica_requisicao_post_um_usuario(self):
        'Teste que verifica requisição POST para um usuario'

        dados = {
            "username": "teste@email.com",
            "password": self.password,
            "email": "email@email.com",
            "grupo": "leitores"
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_um_usuario(self):
        '''Teste que verifica requisição DELETE para um usuario'''

        response = self.client.delete(f'{self.url}{self.usuario_2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_um_usuario(self):
        '''Teste que verifica requisição PUT para um usuario'''

        dados = {
            "username": "email@email.com",
            "password": "TESTEALTERASENHA",
            "email": "email@email.com",
            "grupo": "leitores"
        }

        response = self.client.put(f'{self.url}{self.usuario_1.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)