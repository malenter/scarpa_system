from django.shortcuts import render ,redirect  ,get_object_or_404 ,HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth import login ,logout,authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import cleinteform ,Zapatoform , FacturaForm , PedidoForm ,EncuestaForm ,Userprofileform
from .models import cliente ,Zapato ,Factura ,Pedido,Ciudad,UserProfile , Encuesta
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import plotly.graph_objs as go
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from django.db.models import Sum
from .models import Factura
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from crm import settings
from email.mime.text import MIMEText
import smtplib
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart

from email.mime.image import MIMEImage

@login_required
def encuesta_detail(request):
    encuesta = Encuesta.objects.filter(user=request.user)
    return render(request, 'encuesta_detail.html', {'encuesta': encuesta})

@login_required
def profile_detail(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile_detail.html', {'user_profile': user_profile})

@login_required
def foto_profile(request):
     user_profile_foto = UserProfile.objects.get(user=request.user)
     return render(request, 'index.html' , {'user_profile': user_profile_foto})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = Userprofileform(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige a la misma vista después de guardar
    else:
        form = Userprofileform(instance=user_profile)
    
    return render(request, 'profile_user.html', {'form': form})
def send_email_to_client_encuesta(request, cliente_id):
    try:
        mail_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado al servidor de correo...')

        cliente1 = get_object_or_404(cliente, id=cliente_id, user=request.user)
    

        # Genera la URL para que el cliente complete la encuesta
        encuesta_url = request.build_absolute_uri(f'/encuesta/{cliente_id}/')

        html_content = render_to_string('email_encuesta.html', {
            'nombre_cliente': cliente1.nombre,
            'encuesta_url': encuesta_url,
        })

        mensaje = MIMEMultipart('alternative')
        mensaje.attach(MIMEText(html_content, 'html'))
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = cliente1.correo
        mensaje['Subject'] = "Encuesta de Satisfacción"

        mail_server.sendmail(settings.EMAIL_HOST_USER,
                             cliente1.correo,
                             mensaje.as_string())
        print(f'Correo enviado a {cliente1.nombre} correctamente')

        mail_server.quit()
        print('Correo enviado correctamente')

    except cliente.DoesNotExist:
        print('El cliente no existe o no está asociado al usuario actual.')
    except Exception as e:
        print('Error al enviar el correo:', e)

def mi_vista_email_encuesta(request, cliente_id):
    if request.method == 'POST':
        send_email_to_client_encuesta(request, cliente_id)
        return redirect('clientes')  # Cambia 'clientes' si tienes una URL llamada 'clientes'
    clientes = get_object_or_404(cliente, id=cliente_id)
    return render(request, 'clientes.html', {'cliente': clientes})

@login_required
def encuesta_view(request, cliente_id):
    cliente1 = get_object_or_404(cliente, id=cliente_id, user=request.user)
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.cliente = cliente1
            encuesta.user = request.user
            encuesta.save()
            return redirect('gracias_encuesta')
    else:
        form = EncuestaForm()
    return render(request, 'encuesta.html', {'form': form, 'cliente': cliente1})

@login_required
def gracias_encuesta(request):
    return render(request, 'gracias_encuesta.html')


def send_email_to_client_factura(request, factura_id):
    try:
        mail_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado al servidor de correo...')

        factura = get_object_or_404(Factura, id=factura_id, cliente__user=request.user)
        cliente1 = factura.cliente
        pedidos = Pedido.objects.filter(factura=factura)

        html_content = render_to_string('new-email.html', {
            'nombre_cliente': cliente1.nombre,
            'factura': factura,
            'pedidos': pedidos
        })

        mensaje = MIMEMultipart('alternative')
        mensaje.attach(MIMEText(html_content, 'html'))
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = cliente1.correo
        mensaje['Subject'] = "Actualización del estado del pedido"

        mail_server.sendmail(settings.EMAIL_HOST_USER,
                             cliente1.correo,
                             mensaje.as_string())
        print(f'Correo enviado a {cliente1.nombre} correctamente')

        mail_server.quit()
        print('Correo enviado correctamente')

    except Factura.DoesNotExist:
        print('La factura no existe o no está asociada al usuario actual.')
    except Exception as e:
        print('Error al enviar el correo:', e)

def mi_vista_email(request, factura_id):
    if request.method == 'POST':
        send_email_to_client_factura(request, factura_id)
        return redirect('facturas')  # Cambia 'facturas' si tienes una URL llamada 'facturas'
    factura = get_object_or_404(Factura, id=factura_id, cliente__user=request.user)
    cliente1 = factura.cliente
    return render(request, 'factura.html', {'Factura': factura, 'Cliente': cliente1})



def send_email_to_client(request, cliente_id):
    try:
        mail_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado al servidor de correo...')

        cliente1 = cliente.objects.get(id=cliente_id, user=request.user)
        zapatos = Zapato.objects.filter(user=request.user)


        html_content = render_to_string('new-email-zapatos.html', {
            'nombre_cliente': cliente1.nombre,
            'zapatos': zapatos
        })
      
        mensaje = MIMEMultipart('alternative')
        mensaje.attach(MIMEText(html_content, 'html'))
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = cliente1.correo
        mensaje['Subject'] = "Muestrario de Zapatos Disponibles"
        
        for zapato in zapatos:
            if zapato.foto:
                with open(zapato.foto.path, 'rb') as img_file:
                    img_data = img_file.read()
                    img = MIMEImage(img_data)
                    img.add_header('Content-ID', f'<{zapato.foto.url}>')
                    mensaje.attach(img)
                    zapato.foto_cid = zapato.foto.url

        mail_server.sendmail(settings.EMAIL_HOST_USER,
                             cliente1.correo,
                             mensaje.as_string())
        print(f'Correo enviado a {cliente1.nombre} correctamente')

        mail_server.quit()
        print('Correo enviado correctamente')

    except cliente.DoesNotExist:
        print('El cliente no existe o no está asociado al usuario actual.')
    except Exception as e:
        print('Error al enviar el correo:', e)

def mi_vista_muestrario(request, cliente_id):
    if request.method == 'POST':
        send_email_to_client(request, cliente_id)
        return redirect('clientes')
    clientes = get_object_or_404(cliente, id=cliente_id)
    return render(request, 'clientes.html', {'Clientes': clientes})

# Create your views here.

def obtener_ciudades(request):
    if request.method == 'GET' and 'departamento_id' in request.GET:
        departamento_id = request.GET.get('departamento_id')
        ciudades = Ciudad.objects.filter(departamento_id=departamento_id)
        ciudades_list = list(ciudades.values())
        return JsonResponse(ciudades_list, safe=False)
    else:
        return JsonResponse({'error': 'Se requiere el ID del departamento.'})

@login_required
def inicio(request):
    ventas_por_anio = (
          Factura.objects
           .filter(user=request.user, pago=True)
           .annotate(Year=ExtractYear('fecha_pedido'))  # Añadir el año de la factura como campo 'anio'
        .values('Year')
        .annotate(total_ventas=Sum('total'))
        .order_by('Year') )
    total_facturas_no_pagadas = Factura.objects.filter( user=request.user ,pago=False).count()

    total_pedidos = Pedido.objects.filter(user=request.user).count()
    pedidos_no_iniciados = Pedido.objects.filter(user=request.user,estado='no iniciado').count()
    pedidos_en_proceso = Pedido.objects.filter(user=request.user).exclude(estado='no iniciado').exclude(estado='terminado').count()
    pedidos_completados = Pedido.objects.filter(user=request.user,estado='terminando').count()
    facturas = Factura.objects.filter(user=request.user)
    context = {
        'facturas': ventas_por_anio,
         'total_facturas_no_pagadas': total_facturas_no_pagadas,
        'total_pedidos_no_cancelados': total_pedidos,
        'pedidos_no_iniciados': pedidos_no_iniciados,
        'pedidos_en_proceso': pedidos_en_proceso,
        'facturas_mas':facturas,

      }

  
    return render(request,'inicio.html',context)

@login_required
def plotly_ventas_mes(request):
    ventas_por_mes = Factura.objects.filter(user=request.user).filter(pago=True).annotate(month=ExtractMonth('fecha_pedido')).values('month').annotate(total_ventas=Sum('total')).order_by('month')
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']  
    ventas = [0] * 12  
    for venta in ventas_por_mes:
        mes_index = venta['month'] - 1  
        ventas[mes_index] = venta['total_ventas']
    trace_ventas_mes = go.Bar(x=meses,
                   y=ventas,
                   marker=dict(color='rgb(26, 118, 255)'))
    data_ventas_mes = [trace_ventas_mes]
    layout_ventas_mes = go.Layout(title='Ventas por Mes',
                       xaxis=dict(title='Mes'),
                       yaxis=dict(title='Total de ventas'))
    fig_ventas_mes = go.Figure(data=data_ventas_mes, layout=layout_ventas_mes)
    plot_div_ventas_mes = fig_ventas_mes.to_html(full_html=False)

    # Código para el gráfico de ventas por producto
    ventas_por_producto = Pedido.objects.filter(user=request.user).values('zapato__nombre').annotate(total_cantidad=Sum('canitdad'))
    labels = []
    values = []
    for venta in ventas_por_producto:
        producto_nombre = venta['zapato__nombre']
        cantidad_vendida = venta['total_cantidad']
        labels.append(producto_nombre)
        values.append(cantidad_vendida)
    trace_ventas_producto = go.Pie(labels=labels,
                   values=values,
                   hole=0.3)
    data_ventas_producto = [trace_ventas_producto]
    layout_ventas_producto = go.Layout(title='Porcentaje de ventas por producto')
    fig_ventas_producto = go.Figure(data=data_ventas_producto, layout=layout_ventas_producto)
    plot_div_ventas_producto = fig_ventas_producto.to_html(full_html=False)

    return render(request, 'graficas.html', context={'plot_div_ventas_mes': plot_div_ventas_mes, 'plot_div_ventas_producto': plot_div_ventas_producto})

def home(request):
    return render(request, 'home.html')

  
@login_required        
def signaout(request):
    logout(request)
    return redirect(' ')

def singnup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Username already exits'})

        return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'contraseñas no coninciden'})
