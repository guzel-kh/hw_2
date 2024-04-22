from django.shortcuts import render

from catalog.models import Product


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная'
    }
    return render(request, 'catalog/index.html', context)


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


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(id=pk),
        'title': f'Вы выбрали {product_item.name}'
    }
    return render(request, 'catalog/product.html', context)

