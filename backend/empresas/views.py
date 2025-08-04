from rest_framework import viewsets, permissions
from .models import Empresa
from .serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para empresas.
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAdminUser]  # Solo administradores pueden gestionar empresas