def siging(request):
    if request.method =='GET':
         return render(request,'login.html',{'form':AuthenticationForm})
    else:
         user=authenticate(request,username=request.POST['username'], password=request.POST['password'])
         if user is None:
              return render(request,'login.html',{'form':AuthenticationForm,'error':'username or passwors is incorrect'})
         else:
             login(request,user)
             return redirect('home')
        

@login_required
def clientes(request):
    clientes=cliente.objects.filter(user=request.user)

    return render(request,'clientes.html',{'Clientes':clientes})

@login_required
def create_clientes(request):
    if request.method =='GET':
       return render(request,'crear_clientes.html',{'form':cleinteform})
    else:
          try:
              form=cleinteform(request.POST)
              new_task= form.save(commit=False)
              new_task.user=request.user
              new_task.save()
              return redirect('clientes')
          except ValueError:
                   return render(request,'create_task.html',{'form':cleinteform,'ERROR':'DA UNOS DATOS QUE SEAN LEGIBLES'})
          

@login_required        
def signaout(request):
    logout(request)
    return redirect('')

@login_required
def task_detail(request,cliente_id):
    if request .method =='GET':
        task=get_object_or_404(cliente,pk=cliente_id,user=request.user)
        form=cleinteform(instance=task)
        return render(request,'clientes_detalle.html',{'task':task,'form': form})
    else:
         try:
             task= get_object_or_404(cliente,pk=cliente_id)
             form=cleinteform(request.POST,instance=task)
             form.save()
             return redirect('clientes')
        
         except ValueError:
              return render(request,'clientes_detalle.html',{'task':task,'form': form,'error':'error al cargar la task'})
