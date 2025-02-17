from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webhook.models import Acessos, Posts, UTM

class WebhookViewSetTestCase(APITestCase):
    '''
        Classe para testar o webhook.

        - Métodos permitidos:
            GET

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):
        
        self.usuario = User.objects.get(username='admin')
        self.url = reverse('Webhook')
        self.client.force_authenticate(self.usuario)

        self.email = 'novo2_usuario@example.com'
        self.resource_id = 'post_2025-02-17'
        self.source = 'tiktok'
        self.medium = 'socialpaid'
        self.campaign = '12/12/2024'
        self.channel = 'web'

    def test_verifica_requisicao_get_webhook_sucesso(self):
        'Teste que verifica uma requisição GET bem sucessidida ao Webhook '

        response = self.client.get(f'{self.url}?email={self.email}&id={self.resource_id}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        usuario = User.objects.filter(username=self.email).first()
        post = Posts.objects.filter(resource_id=self.resource_id).first()
        acesso = Acessos.objects.filter(leitor=usuario, post=post).first()

        self.assertEqual(self.email, usuario.username)
        self.assertEqual(self.resource_id, post.resource_id)
        self.assertEqual(acesso.leitor.email, self.email)
        self.assertEqual(acesso.post.resource_id, self.resource_id)
        self.assertEqual(response.data, {"message": "Dados salvos com sucesso."})

    def test_verifica_requisicao_get_webhook_sem_email(self):
        'Teste que verifica uma requisição GET ao Webhook sem email'

        response = self.client.get(f'{self.url}?id={self.resource_id}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "O email e id são obrigatórios para essa requisição."})

    def test_verifica_requisicao_get_webhook_sem_post(self):
        'Teste que verifica uma requisição GET ao Webhook sem post'

        response = self.client.get(f'{self.url}?email={self.email}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "O email e id são obrigatórios para essa requisição."})

    def test_verifica_requisicao_get_webhook_com_utms(self):
        'Teste que verifica uma requisição GET ao Webhook com as utms'

        response = self.client.get(f'{self.url}?email={self.email}&id={self.resource_id}&utm_source={self.source}&utm_medium={self.medium}&utm_campaign={self.campaign}&utm_channel={self.channel}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        acesso = Acessos.objects.filter(leitor__username=self.email, post__resource_id=self.resource_id).first()
        utm = UTM.objects.filter(acesso=acesso).first()

        self.assertEqual(utm.source, self.source)
        self.assertEqual(utm.medium, self.medium)
        self.assertEqual(utm.campaign, self.campaign)
        self.assertEqual(utm.channel, self.channel)