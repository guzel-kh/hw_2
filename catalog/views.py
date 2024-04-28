from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductCreateView(CreateView):
    model = Product
    # fields = ('name', 'description', 'preview', 'category', 'price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')


class ProductListView(ListView):
    model = Product


# def index(request):
#     product_list = Product.objects.all()
#     context = {
#         'object_list': product_list,
#         'title': 'Главная'
#     }
#     return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'preview', 'price')
    # form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

# def toggle_activity(request, pk):
#     product_item = get_object_or_404(Product,pk=pk)
#     if product_item.is_active:
#         product_item.is_active = False
#     else:
#         product_item.is_active = True
#     product_item.save()
#
#     return redirect(reverse('catalog:index'))


class ProductDetailView(DetailView):
    model = Product


# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(id=pk),
#         'title': f'Вы выбрали {product_item.name}'
#     }
#     return render(request, 'catalog/product.html', context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')







# class VersionCreateView(CreateView):
#     model = Version
#     # form_class = VersionForm
#     success_url = reverse_lazy('catalog:index')
#
#     # def form_valid(self, form):
#     #     product_pk = self.kwargs['pk']  # Получаем pk продукта из URL
#     #     product = Product.objects.get(pk=product_pk)  # Получаем объект продукта
#     #     form.instance.product = product  # Устанавливаем продукт в поле версии
#     #     return super().form_valid(form)
#
#
# class VersionListView(ListView):
#     model = Product
#     # extra_context = {'title': 'Продукты'}