@login_required
def delete_task(request,cliente_id):
    task=get_object_or_404(cliente,pk=cliente_id,user=request.user)
    if request .method =='POST':
        task.delete()
        return redirect('clientes') 

@login_required  
def Zapatos(request):
    zapato=Zapato.objects.filter(user=request.user)

    return render(request,'zapato.html',{'Zapato':zapato})

@login_required
def crear_Zapatos(request):
    if request .method =='GET':
       return render(request,'crear_zapato.html',{'form':Zapatoform})
    else:
          print("Datos recibidos:", request.POST, request.FILES)
          try:
              form=Zapatoform(request.POST, request.FILES)
              new_task= form.save(commit=False)
              new_task.user=request.user
              new_task.save()
              messages.success(request, ('La imagen fue registrada con exito'))
              return redirect('zapato')
          except ValueError :
                   messages.error(request, 'Error, no se pudo registrar la imagen.')
                   return render(request,'crear_zapato.html',{'form':Zapatoform,'ERROR':'DA UNOS DATOS QUE SEAN LEGIBLES'})

@login_required
def Zapato_detail(request,Zapato_id):
    if request .method =='GET':
        zapato=get_object_or_404(Zapato,pk=Zapato_id,user=request.user)
        form_zapato=Zapatoform(instance=zapato)
        return render(request,'zapato_detail.html',{'zapato':zapato,'form_zapato': form_zapato})
    else:
         print("Datos recibidos:", request.POST, request.FILES)
         try:
             zapato= get_object_or_404(Zapato,pk=Zapato_id)
             form_zapato=Zapatoform(request.POST,request.FILES,instance=zapato)
             form_zapato.save()
             return redirect('zapato')
        
         except ValueError:
              return render(request,'zapato_detail.html',{'zapato':zapato,'form_zapato': form_zapato,'error':'error al cargar la task'})
          
@login_required
def delete_zapato(request,Zapato_id):
    task=get_object_or_404(Zapato,pk=Zapato_id,user=request.user)
    if request .method =='POST':
        task.delete()
        return redirect('zapato') 
    
