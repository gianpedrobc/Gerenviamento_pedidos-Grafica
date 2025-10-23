from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ("cliente", "Cliente"),
        ("gerente", "Gerente"),
    )
    email = models.EmailField(max_length=30, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='cliente')

    def __str__(self):
        return self.username

class ProdutoInterno(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    estoque_atual = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente de Aprovação'),
        ('aprovado', 'Aprovado'),
        ('producao', 'Em Produção'), 
        ('concluido', 'Concluído'), 
        ('cancelado', 'Cancelado'),
    )
    
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    )

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)

    order_number = models.CharField(max_length=20, unique=True, blank=True) 
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Pedido.objects.all().order_by('id').last()
            new_id = (last_order.id + 1) if last_order else 1
            self.order_number = f'PED-{new_id:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.order_number} - {self.titulo}"

class ItemPedido(models.Model):
    order = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'

class MensagemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.autor.username} no Pedido #{self.pedido.id}"

class AnexoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos_pedidos/')
    descricao = models.CharField(max_length=255, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo do Pedido #{self.pedido.id}"
    
class EntradaEstoque(models.Model):
    produto = models.ForeignKey(ProdutoInterno, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.PositiveIntegerField()
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} em {self.data_compra.strftime('%d/%m/%Y')}"