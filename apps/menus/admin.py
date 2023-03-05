from django.contrib import admin

from apps.menus.models import Seccion,Menu,OfertGroup,Ofert


admin.site.register(Menu)
admin.site.register(Seccion)
admin.site.register(OfertGroup)
admin.site.register(Ofert)