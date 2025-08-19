from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class EmpresaInfoView(View):
    def get(self, request, *args, **kwargs):
        # Devolver información básica de configuración
        return JsonResponse({
            'nombre_sistema': 'Packfy',
            'version': '1.0.0'
        })
    
    def post(self, request, *args, **kwargs):
        # Devolver información básica de configuración
        return JsonResponse({
            'nombre_sistema': 'Packfy',
            'version': '1.0.0'
        })
