from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Posts(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)

    def __str__(self):
        return f'{self.id}'

class Acessos(models.Model):
    leitor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='acessos'
    )
    post = models.ForeignKey(
        to=Posts,
        on_delete=models.CASCADE,
        related_name='acessos'
    )
    abertura_dia = models.DateField(db_index=True)
    abertura_hora = models.TimeField(db_index=True)
    abertura_dia_semana = models.IntegerField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['leitor', 'abertura_dia']),
            models.Index(fields=['leitor', 'abertura_hora']),
            models.Index(fields=['post', 'abertura_dia']),
            models.Index(fields=['post', 'abertura_hora'])
        ]
    

    def __str__(self):
        return f'Acesso de {self.leitor.email} a {self.post.id} em {self.abertura_dia}.'
    
class UTM(models.Model):
    acesso = models.ForeignKey(
        to=Acessos,
        on_delete=models.CASCADE,
        related_name='utms'
    )
    source = models.CharField(max_length=50, db_index=True, null=True, default=None)
    medium = models.CharField(max_length=50, db_index=True, null=True, default=None)
    campaign = models.CharField(max_length=50, db_index=True, null=True, default=None)
    channel = models.CharField(max_length=50, db_index=True, null=True, default=None) 

    def __str__(self):
        return f'UTM de {self.acesso.leitor.email} no post {self.acesso.post.id} em {self.acesso.abertura_dia}'
