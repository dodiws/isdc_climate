from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from django.template import RequestContext

from django.utils.translation import ugettext as _
from graphos.renderers import flot, gchart

from graphos.sources.simple import SimpleDataSource
import datetime, re
from graphos.renderers import flot, gchart
from .models import (
    AfgMettClim1KmChelsaBioclim,
    AfgMettClim1KmWorldclimBioclim2050Rpc26,
    AfgMettClim1KmWorldclimBioclim2050Rpc45,
    AfgMettClim1KmWorldclimBioclim2050Rpc85,
    AfgMettClim1KmWorldclimBioclim2070Rpc26,
    AfgMettClim1KmWorldclimBioclim2070Rpc45,
    AfgMettClim1KmWorldclimBioclim2070Rpc85,
    AfgMettClimperc1KmChelsaPrec,
    AfgMettClimtemp1KmChelsaTempavg,
    AfgMettClimtemp1KmChelsaTempmax,
    AfgMettClimtemp1KmChelsaTempmin    ,
)
from django.shortcuts import render_to_response

import json
from geonode.utils import include_section, none_to_zero, query_to_dicts, RawSQL_nogroupby, ComboChart
from geodb.views import (
    get_nc_file_from_ftp,
    getCommonVillageData,
    )

gchart.ComboChart = ComboChart

