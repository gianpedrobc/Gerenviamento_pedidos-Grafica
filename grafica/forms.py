
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, MensagemPedido, AnexoPedido, Usuario, ProdutoInterno, EntradaEstoque
from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'Endereço de E-mail',
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')

class PedidoForm(forms.ModelForm):
    anexo_principal = forms.FileField(
        label="Enviar um anexo (opcional)", 
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Pedido
        fields = ['titulo', 'descricao', 'deadline']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deadline': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d' 
            ),
        }
        
        labels = {
            'titulo': 'Título do Pedido',
            'descricao': 'Descrição Detalhada do que você precisa',
            'deadline': 'Sugestão de Prazo para Entrega',
        }

class MensagemPedidoForm(forms.ModelForm):
    class Meta:
        model = MensagemPedido
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua mensagem...',
                'aria-label': 'Mensagem'
            })
        }
        labels = {
            'texto': '' 
        }

class AnexoPedidoForm(forms.ModelForm):
    class Meta:
        model = AnexoPedido
        fields = ['arquivo', 'descricao']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'}) 
        }
        labels = {
            'status': '' 
        }

class ProdutoInternoForm(forms.ModelForm):
    class Meta:
        model = ProdutoInterno
        fields = ['nome', 'descricao', 'estoque_atual'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}), 
        }
        labels = {
            'nome': 'Nome do Produto/Material',
            'descricao': 'Descrição (Opcional)',
            'estoque_atual': 'Quantidade Inicial em Estoque (Opcional, pode adicionar depois)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estoque_atual'].required = False

class EntradaEstoqueForm(forms.ModelForm):
    novo_produto_nome = forms.CharField(
        label="Ou Crie um Novo Produto: Nome",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    novo_produto_descricao = forms.CharField(
        label="Descrição do Novo Produto (Opcional)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    class Meta:
        model = EntradaEstoque
        fields = ['produto', 'quantidade', 'custo_unitario'] 
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}), 
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'produto': 'Selecione um Produto Existente',
            'quantidade': 'Quantidade Comprada',
            'custo_unitario': 'Custo por Unidade (R$)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].required = False 
        self.fields['produto'].empty_label = "--- Selecione ---"

    def clean(self):
        cleaned_data = super().clean()
        produto_selecionado = cleaned_data.get('produto')
        novo_produto_nome = cleaned_data.get('novo_produto_nome')

        if produto_selecionado and novo_produto_nome:
            raise ValidationError(
                "Erro: Você não pode selecionar um produto existente E criar um novo ao mesmo tempo. Escolha apenas uma opção."
            )

        if not produto_selecionado and not novo_produto_nome:
            raise ValidationError(
                "Erro: Você precisa selecionar um produto existente OU informar o nome de um novo produto para cadastrar."
            )
            
        if novo_produto_nome and ProdutoInterno.objects.filter(nome__iexact=novo_produto_nome).exists():
            raise ValidationError(
                f"Erro: Já existe um produto chamado '{novo_produto_nome}'. Selecione-o na lista de produtos existentes."
            )

        return cleaned_data