@login_required
def facturas(request):
     facturas=Factura.objects.filter(user=request.user)
     return render(request,'factura.html',{'facturas':facturas})

@login_required
def create_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.user, request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('facturas')
    else:
        form = FacturaForm(request.user)
    
    return render(request, 'create_factura.html', {'form': form})

@login_required
def pagar_factura(request, factura_id):
    factura=get_object_or_404(Factura,pk=factura_id,user=request.user)
    if request .method =='POST':
      factura = Factura.objects.get(id=factura_id)
      factura.pago = True
      factura.save()
      return redirect('facturas')

@login_required
def entregar_factura(request, factura_id):
    factura=get_object_or_404(Factura,pk=factura_id,user=request.user)
    if request .method =='POST':
      factura = Factura.objects.get(id=factura_id)
      factura.fecha_de_entrega = timezone.now()
      factura.save()
    return redirect('facturas')

@login_required
def delete_factura(request, factura_id):
    factura=get_object_or_404(Factura,pk=factura_id,user=request.user)
    if request .method =='POST':
        factura.delete()
        return redirect('facturas') 

@login_required
def factura_detail(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id, user=request.user)
    
    if request.method == 'POST':
        form = FacturaForm(request.user, request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('facturas')
    else:
        form = FacturaForm(request.user, instance=factura)
    
    return render(request, 'factura_detail.html', {'factura': factura, 'form': form})

@login_required
def pedidos(request):
     pedidos=Pedido.objects.filter(user=request.user)
     return render(request,'pedido.html',{'pedidos':pedidos})

@login_required
def create_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.user, request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('pedidos')
    else:
        form = PedidoForm(request.user)
        
    return render(request, 'create_pedido.html', {'form': form})

def pedidos_detail(request, pedidos_id):
    pedidos = get_object_or_404(Pedido, pk=pedidos_id, user=request.user)
    
    if request.method == 'POST':
        form = PedidoForm(request.user, request.POST, instance=pedidos)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm(request.user, instance=pedidos)
    
    return render(request, 'pedidos_detail.html', {'pedidos': pedidos, 'form': form})

@login_required
def delete_pedido(request, pedidos_id):
    pedido=get_object_or_404(Pedido,pk=pedidos_id,user=request.user)
    if request .method =='POST':
        pedido.delete()
        return redirect('pedidos')

@login_required
def busqueda_clientes(request):
        busqueda = request.GET.get('buscar')
        clientes = cliente.objects.filter(user=request.user)
        if busqueda:
            clientes = clientes.filter(Q(nombre__icontains=busqueda) |
                                       Q(ciudad__icontains=busqueda) |
                                       Q(departamento__icontains=busqueda) |
                                       Q(local__icontains=busqueda)).distinct()

        else:
            print("Sin término de búsqueda. Mostrando todos los clientes.")

        return render(request, 'clientes.html', {'Clientes': clientes})

      

@login_required

def busqueda_zapato(request):
        busqueda = request.GET.get('buscar')
        print("Término de búsqueda recibido:", busqueda)

        zapatos = Zapato.objects.filter(user=request.user)
        
        if busqueda:
            print("Realizando búsqueda con término:", busqueda)

            zapatos = zapatos.filter(Q(nombre__icontains=busqueda) |
                                       Q(color__icontains=busqueda) |
                                       Q(tipo__icontains=busqueda) ).distinct()
            
            print("Número de zapatos encontrados:", zapatos.count())

        else:
             print("Sin término de búsqueda. Mostrando todos los zapatos.")
        

        return render(request, 'zapato.html', {'Zapato': zapatos})

@login_required

def busqueda_pedido(request):
        busqueda = request.GET.get('buscar')
        pedido = Pedido.objects.filter(user=request.user)
        
        if busqueda:
            pedido = pedido.filter(Q(factura__nombre__icontains=busqueda) |
                                       Q(estado__icontains=busqueda) |
                                       Q(zapato__nombre__icontains=busqueda)|
                                         Q(factura__cliente__nombre__icontains=busqueda)).distinct()

        else:
             print("Sin término de búsqueda. Mostrando todos los pedidos.")
        

        return render(request, 'pedido.html', {'pedidos': pedido})

@login_required

def busqueda_factura(request):
        busqueda = request.GET.get('buscar')
        factura = Factura.objects.filter(user=request.user)
        
        if busqueda:
            factura = factura.filter(Q(nombre__icontains=busqueda) |
                                       Q(cliente__nombre__icontains=busqueda) ).distinct()

        else:
             print("Sin término de búsqueda. Mostrando todos las facturas.")
        

        return render(request, 'factura.html', {'facturas': factura})
  
  

