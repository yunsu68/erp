from django import forms
from config.models import Product, Inbound, Outbound



# form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'description', 'price', 'size']



class DateInput(forms.DateInput):
    input_type = 'date'



class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product_code', 'inbound_quantity', 'inbound_date', 'inbound_cost']
        widgets = {
            'inbound_date': DateInput(),
        }

class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product_code', 'outbound_quantity', 'outbound_date', 'outbound_cost']
        widgets = {
            'outbound_date': DateInput(),
        }
