from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
from .models import Factura 
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import Coalesce

class Chartboardview(TemplateView):
    template_name = 'graficas.html'
    def get_context_data(self ):
        data=[]
        year = datetime.now().year
        for m in range (1,13):
            total=Factura.objects.filter(user=self.user).filter(fecha_pedido_year=year,fecha_pedido_mes=m).aaggregate(r=Coalesce(Sum('total'),0)).get('r')
            data.append(float(total))
        return (data)

    def get_context(self,**kwargs):
        context =super.get_context(**kwargs)
        context['report_sales_year_month']=self.get_context_data()
        
        return context
    