from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pedido, MensagemPedido, AnexoPedido, ProdutoInterno, Usuario, EntradaEstoque 
from .forms import PedidoForm, CustomUserCreationForm, MensagemPedidoForm, OrderStatusForm, UserProfileForm,ProdutoInternoForm, EntradaEstoqueForm
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = 'grafica/home.html'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'

class InventoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ProdutoInterno
    template_name = 'grafica/inventory_list.html'
    context_object_name = 'produtos'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return ProdutoInterno.objects.all().order_by('nome')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'grafica/pedido_detail.html' 
    context_object_name = 'order' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MensagemPedidoForm() 
        
        context['status_form'] = OrderStatusForm(instance=self.object) 
        
        return context

    def post(self, request, *args, **kwargs):
        pedido = self.get_object()
        form = MensagemPedidoForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.pedido = pedido
            mensagem.autor = request.user
            mensagem.save()
            return render(request, 'grafica/partials/chat_messages.html', {'order': pedido})
        
        return render(request, 'grafica/partials/chat_messages.html', {'order': pedido})

@login_required
def upload_attachment_view(request, order_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=order_id)
        arquivo = request.FILES.get('file')
        if arquivo:
            AnexoPedido.objects.create(pedido=pedido, arquivo=arquivo)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'grafica/pedido_form.html'
    success_url = reverse_lazy('pedido_list') 

    def form_valid(self, form):
        form.instance.cliente = self.request.user
        
        response = super().form_valid(form)
        
        anexo = self.request.FILES.get('anexo_principal')
        
        if anexo:
            AnexoPedido.objects.create(pedido=self.object, arquivo=anexo)
            
        return response

class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'grafica/pedido_form.html'
    success_url = reverse_lazy('pedido_list')

class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'grafica/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido_list')

class ManagerDashboardView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Pedido
    template_name = 'grafica/manager_dashboard.html'
    context_object_name = 'pedidos'
    paginate_by = 15

    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = Pedido.objects.all().order_by('-data_criacao')
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Pedido.STATUS_CHOICES
        return context
    
class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'grafica/pedido_list.html'
    
    context_object_name = 'pedidos' 
    
    paginate_by = 10

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user).order_by('-data_criacao')
    
class ManagerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/create_manager.html' 
    success_url = reverse_lazy('manager_dashboard') 

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        
        user = self.object 
        
        user.is_staff = True
        user.save() 
        
        return response
    
def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user) 
def update_order_status_view(request, order_id):
    pedido = get_object_or_404(Pedido, id=order_id)
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            status_form_instance = OrderStatusForm(instance=pedido) 
            return render(request, 'grafica/partials/order_status.html', {'order': pedido, 'status_form': status_form_instance})
    
    return redirect('pedido_detail', pk=order_id)

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UserProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile') 

    def get_object(self, queryset=None):
        return self.request.user 
    def form_valid(self, form):
        from django.contrib import messages 
        messages.success(self.request, 'Seu perfil foi atualizado com sucesso!')
        return super().form_valid(form)
    
class ProdutoInternoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProdutoInterno
    form_class = ProdutoInternoForm
    template_name = 'grafica/produto_interno_form.html' 
    success_url = reverse_lazy('inventory_list') 

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, f'Produto "{form.instance.nome}" adicionado ao estoque com sucesso!')
        return super().form_valid(form)
    
class EntradaEstoqueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EntradaEstoque
    form_class = EntradaEstoqueForm
    template_name = 'grafica/entrada_estoque_form.html' 
    success_url = reverse_lazy('inventory_list')

    def test_func(self):
        return self.request.user.is_staff
       
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        novo_nome = cleaned_data.get('novo_produto_nome')
        produto_selecionado = cleaned_data.get('produto')
        quantidade = cleaned_data.get('quantidade')
        custo_unitario = cleaned_data.get('custo_unitario')

        produto_final = None
        produto_nome_msg = ""

        try:
            if novo_nome:
                novo_descricao = cleaned_data.get('novo_produto_descricao', '')
                produto_final = ProdutoInterno.objects.create(
                    nome=novo_nome, 
                    descricao=novo_descricao, 
                    estoque_atual=0 
                )
                produto_nome_msg = novo_nome
            elif produto_selecionado:
                produto_final = produto_selecionado
                produto_nome_msg = produto_final.nome
            
            if produto_final:
                EntradaEstoque.objects.create(
                    produto=produto_final,
                    quantidade=quantidade,
                    custo_unitario=custo_unitario
                )
                produto_final.estoque_atual += quantidade
                produto_final.save()

                messages.success(self.request, f'{quantidade} unidade(s) de "{produto_nome_msg}" registradas no estoque.')
                return redirect(self.get_success_url()) 
            else:
                messages.error(self.request, "Erro: Não foi possível determinar o produto. Tente novamente.")
                return self.form_invalid(form)

        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro inesperado: {e}")
            return self.form_invalid(form)