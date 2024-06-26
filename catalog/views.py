from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Subquery, OuterRef
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm, VersionFormset, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_cached_categories


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания продукта
    """
    model = Product
    # fields = ('name', 'description', 'preview', 'category', 'price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductListView(ListView):
    """
    Класс для отображения списка продуктов
    """
    model = Product

    def get_context_data(self,*args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(is_active=True)
            if active_versions:
                product.active_version = active_versions.last().version_number
            else:
                product.active_version = '-'
        context_data['object_list'] = products
        return context_data


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')

    context = {'title': 'Контакты'}
    return render(request, 'catalog/contacts.html', context)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    класс для редактирования Продукта
    """
    model = Product
    form_class = ProductForm
    # permission_required = "catalog.change_product"
    # success_url = reverse_lazy('catalog:detail')

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:edit', args=[self.get_object().pk])

    def test_func(self):
        """
        Проверка пользователя, является ли владельцем продукта или модератором
        """
        user = self.request.user
        author = self.get_object().owner
        return user == author or user.groups.filter(name='moderator').exists()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_cancel_publish'):
            return ProductModeratorForm
        raise PermissionDenied


@login_required
def toggle_publish(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.user.has_perm('catalog.can_cancel_publish') or request.get_object().owner:
        if product_item.is_published:
            product_item.is_published = False
        else:
            product_item.is_published = True
        product_item.save()

        return redirect(reverse('catalog:list'))


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Класс для просмотра Продукта
    """
    model = Product


# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(id=pk),
#         'title': f'Вы выбрали {product_item.name}'
#     }
#     return render(request, 'catalog/product.html', context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления Продукта
    """
    model = Product
    success_url = reverse_lazy('catalog:list')


class CategoryListView(ListView):
    """
    Класс для отображения списка продуктов
    """
    model = Category
    template_name = 'catalog/category_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     context_data['object_list'] = get_cached_categories
    #     return context_data

    def get_queryset(self):
        return get_cached_categories()