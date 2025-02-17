from django.contrib import admin
from webhook.models import Posts, Acessos, UTM

class PostsAdmin(admin.ModelAdmin):
    list_display= ('id', 'resource_id' )
    list_display_links= ('id', 'resource_id' )
    list_per_page = 10
    list_filter = ('id', 'resource_id' )
    search_fields = ('id', 'resource_id' )
    ordering = ('id', 'resource_id' )

admin.site.register(Posts, PostsAdmin)

class AcessosAdmin(admin.ModelAdmin):
    list_display= ('leitor', 'post', 'abertura_dia', 'abertura_hora')
    list_display_links= ('leitor', 'post', 'abertura_dia', 'abertura_hora')
    list_per_page = 10
    list_filter = ('leitor__email', 'post__id', 'abertura_dia', 'abertura_hora')
    search_fields = ('leitor__email', 'post__id', 'abertura_dia', 'abertura_hora')
    ordering = ('leitor', 'post', 'abertura_dia', 'abertura_hora')

admin.site.register(Acessos, AcessosAdmin)

class UTMAdmin(admin.ModelAdmin):
    list_display=( 'acesso', 'source', 'medium', 'campaign', 'channel' )
    list_display_links=('acesso' ,'source', 'medium')
    list_per_page = 10
    list_filter = ('source', 'medium', 'campaign', 'channel')
    search_fields = ('source', 'medium', 'campaign', 'channel')
    ordering = ('source', )

admin.site.register(UTM, UTMAdmin)