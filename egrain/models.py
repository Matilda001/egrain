# -*- coding: UTF-8 -*-

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.html import escape

# Create your models here.

class Cornfield(models.Model):
    name_field = models.CharField(max_length=20)
    area = models.DecimalField(decimal_places=2, max_digits=10)
    mpoly_coding_paths = models.TextField()
    mpoly_coding_levels = models.TextField()
    use_user = models.ForeignKey(User)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name_field


class HistoryCornfield(models.Model):
    cornfield = models.ForeignKey('Cornfield')
    year = models.IntegerField(verbose_name=u'Год')
    agriculture_name = models.ForeignKey('Agriculture', verbose_name=u'Культура')
    prolificness = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=u'Урожайность')
    fallout = models.CharField(max_length=120, null=True, blank=True, verbose_name=u'Осадки')

    def __unicode__(self):
        return '%s'%self.year

class Agriculture(models.Model):
    name_agriculture = models.CharField(max_length=120, verbose_name=u'Культура')
    color_agriculture = models.CharField(max_length=7, verbose_name=u'Цвет')

    def __unicode__(self):
        #return mark_safe(u'''<div style="background-color:"%s"; width:15px; height:15px;>%s</div>'''%(self.color_agriculture, self.name_agriculture ))
        return self.name_agriculture

class Manure(models.Model):
    name_manure = models.CharField(max_length=120, verbose_name=u'Удобрения')

    def __unicode__(self):
        return self.name_manure


class CornfieldManure(models.Model):
    manure_name = models.ForeignKey('Manure', null=True, blank=True)
    field_manure = models.ForeignKey('HistoryCornfield', null=True, blank=True)



