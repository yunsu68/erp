from django.db import transaction
from django.shortcuts import render, redirect
from .forms import ProductForm, InboundForm, OutboundForm
from .models import Product, Inbound
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/product-list')
    else:
        return redirect('/user-login')

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product-create')
    else:
        form = ProductForm()
    return render(request, 'erp/product_create.html', {'form': form})
@login_required
def product_list(request):
    if request.method == 'GET':
        all_product = Product.objects.all().order_by('code')
        return render(request, 'erp/product_list.html', {'product': all_product})

@login_required
def inventory(request):
    if request.method == 'GET':
        all_product = Product.objects.all().order_by('code')
        return render(request, 'erp/inventory.html', {'product': all_product})

@transaction.atomic
def inbound_create(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            my_message = False
            inbound = form.save(commit=False)
            product = Product.objects.get(code=form.cleaned_data['product_code'])
            if form.cleaned_data['inbound_cost'] != product.price*form.cleaned_data['inbound_quantity']:
                my_message = True
                return render(request, 'erp/inbound_create.html', {'message': my_message})
            else:
                new_quantity = product.inventory.total_inventory + form.cleaned_data['inbound_quantity']
                product.inventory.total_inventory = new_quantity
                product.inventory.total_cost += form.cleaned_data['inbound_cost']
                product.inventory.save()
                inbound.save()
                return redirect('/inbound-create')
    else:
        form = InboundForm()
    return render(request, 'erp/inbound_create.html', {'form': form})

@login_required
@transaction.atomic
def outbound_create(request):
    if request.method == 'POST':
        form = OutboundForm(request.POST)
        if form.is_valid():
            my_message = False
            outbound = form.save(commit=False)
            product = Product.objects.get(code=form.cleaned_data['product_code'])
            if form.cleaned_data['outbound_cost'] != product.price*form.cleaned_data['outbound_quantity']:
                my_message = 2
                return render(request, 'erp/inbound_create.html', {'message': my_message})
            elif form.cleaned_data['outbound_quantity'] > product.inventory.total_inventory:
                my_message = 1
                return render(request, 'erp/inbound_create.html', {'message': my_message})
            else:
                new_quantity = product.inventory.total_inventory - form.cleaned_data['outbound_quantity']
                product.inventory.total_inventory = new_quantity
                product.inventory.total_cost -= form.cleaned_data['outbound_cost']
                product.inventory.save()
                outbound.save()
                return redirect('/outbound-create')
    else:
        form = OutboundForm()
    return render(request, 'erp/outbound_create.html', {'form': form})



