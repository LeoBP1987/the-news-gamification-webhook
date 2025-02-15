from django.contrib import admin
from webhook.models import Posts, Acessos, UTM

class PostsAdmin(admin.ModelAdmin):
    list_display= ('id_post', )
    list_display_links= ('id_post', )
    list_per_page = 10
    list_filter = ('id_post', )
    search_fields = ('id_post', )
    ordering = ('id_post', )

admin.site.register(Posts, PostsAdmin)

class AcessosAdmin(admin.ModelAdmin):
    list_display= ('leitor', 'id_post', 'abertura_dia', 'abertura_hora')
    list_display_links= ('leitor', 'id_post', 'abertura_dia', 'abertura_hora')
    list_per_page = 10
    list_filter = ('leitor__email', 'id_post__id_post', 'abertura_dia', 'abertura_hora')
    search_fields = ('leitor__email', 'id_post__id_post', 'abertura_dia', 'abertura_hora')
    ordering = ('leitor', 'id_post', 'abertura_dia', 'abertura_hora')

admin.site.register(Acessos, AcessosAdmin)

class UTMAdmin(admin.ModelAdmin):
    list_display=( 'acesso', 'source', 'medium', 'campaign', 'channel' )
    list_display_links=('acesso' ,'source', 'medium')
    list_per_page = 10
    list_filter = ('source', 'medium', 'campaign', 'channel')
    search_fields = ('source', 'medium', 'campaign', 'channel')
    ordering = ('source', )

admin.site.register(UTM, UTMAdmin)