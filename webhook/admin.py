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
    list_display= ('leitor', 'id_post', 'abertura')
    list_display_links= ('leitor', 'id_post', 'abertura')
    list_per_page = 10
    list_filter = ('leitor__email', 'id_post__id_post', 'abertura')
    search_fields = ('leitor__email', 'id_post__id_post', 'abertura')
    ordering = ('leitor', 'id_post', 'abertura')

admin.site.register(Acessos, AcessosAdmin)

class UTMAdmin(admin.ModelAdmin):
    list_display=('utm_source', 'utm_medium', 'utm_campaign', 'utm_channel', 'utm_variaveis')
    list_display_links=('utm_source', 'utm_medium')
    list_per_page = 10
    list_filter = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_channel')
    search_fields = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_channel')
    ordering = ('utm_source', )

admin.site.register(UTM, UTMAdmin)