from django.test import TestCase
from webhook.models import Posts, Acessos, UTM
from django.contrib.auth.models import User
from datetime import datetime

class FixturesTests(TestCase):

    fixtures = ['dados_dumped.json']

    def test_carregamento_fixtures(self):
        '''Teste de carregamento de Fixture'''

        usuario = User.objects.get(pk=9)
        post = Posts.objects.get(pk=1123)
        acesso = Acessos.objects.get(pk=7)
        utm = UTM.objects.get(pk=5)

        self.assertEqual(usuario.username, 'leonardobp1987@gmail.com')
        self.assertEqual(post.id, 1123)
        self.assertEqual(acesso.abertura_dia, datetime.strptime('2025-02-15', '%Y-%m-%d').date())
        self.assertEqual(utm.source, 'instagram')