from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Posts(models.Model):
    id_post = models.IntegerField(db_index=True, primary_key=True)

    def __str__(self):
        return self.id_post

class Acessos(models.Model):
    leitor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='acessos'
    )
    id_post = models.ForeignKey(
        to=Posts,
        on_delete=models.CASCADE,
        related_name='acessos'
    )
    abertura = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['leitor', 'abertura']),
            models.Index(fields=['id_post', 'abertura'])
        ]
    

    def __str__(self):
        return f'Acesso de {self.email.email} a {self.id_post.id_post} em {self.abertura}.'
    
class UTM(models.Model):
    acesso = models.ForeignKey(
        to=Acessos,
        on_delete=models.CASCADE,
        related_name='utms'
    )
    utm_source = models.CharField(max_length=50, db_index=True)
    utm_medium = models.CharField(max_length=50, db_index=True)
    utm_campaign = models.CharField(max_length=50, db_index=True)
    utm_channel = models.CharField(max_length=50, db_index=True)
    utm_variaveis = models.JSONField() 

    def __str__(self):
        return f'UTM de {self.acesso.leitor.email} no post {self.acesso.id_post.id_post} em {self.acesso.abertura}'
