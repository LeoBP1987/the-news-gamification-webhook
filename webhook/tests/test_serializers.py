from django.test import TestCase
from webhook.models import Posts, Acessos, UTM
from django.contrib.auth.models import User
from webhook.serializers import UserSerializers, PostsSerializers, AcessosSerializers, UTMSerializers

class SerializersUserTestCase(TestCase):
    '''
        Classe para teste do serializer User.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):
        self.usuario = User.objects.get(pk=9)
        self.usuario.serializer = UserSerializers(instance=self.usuario)

    def test_verifica_campos_serializados_de_user(self):
        'Teste que verifica os campos serializados do modelo User'

        dados = self.usuario.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'username', 'email', 'grupo']))

    def test_verifica_conteudos_serializados_de_user(self):
        'Teste que verifica o conteudo dos campos serializados do modelo User'

        dados = self.usuario.serializer.data

        self.assertEqual(dados['id'], self.usuario.id)    
        self.assertEqual(dados['username'], self.usuario.username)
        self.assertEqual(dados['email'], self.usuario.email)
        self.assertEqual(dados['grupo'], self.usuario.groups.all()[0].name)

class SerializersPostsTestCase(TestCase):
    '''
        Classe para teste do serializer Posts.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):
        self.post = Posts.objects.get(pk=1123)
        self.post.serializer = PostsSerializers(instance=self.post)

    def test_verifica_campos_serializados_de_posts(self):
        'Teste que verifica os campos serializados do modelo Posts'

        dados = self.post.serializer.data

        self.assertEqual(set(dados.keys()), set(['id',]))

    def test_verifica_conteudos_serializados_de_posts(self):
        'Teste que verifica o conteudo dos campos serializados do modelo Posts'

        dados = self.post.serializer.data

        self.assertEqual(dados['id'], self.post.id)

class SerializersAcessosTestCase(TestCase):
    '''
        Classe para teste do serializer Acessos.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):
        self.usuario = User.objects.get(pk=9)
        self.post = Posts.objects.get(pk=1123)
        
        self.acesso = Acessos.objects.get(pk=7)
        self.acesso.serializer = AcessosSerializers(self.acesso)

    def test_verifica_campos_serializados_de_acessos(self):
        'Teste que verifica os campos serializados do modelo Acessos'

        dados = self.acesso.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'leitor', 'post', 'abertura_dia', 'abertura_hora', 'abertura_dia_semana']))

    def test_verifica_conteudos_serializados_de_acessos(self):
        'Teste que verifica o conteudo dos campos serializados do modelo Acessos'

        dados = self.acesso.serializer.data

        self.assertEqual(dados['id'], self.acesso.id)
        self.assertEqual(dados['leitor'], self.acesso.leitor.id)
        self.assertEqual(dados['post'], self.acesso.post.id)
        self.assertEqual(dados['abertura_dia'], str(self.acesso.abertura_dia))
        self.assertEqual(dados['abertura_hora'], str(self.acesso.abertura_hora))
        self.assertEqual(dados['abertura_dia_semana'], self.acesso.abertura_dia_semana)

class SerializersUTMTestCase(TestCase):
    '''
        Classe para teste do serializer UTM.

        - Para rodar os testes usar:
      ```
      python manage.py test --settings=the_news.settings_test
    '''
    fixtures = ['dados_dumped.json']

    def setUp(self):
        self.usuario = User.objects.get(pk=9)
        self.post = Posts.objects.get(pk=1123)
        self.acesso = Acessos.objects.get(pk=7)

        self.utm = UTM.objects.get(pk=5)
        self.utm.serializer = UTMSerializers(instance=self.utm)

    def test_verifica_campos_serializados_de_utm(self):
        'Teste que verifica os campos serializados do modelo UTM'

        dados = self.utm.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'acesso', 'source', 'medium', 'campaign', 'channel']))

    def test_verifica_conteudos_serializados_de_utm(self):
        'Teste que verifica o conteudo dos campos serializados do modelo UTM'

        dados = self.utm.serializer.data

        self.assertEqual(dados['id'], self.utm.id)
        self.assertEqual(dados['acesso'], self.utm.acesso.id)
        self.assertEqual(dados['source'], self.utm.source)
        self.assertEqual(dados['medium'], self.utm.medium)
        self.assertEqual(dados['campaign'], self.utm.campaign)
        self.assertEqual(dados['channel'], self.utm.channel)