def getClimateVillage(request):
    template = './climateinfo.html'
    village = request.GET["v"]
    context_dict = getCommonVillageData(village)
    currentdate = datetime.datetime.utcnow()
    year = currentdate.strftime("%Y")
    month = currentdate.strftime("%m")
    day = currentdate.strftime("%d")

    climatePrec = get_object_or_404(AfgMettClimperc1KmChelsaPrec, vuid=village)
    climateTempAVG = get_object_or_404(AfgMettClimtemp1KmChelsaTempavg, vuid=village)
    climateTempMAX = get_object_or_404(AfgMettClimtemp1KmChelsaTempmax, vuid=village)
    climateTempMIN = get_object_or_404(AfgMettClimtemp1KmChelsaTempmin, vuid=village)

    tempData = []
    tempData.append([_('Month'),_('Precipitation'),_('Max Temp'),_('Avg Temp'),_('Min Temp')])
    tempData.append([_('Jan'),climatePrec.january,climateTempMAX.january,climateTempAVG.january,climateTempMIN.january])
    tempData.append([_('Feb'),climatePrec.february,climateTempMAX.february,climateTempAVG.february,climateTempMIN.february])
    tempData.append([_('Mar'),climatePrec.march,climateTempMAX.march,climateTempAVG.march,climateTempMIN.march])
    tempData.append([_('Apr'),climatePrec.april,climateTempMAX.april,climateTempAVG.april,climateTempMIN.april])
    tempData.append([_('May'),climatePrec.may,climateTempMAX.may,climateTempAVG.may,climateTempMIN.may])
    tempData.append([_('Jun'),climatePrec.june,climateTempMAX.june,climateTempAVG.june,climateTempMIN.june])
    tempData.append([_('Jul'),climatePrec.july,climateTempMAX.july,climateTempAVG.july,climateTempMIN.july])
    tempData.append([_('Aug'),climatePrec.august,climateTempMAX.august,climateTempAVG.august,climateTempMIN.august])
    tempData.append([_('Sep'),climatePrec.september,climateTempMAX.september,climateTempAVG.september,climateTempMIN.september])
    tempData.append([_('Oct'),climatePrec.october,climateTempMAX.october,climateTempAVG.october,climateTempMIN.october])
    tempData.append([_('Nov'),climatePrec.november,climateTempMAX.november,climateTempAVG.november,climateTempMIN.november])
    tempData.append([_('Dec'),climatePrec.december,climateTempMAX.december,climateTempAVG.december,climateTempMIN.december])

    context_dict['temperature_line_chart'] = gchart.ComboChart(
        SimpleDataSource(data=tempData), 
        html_id="line_chart1", 
        options={
            'title': _("Current Climate"), 
            'width': 500,
            'height': 400, 
            'legend': 'bottom', 
            # 'curveType': 'function', 
            'seriesType': 'bars',
            'colors': ['#3366cc', 'red', 'black', 'blue'],
            'chartArea': {'top':10, 'bottom':90, 'left':50, 'right':50},
            'vAxes': { 
                0:{'format': u'# \u00b0C'},
                1:{'format':"# mm", 'viewWindow':{'min':0}} 
            },
            'series': {
                0: {'targetAxisIndex':1,'type':'bars'},
                1: {'targetAxisIndex':0,'type':'line'},
                2: {'targetAxisIndex':0,'type':'line'},
                3: {'targetAxisIndex':0,'type':'line'},
            },
        })

    climateBioClim = get_object_or_404(AfgMettClim1KmChelsaBioclim, vuid=village)
    climateBioClim2050Rpc26 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2050Rpc26, vuid=village)
    climateBioClim2050Rpc45 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2050Rpc45, vuid=village)
    climateBioClim2050Rpc85 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2050Rpc85, vuid=village)
    climateBioClim2070Rpc26 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2070Rpc26, vuid=village)
    climateBioClim2070Rpc45 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2070Rpc45, vuid=village)
    climateBioClim2070Rpc85 = get_object_or_404(AfgMettClim1KmWorldclimBioclim2070Rpc85, vuid=village)

    climDataTemp = []
    climDataTemp.append([
        'State',
        'Annual Mean Temperature',
        'Mean Diurnal Range',
        'Isothermality',
        'Temperature Seasonality',
        'Max Temperature of Warmest Month',
        'Min Temperature of Coldest Month',
        'Temperature Annual Range',
        'Mean Temperature of Wettest Quarter',
        'Mean Temperature of Driest Quarter',
        'Mean Temperature of Warmest Quarter',
        'Mean Temperature of Coldest Quarter',
        {'type': 'string', 'role': 'style'}
    ])

    climDataTemp.append([
        _('Current Climate'),
        climateBioClim.bio1,
        climateBioClim.bio2,
        climateBioClim.bio3,
        climateBioClim.bio4,
        climateBioClim.bio5,
        climateBioClim.bio6,
        climateBioClim.bio7,
        climateBioClim.bio8,
        climateBioClim.bio9,
        climateBioClim.bio10,
        climateBioClim.bio11,
        'color: #3366cc'
    ])
    climDataTemp.append([
        _('RPC 26\n'),
        climateBioClim2050Rpc26.bio1,
        climateBioClim2050Rpc26.bio2,
        climateBioClim2050Rpc26.bio3*10,
        climateBioClim2050Rpc26.bio4,
        climateBioClim2050Rpc26.bio5,
        climateBioClim2050Rpc26.bio6,
        climateBioClim2050Rpc26.bio7,
        climateBioClim2050Rpc26.bio8,
        climateBioClim2050Rpc26.bio9,
        climateBioClim2050Rpc26.bio10,
        climateBioClim2050Rpc26.bio11,
        'color: #ffff03'
    ])
    climDataTemp.append([
        _('RPC 45\n2050'),
        climateBioClim2050Rpc45.bio1,
        climateBioClim2050Rpc45.bio2,
        climateBioClim2050Rpc45.bio3*10,
        climateBioClim2050Rpc45.bio4,
        climateBioClim2050Rpc45.bio5,
        climateBioClim2050Rpc45.bio6,
        climateBioClim2050Rpc45.bio7,
        climateBioClim2050Rpc45.bio8,
        climateBioClim2050Rpc45.bio9,
        climateBioClim2050Rpc45.bio10,
        climateBioClim2050Rpc45.bio11,
        'color: #ffc003'
    ])
    climDataTemp.append([
        _('RPC 85\n'),
        climateBioClim2050Rpc85.bio1,
        climateBioClim2050Rpc85.bio2,
        climateBioClim2050Rpc85.bio3*10,
        climateBioClim2050Rpc85.bio4,
        climateBioClim2050Rpc85.bio5,
        climateBioClim2050Rpc85.bio6,
        climateBioClim2050Rpc85.bio7,
        climateBioClim2050Rpc85.bio8,
        climateBioClim2050Rpc85.bio9,
        climateBioClim2050Rpc85.bio10,
        climateBioClim2050Rpc85.bio11,
        'color: #ff0303'
    ])
    climDataTemp.append([
        _('RPC 26\n'),
        climateBioClim2070Rpc26.bio1,
        climateBioClim2070Rpc26.bio2,
        climateBioClim2070Rpc26.bio3*10,
        climateBioClim2070Rpc26.bio4,
        climateBioClim2070Rpc26.bio5,
        climateBioClim2070Rpc26.bio6,
        climateBioClim2070Rpc26.bio7,
        climateBioClim2070Rpc26.bio8,
        climateBioClim2070Rpc26.bio9,
        climateBioClim2070Rpc26.bio10,
        climateBioClim2070Rpc26.bio11,
        'color: #ffff03'
    ])
    climDataTemp.append([
        _('RPC 45\n2070'),
        climateBioClim2070Rpc45.bio1,
        climateBioClim2070Rpc45.bio2,
        climateBioClim2070Rpc45.bio3*10,
        climateBioClim2070Rpc45.bio4,
        climateBioClim2070Rpc45.bio5,
        climateBioClim2070Rpc45.bio6,
        climateBioClim2070Rpc45.bio7,
        climateBioClim2070Rpc45.bio8,
        climateBioClim2070Rpc45.bio9,
        climateBioClim2070Rpc45.bio10,
        climateBioClim2070Rpc45.bio11,
        'color: #ffc003'
    ])
    climDataTemp.append([
        _('RPC 85\n'),
        climateBioClim2070Rpc85.bio1,
        climateBioClim2070Rpc85.bio2,
        climateBioClim2070Rpc85.bio3*10,
        climateBioClim2070Rpc85.bio4,
        climateBioClim2070Rpc85.bio5,
        climateBioClim2070Rpc85.bio6,
        climateBioClim2070Rpc85.bio7,
        climateBioClim2070Rpc85.bio8,
        climateBioClim2070Rpc85.bio9,
        climateBioClim2070Rpc85.bio10,
        climateBioClim2070Rpc85.bio11,
        'color: #ff0303'
    ])
    context_dict['climatechange_temp_data'] = json.dumps(climDataTemp)


    climDataPrec = []
    climDataPrec.append([
        'State',
        'Annual Precipitation',
        'Precipitation of Wettest Month',
        'Precipitation of Driest Month',
        'Precipitation Seasonality',
        'Precipitation of Wettest Quarter',
        'Precipitation of Driest Quarter',
        'Precipitation of Warmest Quarter',
        'Precipitation of Coldest Quarter',
        {'type': 'string', 'role': 'style'}
    ])

    climDataPrec.append([
        _('Current Climate'),
        climateBioClim.bio12,
        climateBioClim.bio13,
        climateBioClim.bio14,
        climateBioClim.bio15,
        climateBioClim.bio16,
        climateBioClim.bio17,
        climateBioClim.bio18,
        climateBioClim.bio19,
        'color: #3366cc'
    ])
    climDataPrec.append([
        _('RPC 26\n'),
        climateBioClim2050Rpc26.bio12,
        climateBioClim2050Rpc26.bio13,
        climateBioClim2050Rpc26.bio14,
        climateBioClim2050Rpc26.bio15,
        climateBioClim2050Rpc26.bio16,
        climateBioClim2050Rpc26.bio17,
        climateBioClim2050Rpc26.bio18,
        climateBioClim2050Rpc26.bio19,
        'color: #ffff03'
    ])
    climDataPrec.append([
        _('RPC 45\n2050'),
        climateBioClim2050Rpc45.bio12,
        climateBioClim2050Rpc45.bio13,
        climateBioClim2050Rpc45.bio14,
        climateBioClim2050Rpc45.bio15,
        climateBioClim2050Rpc45.bio16,
        climateBioClim2050Rpc45.bio17,
        climateBioClim2050Rpc45.bio18,
        climateBioClim2050Rpc45.bio19,
        'color: #ffc003'
    ])
    climDataPrec.append([
        _('RPC 85\n'),
        climateBioClim2050Rpc85.bio12,
        climateBioClim2050Rpc85.bio13,
        climateBioClim2050Rpc85.bio14,
        climateBioClim2050Rpc85.bio15,
        climateBioClim2050Rpc85.bio16,
        climateBioClim2050Rpc85.bio17,
        climateBioClim2050Rpc85.bio18,
        climateBioClim2050Rpc85.bio19,
        'color: #ff0303'
    ])
    climDataPrec.append([
        _('RPC 26\n'),
        climateBioClim2070Rpc26.bio12,
        climateBioClim2070Rpc26.bio13,
        climateBioClim2070Rpc26.bio14,
        climateBioClim2070Rpc26.bio15,
        climateBioClim2070Rpc26.bio16,
        climateBioClim2070Rpc26.bio17,
        climateBioClim2070Rpc26.bio18,
        climateBioClim2070Rpc26.bio19,
        'color: #ffff03'
    ])
    climDataPrec.append([
        _('RPC 45\n2070'),
        climateBioClim2070Rpc45.bio12,
        climateBioClim2070Rpc45.bio13,
        climateBioClim2070Rpc45.bio14,
        climateBioClim2070Rpc45.bio15,
        climateBioClim2070Rpc45.bio16,
        climateBioClim2070Rpc45.bio17,
        climateBioClim2070Rpc45.bio18,
        climateBioClim2070Rpc45.bio19,
        'color: #ffc003'
    ])
    climDataPrec.append([
        _('RPC 85\n'),
        climateBioClim2070Rpc85.bio12,
        climateBioClim2070Rpc85.bio13,
        climateBioClim2070Rpc85.bio14,
        climateBioClim2070Rpc85.bio15,
        climateBioClim2070Rpc85.bio16,
        climateBioClim2070Rpc85.bio17,
        climateBioClim2070Rpc85.bio18,
        climateBioClim2070Rpc85.bio19,
        'color: #ff0303'
    ])

    context_dict['climatechange_prec_data'] = json.dumps(climDataPrec)

    context_dict.pop('position')
    return render_to_response(template,
                                  RequestContext(request, context_dict))
