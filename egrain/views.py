# -*- coding: UTF-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from pykml import parser
from agri.settings import MEDIA_ROOT
import os
from django.core.serializers import serialize
from django.utils import simplejson
from lxml import etree
from pykml.parser import Schema
from django.template import RequestContext
from django.contrib.gis.maps import google
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.maps.google.overlays import GPolygon
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.geos import fromstr, LinearRing, Point, MultiPolygon, Polygon
from models import Cornfield, Agriculture, Manure, HistoryCornfield, CornfieldManure
from random import choice
from glineenc import encode_pairs
from datetime import date, datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.views import login as login_user
from django.contrib.auth import REDIRECT_FIELD_NAME
from form import AuthenticationForm1, FormHistoryCornfield, FormAgriculture, FormManure, AddField
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def database_add_part_too():
    #agriculture = [u'пшеница', u'рожь', u'овёс', u'ячмень', u'сахарная свёкла', u'подсолнечник', u'рапс', u'капуста', u'морковь', u'огурцы', u'лук', u'свёкла', u'кукуруза']
    agriculture = {u'пшеница':'#FFA07A', u'рожь':'#DC143C', u'овёс':'#B22222', u'ячмень':'#FF69B4', u'сахарная свёкла':'#C71585',
                   u'подсолнечник':'#FF6347', u'рапс':'#DB7093', u'капуста':'#FF69B4', u'морковь':'#FFB6C1', u'огурцы':'#FA8072',
                   u'лук':'#FFD700', u'свёкла':'#FFA500', u'кукуруза':'#FFC0CB'}
    for agro in agriculture:
        a = Agriculture(name_agriculture = agro, color_agriculture = agriculture[agro])
        a.save()
    manures =[u'сульфат аммония', u'аммиачная селитра', u'мочевина', u'суперфосфат', u'преципитат', u'хлористый калий']
    for manure in manures:
        m = Manure(name_manure = manure, field_manure = Cornfield.objects.filter(pk = choice(range(59, 150)))[0])
        m.save()

    for cornfield_ in Cornfield.objects.values('pk'):
        for year_ in range(2000, 2013):
            print choice(agriculture.keys())
            agriculture_name_ = Agriculture.objects.filter(name_agriculture = choice(agriculture.keys()))[0]
            fallout_ = str(choice(range(400, 1000, 30)))
            h = HistoryCornfield(cornfield = Cornfield.objects.filter(pk = cornfield_['pk'])[0], year = year_, agriculture_name =agriculture_name_,
                prolificness = choice(range(200, 400, 10)), fallout = fallout_)
            h.save()
    return "OK"


@csrf_exempt
@login_required
def map_view(request):

    #database_add_part_too()
    #database_add()
    #print "OK"

    """
    ds = DataSource(os.path.join(MEDIA_ROOT, 'ag_fields.kml'))
    layer = ds[0]
    geometry = []
    for feat in layer:
        geom = feat.geom
        new_line = []
        for line in geom:
            new_point = []
            for point in line:
                new_point.append(Point(point[0],point[1]))
            new_point.append(new_point[0])
            new_line = LinearRing(new_point)
        geometry.append(Polygon(new_line))

    polygones = MultiPolygon(geometry)

    gpoly = []
        for polygone in polygones:
            geos_poly = GEOSGeometry(fromstr(str(polygone)))
            gpoly.append(GPolygon(geos_poly).points.replace('GLatLng', 'google.maps.LatLng'))
        gpoly = '[%s]' % ','.join(gpoly)
    """

    """
    Отображение полигонов в template
    """
    """#--рабочий вариант
    for field in cornfield:
        agriculture_color = agriculture[field.agriculture_name]
        for polygone in field.mpoly:
                #geos_poly = GEOSGeometry(fromstr(str(polygone)))
                gpoly.append(GPolygon(polygone).points.replace('GLatLng', 'google.maps.LatLng'))
        attribute_poly.append((agriculture_color, field.name_field, field.area, field.agriculture_name))
    gpoly = '[%s]' % ','.join(gpoly)
    attribute_polys = '%s' % ';'.join(["%s,%s,%s,%s" % (color.encode('ascii'), name.encode('ascii'), area, agriculture_name) for color, name, area, agriculture_name in attribute_poly ])
    """

    today = date.today().year
    cornfield = HistoryCornfield.objects.filter(year = today, cornfield__use_user = request.user.pk)
    attribute_poly =[]
    epoly = []
    first_point = ''
    if cornfield.count() < Cornfield.objects.filter(use_user = request.user.pk).count():
        cornfield_without_history = Cornfield.objects.filter(use_user = request.user.pk)
        for field in cornfield:
            cornfield_without_history.exclude(pk = field.cornfield.pk)



        if cornfield_without_history.count()>0:
            first_point = '%s,%s'%(cornfield_without_history[0].mpoly[0][0][0][1], cornfield_without_history[0].mpoly[0][0][0][0])
        for field in cornfield_without_history:
            epoly.append((field.mpoly_coding_paths,  field.mpoly_coding_levels))
            attribute_poly.append(("#ffffff", field.name_field, field.area, u"поле под паром", field.pk))
        attribute_polys = '%s' % ';'.join(["%s,%s,%s,%s,%s" % (color.encode('ascii'), name.encode('ascii'), area, agriculture_name, pk) for color, name, area, agriculture_name, pk in attribute_poly ])
        #epoly = simplejson.dumps(epoly)



    if cornfield.count() >0:
        first_point = '%s,%s'%(cornfield[0].cornfield.mpoly[0][0][0][1], cornfield[0].cornfield.mpoly[0][0][0][0])
    for field in cornfield:
            epoly.append((field.cornfield.mpoly_coding_paths,  field.cornfield.mpoly_coding_levels))
            attribute_poly.append((field.agriculture_name.color_agriculture, field.cornfield.name_field, field.cornfield.area, field.agriculture_name.name_agriculture, field.cornfield.pk))
    attribute_polys = '%s' % ';'.join(["%s,%s,%s,%s,%s" % (color.encode('ascii'), name.encode('ascii'), area, agriculture_name, pk) for color, name, area, agriculture_name, pk in attribute_poly ])
    epoly = simplejson.dumps(epoly)

    form_history = FormHistoryCornfield()
    form_agriculture = FormAgriculture()
    form_manure = FormManure()
    form_add_field = AddField()

    return render_to_response('map_view.html', {'points':epoly, 'attribute_poly': attribute_polys, 'first_point': first_point, 'form_add_field':form_add_field,
                              'form_history':form_history, 'form_agriculture':form_agriculture, 'form_manure':form_manure}, context_instance=RequestContext(request))



