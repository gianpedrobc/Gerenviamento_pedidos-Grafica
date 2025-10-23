from django.contrib import admin
from .models import Usuario, Pedido, MensagemPedido, AnexoPedido
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(MensagemPedido)
admin.site.register(AnexoPedido)