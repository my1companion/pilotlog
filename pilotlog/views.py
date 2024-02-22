import re
import json
import csv
import decimal
from ast import literal_eval
from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pilotlog.models import Aircraft
from pilotlog.models import Flight
from .forms import JSONImportForm

def import_json_view(request):
    form = JSONImportForm()
    if request.method == 'POST':
        form = JSONImportForm(request.POST, request.FILES)
        if form.is_valid():
            request_file = request.FILES['json_file']
            request_file_str = request_file.read().decode('utf-8')
            request_file_str = re.sub("'(\w+)':", r'"\1":', request_file_str, flags=re.MULTILINE)
            data = json.loads(request_file_str.replace("\\", ""), object_hook=literal_eval, object_pairs_hook=OrderedDict)
            for item in data:
                         
             if item['table']=='Aircraft':
                imported_data = Aircraft(
                    AircraftID=item['guid'],
                    EquipmentType='',
                    TypeCode='',
                    Year='',
                    Make=item['meta']['Make'],
                    Model=item['meta']['Model'],
                    Category=item['meta']['Category'],
                    Class=item['meta']['Class'],
                    GearType='',
                    EngineType='',
                    Complex=item['meta']['Complex'],
                    HighPerformance=item['meta']['HighPerf'],
                    Pressurized='',
                    TAA=''
                )
                imported_data.save()

             if item['table']=='Flight':
                item['meta'].setdefault('inNIGHT', '')
                imported_data_flight = Flight(
                    Date=item['meta']['DateUTC'],
                    FlightID=item['guid'],
                    From='',
                    To='',
                    Route=item['meta']['Route'],
                    TimeOut='',
                    TimeOff='',
                    TimeOn='',
                    Timein='',
                    OnDuty='',
                    OffDuty='',
                    TotalTime='',
                    minPICUS=item['meta']['minPICUS'],
                    SIC='',
                    inNight=item['meta']['inNIGHT'],
                    Solo='',
                    CrossCountry=''
                )
                imported_data_flight.save()

            return redirect('export_csv')

    return render(request, 'pilotlog/import_json.html', {'form': form})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['AircraftID','EquipmentType','TypeCode','Year','Make','Model','Category','Class','GearType','EngineType','Complex','HighPerformance','Pressurized','TAA'])

    for item in Aircraft.objects.all():
        writer.writerow([
            item.AircraftID,
            item.EquipmentType,
            item.TypeCode,
            item.Year,
            item.Make,
            item.Model,
            item.Category,
            item.Class,
            item.GearType,
            item.EngineType,
            item.Complex,
            item.HighPerformance,
            item.Pressurized,
            item.TAA,
        ])

    return response

def export_csv_flight(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['DateUTC','FlightCode','From','To','Route','TimeOut','TimeOff','TimeOn','Timein','OnDuty','OffDuty','TotalTime','minPICUS','SIC','inNight','Solo','CrossCountry'])

    for item in Flight.objects.all():
        writer.writerow([
            item.Date,
            item.FlightID,
            item.From,
            item.To,
            item.Route,
            item.TimeOut,
            item.TimeOff,
            item.TimeOn,
            item.Timein,
            item.OnDuty,
            item.OffDuty,
            item.TotalTime,
            item.minPicus,
            item.SIC,
            item.inNight,
            item.Solo,
            item.CrossCountry,
        ])

    return response