@csrf_exempt
@login_required
def database_add(request):
    """
    Загрузка координат из *.kml в БД
    """
    #Кооординаты Cornfield

    if request.method == 'POST':
            form = AddField(request.POST, request.FILES)
            if form.is_valid():
                all_geometry = Cornfield.objects.filter(use_user = request.user)

                #fname = 'KML/' + request.FILES['append_field'].name[:-4] + "_" + str(request.user) + "_" + datetime.now().strftime("%d_%m_%Y_%H.%M.%S") + ".kml"
                fname = 'KML/' + str(request.user) + "_" + datetime.now().strftime("%d_%m_%Y_%H.%M.%S") + ".kml"
                f = open(os.path.join(MEDIA_ROOT, fname), 'wb+')
                for chunk in request.FILES['append_field'].chunks():
                       f.write(chunk)
                f.close()
                try:
                    ds = DataSource(os.path.join(MEDIA_ROOT, fname))
                    #ds = DataSource(os.path.join(MEDIA_ROOT, 'ag_fields3.kml'))
                    layer = ds[0]
                    i = 0
                    for feat in layer:

                      geom = feat.geom
                      #print geom
                      if geom:
                        new_line = []
                        for line in geom:
                            new_point = []
                            for point in line:
                                new_point.append(Point(point[0],point[1]))
                            new_point.append(new_point[0])
                            new_line = LinearRing(new_point)
                            if not new_line.ring:
                                new_point.append(new_point[0])
                                new_line = LinearRing(new_point)
                        name = "e%d"%i
                        poly = Polygon(new_line)
                        polygon_equals = True
                        for geom in all_geometry:
                            if poly.equals_exact(geom.mpoly[0], 0.001):
                                polygon_equals = False
                                break
                        if polygon_equals:
                            c = Cornfield(use_user = request.user, name_field=name, area = round(poly.area*1000000,2), mpoly = MultiPolygon(poly),
                                mpoly_coding_paths = encode_pairs(new_line)[0], mpoly_coding_levels = encode_pairs(new_line)[1])
                            c.save()
                            i+=1
                except:
                    pass


                return redirect('show_map')

@csrf_exempt
@login_required
def history_view(request, crop_id):
    if request.method == 'POST':
        history = HistoryCornfield.objects.filter(cornfield__pk = crop_id).order_by('year')
        history_table = ['%s,%s,%s,%s,%s'%(h.year, h.agriculture_name.name_agriculture, h.prolificness, h.fallout, ", ".join("%s" % unicode(m.manure_name.name_manure) for m in CornfieldManure.objects.filter(field_manure = h))) for h in history] #request.POST
        response = simplejson.dumps(history_table)
        if request.is_ajax():
            return HttpResponse(response, content_type="application/javascript")
        else:
            return HttpResponse(response)


