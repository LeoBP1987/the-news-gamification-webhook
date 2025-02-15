from rest_framework import serializers
from webhook.models import Posts, Acessos, UTM
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    grupo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ( 'id', 'username', 'email', 'grupo')

    def get_grupo(self, obj):
        grupo = obj.groups.all()
        return grupo[0].name if grupo else None

class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('id_post', )

class AcessosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Acessos
        fields = ('id', 'leitor', 'id_post', 'abertura_dia', 'abertura_hora')

class AcessoPorPeriodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Acessos
        fields = ('id', 'leitor', 'id_post', 'abertura_hora')

class UTMSerializers(serializers.ModelSerializer):
    class Meta:
        model = UTM
        fields = ( 'id', 'acesso', 'source', 'medium', 'campaign', 'channel' )