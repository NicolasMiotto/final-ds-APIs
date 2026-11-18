from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min
from .models import Planeta
from .serializers import PlanetaSerializer

class PlanetaViewSet(viewsets.ModelViewSet):
    queryset = Planeta.objects.all()
    serializer_class = PlanetaSerializer

    # 1. GET /api/planetas/por-tipo/?tipo=Gigante Gasoso
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        tipo = request.query_params.get('tipo')
        if tipo:
            planetas = self.queryset.filter(tipo_planeta__iexact=tipo)
            serializer = self.get_serializer(planetas, many=True)
            return Response(serializer.data)
        return Response({"erro": "Parâmetro 'tipo' é obrigatório."}, status=400)

    # 2. GET /api/planetas/mais-proximos/
    @action(detail=False, methods=['get'])
    def mais_proximos(self, request):
        planetas = self.queryset.filter(distancia__isnull=False).order_by('distancia')[:20]
        serializer = self.get_serializer(planetas, many=True)
        return Response(serializer.data)

    # 3. GET /api/planetas/por-metodo/?metodo=Transito
    @action(detail=False, methods=['get'])
    def por_metodo(self, request):
        metodo = request.query_params.get('metodo')
        if metodo:
            planetas = self.queryset.filter(metodo_descoberta__iexact=metodo)
            serializer = self.get_serializer(planetas, many=True)
            return Response(serializer.data)
        return Response({"erro": "Parâmetro 'metodo' é obrigatório."}, status=400)

    # 4. GET /api/planetas/recentes/?ano=2015
    @action(detail=False, methods=['get'])
    def recentes(self, request):
        ano = request.query_params.get('ano')
        if ano:
            planetas = self.queryset.filter(ano_descoberta__gte=ano).order_by('-ano_descoberta')
            serializer = self.get_serializer(planetas, many=True)
            return Response(serializer.data)
        return Response({"erro": "Parâmetro 'ano' é obrigatório."}, status=400)

    # 5. GET /api/planetas/estatisticas/
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        total = self.queryset.count()
        media_distancia = self.queryset.aggregate(Avg('distancia'))['distancia__avg']
        ano_mais_antigo = self.queryset.aggregate(Min('ano_descoberta'))['ano_descoberta__min']
        
        dados = {
            "total_planetas": total,
            "distancia_media_anos_luz": round(media_distancia, 2) if media_distancia else None,
            "ano_descoberta_mais_antiga": ano_mais_antigo
        }
        return Response(dados)