@csrf_exempt
@login_required
def history_add(request):
    if request.method == 'POST':
        form_history = FormHistoryCornfield(request.POST)
        if form_history.is_valid():
            history_object = HistoryCornfield.objects.filter(year = request.POST['year'], cornfield_id = request.POST['cornfield'])
            if len(history_object)>0 and (len(request.POST['change'])< 3):
                response = simplejson.dumps({'success': 'True', 'change': 'True'})
            elif len(history_object)>0 and (len(request.POST['change'])>= 3):
                form_history = FormHistoryCornfield(request.POST, instance=history_object[0])
                form_history.save()
                if request.POST['manure']:
                               h = HistoryCornfield.objects.get(year = request.POST['year'], cornfield_id = request.POST['cornfield'])
                               manure_object = CornfieldManure.objects.filter(manure_name = request.POST['manure'], field_manure = h)
                               if len(manure_object)>0:
                                   m = CornfieldManure(pk = manure_object[0].pk, manure_name = Manure.objects.filter(pk = request.POST['manure'])[0], field_manure = h)
                                   m.save()
                               else:
                                   m = CornfieldManure(manure_name = Manure.objects.filter(pk = request.POST['manure'])[0], field_manure = h)
                                   m.save()
                response = simplejson.dumps({'success': 'True','change': 'False', 'name_history': 'True', 'color': Agriculture.objects.get(pk = request.POST['agriculture_name']).color_agriculture})
            else:
                form_history.save()
                if request.POST['manure']:
                               h = HistoryCornfield.objects.get(year = request.POST['year'], cornfield_id = request.POST['cornfield'])
                               manure_object = CornfieldManure.objects.filter(manure_name = request.POST['manure'], field_manure = h)
                               if len(manure_object)>0:
                                   m = CornfieldManure(pk = manure_object[0].pk, manure_name = Manure.objects.filter(pk = request.POST['manure'])[0], field_manure = h)
                                   m.save()
                               else:
                                   m = CornfieldManure(manure_name = Manure.objects.filter(pk = request.POST['manure'])[0], field_manure = h)
                                   m.save()
                response = simplejson.dumps({'success': 'True', 'name_history': 'True', 'color': Agriculture.objects.get(pk = request.POST['agriculture_name']).color_agriculture})
        else:
            response = simplejson.dumps({'success': 'False'})
        if request.is_ajax():
            if response.find('"success": "False"') >= 0:
                response = {}
                for k in form_history.errors:
                    response[k] = unicode(form_history.errors[k][0])
                response = simplejson.dumps({'response': response, 'success': 'False', 'name_history': 'False'})
            return HttpResponse(response, content_type="application/javascript")
        else:
            return HttpResponse(response)

@csrf_exempt
@login_required
def agriculture_add(request):
    if request.method == 'POST':
        form_agriculture = FormAgriculture(request.POST)
        if form_agriculture.is_valid():
            agriculture_object = Agriculture.objects.filter(name_agriculture = request.POST['name_agriculture'])
            if len(agriculture_object)>0 and (len(request.POST['change'])< 3):
                response = simplejson.dumps({'success': 'True', 'change': 'True'})
            elif len(agriculture_object)>0 and (len(request.POST['change'])>= 3):
                form_agriculture = FormAgriculture(request.POST, instance=agriculture_object[0])
                form_agriculture.save()
                response = simplejson.dumps({'success': 'True','change': 'False'})
            else:
                form_agriculture.save()
                response = simplejson.dumps({'success': 'True','name_agriculture': request.POST['name_agriculture']})
        else:
            response = simplejson.dumps({'success': 'False'})
        if request.is_ajax():
            if response.find('False') > 0:
                response = {}
                for k in form_agriculture.errors:
                    response[k] = unicode(form_agriculture.errors[k][0])
                response = simplejson.dumps({'response': response, 'success': 'False', 'name_agriculture': 'False'})
            return HttpResponse(response, content_type="application/javascript")
        else:
            return HttpResponse(response)


@csrf_exempt
@login_required
def manure_add(request):
    if request.method == 'POST':
        form_manure = FormManure(request.POST)
        if form_manure.is_valid():
            manure_object = Manure.objects.filter(name_manure = request.POST['name_manure'])
            if len(manure_object)>0 and (len(request.POST['change'])< 3):
                response = simplejson.dumps({'success': 'True', 'change': 'True'})
            elif len(manure_object)>0 and (len(request.POST['change'])>= 3):
                form_manure = FormManure(request.POST, instance=manure_object[0])
                form_manure.save()
                response = simplejson.dumps({'success': 'True','change': 'False'})
            else:
                form_manure.save()
                response = simplejson.dumps({'success': 'True','name_manure': request.POST['name_manure']})
        else:
            response = simplejson.dumps({'success': 'False'})
        if request.is_ajax():
            if response.find('False') > 0:
                response = {}
                for k in form_manure.errors:
                    response[k] = unicode(form_manure.errors[k][0])
                response = simplejson.dumps({'response': response, 'success': 'False', 'name_manure': 'False'})
            return HttpResponse(response, content_type="application/javascript")
        else:
            return HttpResponse(response)


def login(request):
    return login_user(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm1)




