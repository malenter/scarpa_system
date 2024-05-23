from django  import forms
from .models import cliente ,Zapato ,Factura , Pedido , Encuesta ,UserProfile
from django.contrib.auth.models import User

class Userprofileform(forms.ModelForm):
    class Meta:  
        model=UserProfile
        fields=['nombre_empresa','correo','telefono','logo',]
        widgets ={
            'nombre_empresa':forms.TextInput(attrs={'class':'form-control  border border-dark'}),
            'correo':forms.EmailInput(attrs={'class':'form-control  border border-dark'}),
            'telefono':forms.NumberInput(attrs={'class':'form-control  border border-dark'}),
            'logo':forms.FileInput(attrs={'class':'form-control  border border-dark'}),
            }
class cleinteform(forms.ModelForm):
    class Meta:  
        model=cliente
        fields=['nombre','correo','numero','departamento','ciudad','dirreccion','local']
        widgets ={
            'nombre':forms.TextInput(attrs={'class':'form-control  border border-dark'}),
            'correo':forms.EmailInput(attrs={'class':'form-control  border border-dark'}),
            'numero':forms.NumberInput(attrs={'class':'form-control  border border-dark'}),
            'departamento':forms.Select(attrs={'class':'form-control  border border-dark ','id': 'id_departamento'}),
            'ciudad':forms.Select(attrs={'class':'form-control  border border-dark','id': 'id_ciudad'}),
            'dirreccion':forms.TextInput(attrs={'class':'form-control  border border-dark'}),
            'local':forms.TextInput(attrs={'class':'form-control  border border-dark'})
            }
        
class Zapatoform(forms.ModelForm):
    class Meta:
        model =Zapato
        fields=['nombre','color','tipo','foto']
        widgets={
             'nombre': forms.TextInput(attrs={'class': 'form-control  border border-dark'}),
            'color': forms.TextInput(attrs={'class': 'form-control  border border-dark'}),
            'tipo': forms.Select(attrs={'class': 'form-control  border border-dark'}), 
            'foto': forms.FileInput(attrs={'class': 'form-control  border border-dark'}),  }
        

class FacturaForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = cliente.objects.filter(user=user)
    class Meta:
        model = Factura
        fields = ['cliente', 'fecha_pedido','nombre']
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control border border-dark'}),
            'cliente': forms.Select(attrs={'class': 'form-control  border border-dark'}),
            'fecha_pedido': forms.DateInput(attrs={'class': 'form-control  border border-dark ','type': 'date'}),
        }

class PedidoForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['zapato'].queryset = Zapato.objects.filter(user=user)
        self.fields['factura'].queryset = Factura.objects.filter(user=user)
    class Meta:
        model = Pedido
        fields = ['zapato', 'estado', 'canitdad', 'talla', 'valor', 'factura','fecha_pedido']
        labels = {
            'factura': 'Orden de pedido',  
        }
        widgets = {
            'zapato': forms.Select(attrs={'class': 'form-control  border border-dark'}),
            'estado': forms.Select(attrs={'class': 'form-control  border border-dark'}),
            'canitdad': forms.NumberInput(attrs={'class': 'form-control  border border-dark'}),
            'talla': forms.TextInput(attrs={'class': 'form-control  border border-dark'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control  border border-dark'}),
            'factura': forms.Select(attrs={'class': 'form-control  border border-dark'}),
            'fecha_pedido': forms.DateInput(attrs={'class': 'form-control   border border-dark','type': 'date'}),
        }

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['pregunta_1', 'pregunta_2', 'pregunta_3','pregunta_4','pregunta_5','pregunta_6']
        widgets = {
            'pregunta_1': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'pregunta_2': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'pregunta_3': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'pregunta_4': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'pregunta_5': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'pregunta_6' :forms.Textarea(attrs={'rows': 3, 'cols': 40}),
             }
        labels = {
            'pregunta_1': '¿Cómo calificaría el servicio recibido?',
            'pregunta_2': '¿Cómo calificaría la atención al cliente?',
            'pregunta_3': '¿Está satisfecho con la calidad del producto?',
            'pregunta_4': '¿Cómo evaluaría el tiempo de espera?',
            'pregunta_5': '¿Recomendaría nuestro servicio a otros?',
            'pregunta_6': 'Comentarios o recomendaciones adicionales:',
        }
        help_texts = {
            'pregunta_1': '1: Muy Malo, 5: Excelente',
            'pregunta_2': '1: Muy Malo, 5: Excelente',
            'pregunta_3': '1: Muy Malo, 5: Excelente',
            'pregunta_4': '1: Muy Malo, 5: Excelente',
            'pregunta_5': '1: Definitivamente no, 5: Definitivamente sí',
            'pregunta_6': 'recomendaciones adicionales que quiera hacer  a nuestro servicio ',

        }




