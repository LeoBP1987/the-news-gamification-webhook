from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webhook.models import UTM, Acessos
from webhook.serializers import UTMSerializers
from datetime import datetime

class AcessosTestCase(APITestCase):
    '''
        Classe para testar os métodos do viewset UTMViewset.

        - Métodos permitidos:
            GET, POST, PUT e DELETE

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):

        self.usuario = User.objects.get(username='admin')
        self.url = reverse('UTMs-list')
        self.client.force_authenticate(self.usuario)

        self.acesso_1 = Acessos.objects.get(pk=5)
        
        self.utm_1 = UTM.objects.get(pk=3)
        self.utm_2 = UTM.objects.get(pk=6)

    def test_verifica_requisicao_get_lista_utm(self):
        'Teste que verifica requisição GET para listar UTMs'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_um_utm(self):
        'Teste que verifica requisição GET para um utm'
        
        response = self.client.get(f'{self.url}{self.utm_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_criatura = self.utm_1
        dados_serializados = UTMSerializers(dados_criatura).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['acesso'], dados_serializados['acesso'])
        self.assertEqual(response.data['source'], dados_serializados['source'])
        self.assertEqual(response.data['medium'], dados_serializados['medium'])
        self.assertEqual(response.data['campaign'], dados_serializados['campaign'])
        self.assertEqual(response.data['channel'], dados_serializados['channel'])

    def test_verifica_requisicao_post_um_utm(self):
        'Teste que verifica requisição POST para um utm'

        dados = {
            "acesso": self.acesso_1.id,
            "source": "tiktok",
            "medium": "socialpaid",
            "campaign": "12/12/2024",
            "channel": "web"
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_um_utm(self):
        '''Teste que verifica requisição DELETE para um utm'''

        response = self.client.delete(f'{self.url}{self.utm_2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_um_utm(self):
        '''Teste que verifica requisição PUT para um utm'''

        dados = {
            "acesso": self.acesso_1.id,
            "source": "instagran",
            "medium": "socialpaid",
            "campaign": "15/02/2025",
            "channel": "web"
        }

        response = self.client.put(f'{self.url}{self.utm_1.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)