from django.test import TestCase
from webhook.models import Posts, Acessos, UTM
from django.contrib.auth.models import User, Group
from datetime import datetime
from webhook.views import gerar_senha

class ModelUserTestCase(TestCase):
    '''
        Classe para teste do modelo User.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    def setUp(self):
        self.password = gerar_senha()
        self.usuario = User.objects.create(
            username = 'email@email.com',
            email = 'email@email.com',
            password = self.password
        )

    def test_verifica_atributo_modelo_user(self):
        'Teste que verifica os atributos do modelo User'

        self.assertEqual(self.usuario.username, 'email@email.com')
        self.assertEqual(self.usuario.email, 'email@email.com')
        self.assertEqual(self.usuario.password, self.password)

class ModelPostsTestCase(TestCase):
    '''
        Classe para teste do modelo Posts.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    def setUp(self):
        self.posts = Posts.objects.create(
            id = 1010
        )

    def test_verifica_atributo_modelo_posts(self):
        'Teste que verifica os atributos do modelo Posts'

        self.assertEqual(self.posts.id, 1010)

class ModelAcessosTestCase(TestCase):
    '''
        Classe para teste do modelo Acessos.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    def setUp(self):
        self.password = gerar_senha()
        self.usuario = User.objects.create(
            username = 'email@email.com',
            email = 'email@email.com',
            password = self.password
        )

        self.posts = Posts.objects.create(
            id = 1010
        )
        
        self.abertura = datetime.today()

        self.acessos = Acessos.objects.create(
            leitor = self.usuario,
            post = self.posts,
            abertura_dia = self.abertura.date(),
            abertura_hora = self.abertura.time(),
            abertura_dia_semana = self.abertura.isoweekday()
        )

    def test_verifica_atributo_modelo_acessos(self):
        'Teste que verifica os atributos do modelo Acessos'

        self.assertEqual(self.acessos.leitor.username, self.usuario.username)
        self.assertEqual(self.acessos.post.id, self.posts.id)
        self.assertEqual(self.acessos.abertura_dia, self.abertura.date())
        self.assertEqual(self.acessos.abertura_hora, self.abertura.time())
        self.assertEqual(self.acessos.abertura_dia_semana, self.abertura.isoweekday())

class ModelUTMTestCase(TestCase):
    '''
        Classe para teste do modelo UTM.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    def setUp(self):
        self.password = gerar_senha()
        self.usuario = User.objects.create(
            username = 'email@email.com',
            email = 'email@email.com',
            password = self.password
        )

        self.posts = Posts.objects.create(
            id = 1010
        )
        
        self.abertura = datetime.today()

        self.acessos = Acessos.objects.create(
            leitor = self.usuario,
            post = self.posts,
            abertura_dia = self.abertura.date(),
            abertura_hora = self.abertura.time(),
            abertura_dia_semana = self.abertura.isoweekday()
        )

        self.UTM = UTM.objects.create(
            acesso = self.acessos,
            source = 'tiktok',
            medium = 'socialpaid',
            campaign = '12/12/2024',
            channel = 'web'
        )

    def test_verifica_atributo_modelo_utm(self):
        'Teste que verifica os atributos do modelo UTM'

        self.assertEqual(self.UTM.acesso.id, self.acessos.id)
        self.assertEqual(self.UTM.source, 'tiktok')
        self.assertEqual(self.UTM.medium, 'socialpaid')
        self.assertEqual(self.UTM.campaign, '12/12/2024')
        self.assertEqual(self.UTM.channel, 'web')