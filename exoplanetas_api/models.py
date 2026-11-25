from django.db import models

class Planeta(models.Model):
    nome = models.CharField(max_length=150)
    distancia = models.FloatField(null=True, blank=True)
    magnitude_estelar = models.FloatField(null=True, blank=True)
    tipo_planeta = models.CharField(max_length=50, null=True, blank=True)
    ano_descoberta = models.IntegerField(null=True, blank=True)
    multiplicador_massa = models.FloatField(null=True, blank=True)
    massa_relativa = models.CharField(max_length=50, null=True, blank=True)
    multiplicador_raio = models.FloatField(null=True, blank=True)
    raio_relativo = models.CharField(max_length=50, null=True, blank=True)
    raio_orbital = models.FloatField(null=True, blank=True)
    periodo_orbital = models.FloatField(null=True, blank=True)
    excentricidade = models.FloatField(null=True, blank=True)
    metodo_descoberta = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'planetas'
        managed = False  # tabela criada pelo database/db_exoplanetas.sql

    def __str__(self):
        return self.nome