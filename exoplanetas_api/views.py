from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min, Max, Count
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, inline_serializer
from .models import Planeta
from .serializers import PlanetaSerializer


ERRO_400 = inline_serializer(name='Erro', fields={'erro': serializers.CharField()})


@extend_schema_view(
    list=extend_schema(summary='Lista todos os planetas (paginado)'),
    create=extend_schema(summary='Cadastra um novo planeta'),
    retrieve=extend_schema(summary='Exibe os detalhes de um planeta'),
    update=extend_schema(summary='Atualiza todos os campos de um planeta'),
    partial_update=extend_schema(summary='Atualiza parte dos campos de um planeta'),
    destroy=extend_schema(summary='Remove um planeta'),
)
class PlanetaViewSet(viewsets.ModelViewSet):
    queryset = Planeta.objects.all().order_by('id')
    serializer_class = PlanetaSerializer

    def _resposta_paginada(self, queryset):
        """Aplica a paginação padrão (settings.REST_FRAMEWORK) a uma lista filtrada."""
        pagina = self.paginate_queryset(queryset)
        if pagina is not None:
            serializer = self.get_serializer(pagina, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 1. GET /api/planetas/por-tipo/?tipo=Gigante Gasoso
    @extend_schema(
        summary='Filtra planetas por tipo',
        parameters=[OpenApiParameter(
            'tipo', str, required=True,
            description='Gigante Gasoso, Super-Terra, Tipo Netuno, Terrestre ou Desconhecido',
        )],
        responses={200: PlanetaSerializer(many=True), 400: ERRO_400},
    )
    @action(detail=False, methods=['get'], url_path='por-tipo')
    def por_tipo(self, request):
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response({"erro": "Parâmetro 'tipo' é obrigatório."}, status=400)
        planetas = self.get_queryset().filter(tipo_planeta__iexact=tipo)
        return self._resposta_paginada(planetas)

    # 2. GET /api/planetas/mais-proximos/
    @extend_schema(
        summary='Os 20 planetas mais próximos da Terra',
        responses={200: PlanetaSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='mais-proximos', pagination_class=None)
    def mais_proximos(self, request):
        planetas = self.get_queryset().filter(distancia__isnull=False).order_by('distancia')[:20]
        serializer = self.get_serializer(planetas, many=True)
        return Response(serializer.data)

    # 3. GET /api/planetas/por-metodo/?metodo=Transito
    @extend_schema(
        summary='Filtra planetas pelo método de descoberta',
        parameters=[OpenApiParameter(
            'metodo', str, required=True,
            description='Ex: Transito, Velocidade Radial, Imagem Direta, Astrometria, Microlentes Gravitacionais',
        )],
        responses={200: PlanetaSerializer(many=True), 400: ERRO_400},
    )
    @action(detail=False, methods=['get'], url_path='por-metodo')
    def por_metodo(self, request):
        metodo = request.query_params.get('metodo')
        if not metodo:
            return Response({"erro": "Parâmetro 'metodo' é obrigatório."}, status=400)
        planetas = self.get_queryset().filter(metodo_descoberta__iexact=metodo)
        return self._resposta_paginada(planetas)

    # 4. GET /api/planetas/recentes/?ano=2015
    @extend_schema(
        summary='Planetas descobertos a partir de um ano',
        parameters=[OpenApiParameter('ano', int, required=True, description='Ano inicial (ex: 2015)')],
        responses={200: PlanetaSerializer(many=True), 400: ERRO_400},
    )
    @action(detail=False, methods=['get'])
    def recentes(self, request):
        ano = request.query_params.get('ano')
        if not ano:
            return Response({"erro": "Parâmetro 'ano' é obrigatório."}, status=400)
        try:
            ano = int(ano)
        except ValueError:
            return Response({"erro": "Parâmetro 'ano' deve ser um número inteiro (ex: 2015)."}, status=400)
        planetas = self.get_queryset().filter(ano_descoberta__gte=ano).order_by('-ano_descoberta', 'id')
        return self._resposta_paginada(planetas)

    # 5. GET /api/planetas/estatisticas/
    @extend_schema(
        summary='Resumo analítico da base',
        responses={200: inline_serializer(name='Estatisticas', fields={
            'total_planetas': serializers.IntegerField(),
            'distancia_media_anos_luz': serializers.FloatField(allow_null=True),
            'ano_descoberta_mais_antiga': serializers.IntegerField(allow_null=True),
            'ano_descoberta_mais_recente': serializers.IntegerField(allow_null=True),
            'total_por_tipo': serializers.DictField(child=serializers.IntegerField()),
            'total_por_metodo': serializers.DictField(child=serializers.IntegerField()),
        })},
    )
    @action(detail=False, methods=['get'], pagination_class=None)
    def estatisticas(self, request):
        qs = self.get_queryset()
        agregados = qs.aggregate(
            media_distancia=Avg('distancia'),
            ano_min=Min('ano_descoberta'),
            ano_max=Max('ano_descoberta'),
        )
        media_distancia = agregados['media_distancia']

        por_tipo = {
            item['tipo_planeta']: item['total']
            for item in qs.values('tipo_planeta').annotate(total=Count('id')).order_by('-total')
        }
        por_metodo = {
            item['metodo_descoberta']: item['total']
            for item in qs.values('metodo_descoberta').annotate(total=Count('id')).order_by('-total')
        }

        dados = {
            "total_planetas": qs.count(),
            "distancia_media_anos_luz": round(media_distancia, 2) if media_distancia is not None else None,
            "ano_descoberta_mais_antiga": agregados['ano_min'],
            "ano_descoberta_mais_recente": agregados['ano_max'],
            "total_por_tipo": por_tipo,
            "total_por_metodo": por_metodo,
        }
        return Response(dados)
