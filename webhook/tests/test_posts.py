from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webhook.models import Posts
from webhook.serializers import PostsSerializers

class PostsTestCase(APITestCase):
    '''
        Classe para testar os métodos do viewset PostsViewset.

        - Métodos permitidos:
            GET, POST e DELETE

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):

        self.usuario = User.objects.get(username='admin')
        self.url = reverse('Posts-list')
        self.client.force_authenticate(self.usuario)

        self.post_1 = Posts.objects.get(pk=1123)
        self.post_2 = Posts.objects.get(pk=2202)

    def test_verifica_requisicao_get_lista_posts(self):
        'Teste que verifica requisição GET para listar Posts'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_um_post(self):
        'Teste que verifica requisição GET para um post'
        
        response = self.client.get(f'{self.url}{self.post_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_criatura = self.post_1
        dados_serializados = PostsSerializers(dados_criatura).data

        self.assertEqual(response.data['id'], dados_serializados['id'])

    def test_verifica_requisicao_post_um_post(self):
        'Teste que verifica requisição POST para um post'

        dados = {
            "id": 3030,
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_um_post(self):
        '''Teste que verifica requisição DELETE para um post'''

        response = self.client.delete(f'{self.url}{self.post_2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)