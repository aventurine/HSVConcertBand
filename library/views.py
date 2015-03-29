import json
from django.http import HttpResponse
from django.shortcuts import render
from library.models import Composition, Composer

from xlrd import open_workbook

POSSIBLE_PARTS = ['c_piccolo', 'd_flat_piccolo', 'flute_1', 'flute_2', 'flute_3', 'oboe_1', 'oboe_2', 'e_flat_clarinet', 'solo_b_flat_clarinet', 'b_flat_clarinet_1', 'b_flat_clarinet_2', 'b_flat_clarinet_3', 'b_flat_clarinet_4', 'alto_clarinet', 'bass_clarinet', 'contrabass_clarinet', 'bassoon_1', 'bassoon_2', 'soprano_saxophone', 'alto_saxophone_1', 'alto_saxophone_2', 'tenor_saxophone', 'baritone_saxophone', 'solo_cornet', 'cornet_1', 'cornet_2', 'cornet_3', 'trumpet_1', 'trumpet_2', 'trumpet_3', 'f_horn_1', 'f_horn_2', 'f_horn_3', 'f_horn_4', 'e_flat_horn_1', 'e_flat_horn_2', 'e_flat_horn_3', 'e_flat_horn_4', 'trombone_1', 'trombone_2', 'trombone_3', 'baritone_tc', 'baritone_bc', 'bass_tuba', 'string_bass', 'timpani', 'mallets', 'percussion_1', 'percussion_2', 'percussion_other']

def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

def index(request):
    return render(request, 'index.html')

def get_compositions(request):
    def mkview(album):
        return {
            'ID': album.id,
            'TITLE': album.title,
            'TYPE': album.style,
            'COMPOSER': album.composer.name,
            'ARRANGER': album.arranger,
            'DUR': album.duration,
            'CR DATE': album.copyright_year,
            'LAST DIST': album.date_last_passed_out,
            'LAST PERF': album.date_last_performed,
            'PUBLISHER': album.publisher
        }

    compositions = Composition.objects.all()
    return json_response([mkview(c) for c in compositions])

def post_compositions(request):

    for file in request.FILES:
        # this version of the ctor takes a path name
        # you can also use a file

        Workbook = open_workbook( file_contents=request.FILES[file].read() )
        Worksheet = Workbook.sheet_by_index( 0 )

        # this caches the headers
        Headers = []
        for col in range(Worksheet.ncols):
            Headers.append( Worksheet.cell(0,col).value )

        # create the dictionaries and add them to the data
        for row in range(1,Worksheet.nrows):
            composition = Composition()
            for col in range(Worksheet.ncols):
                if Headers[col] == 'TITLE':
                    composition.title = Worksheet.cell(row,col).value
                elif Headers[col] == 'TYPE':
                    composition.style = Worksheet.cell(row,col).value
                elif Headers[col] == 'COMPOSER':
                    composer_name = Worksheet.cell(row,col).value
                    composer, _ = Composer.objects.get_or_create(name=composer_name)
                    composition.composer = composer
                elif Headers[col] == 'ARRANGER':
                    composition.arranger = Worksheet.cell(row,col).value
                elif Headers[col] == 'DUR.':
                    composition.duration = Worksheet.cell(row,col).value
                elif Headers[col] == 'CR DATE':
                    composition.copyright_year = Worksheet.cell(row,col).value
                elif Headers[col] == 'LAST DIST':
                    composition.date_last_passed_out = Worksheet.cell(row,col).value
                elif Headers[col] == 'LAST PERF':
                    composition.date_last_performed = Worksheet.cell(row,col).value
                elif Headers[col] == 'PUBLISHER':
                    composition.publisher = Worksheet.cell(row,col).value
                elif Headers[col] == 'NOTES':
                    composition.comments = Worksheet.cell(row,col).value
            if composition.composer is None:
                composition.composer = Composer.objects.create(name="unknown")
            composition.save()

    return HttpResponse('OK')

def compositions(request):
    if request.method == 'GET':
        return get_compositions(request)
    elif request.method == 'POST':
        return post_compositions(request)

def composition_details(request, pk):
    def mkview(album):
        def filter_part(part):
            return getattr(album, part) != None and getattr(album, part) != ""
        parts = [{'count': getattr(album, part),
                  'name': part }
                    for part in POSSIBLE_PARTS if filter_part(part)]
        return {
            'PARTS': sorted(parts, key=lambda part: part['name']),
            'TITLE': album.title,
            'COMPOSER': album.composer.name,
            'ARRANGER': album.arranger,
            'PUBLISHER': album.publisher,
            'COPYRIGHT_YEAR': album.copyright_year,
            'STYLE': album.style,
            'DURATION': album.duration,
            'DATE_LAST_PASSED_OUT': album.date_last_passed_out,
            'DATE_LAST_PERFORMED': album.date_last_performed,
            'COMMENTS': album.comments,
            'FULL_SCORE': album.full_score,
            'CONDENSED_SCORE': album.condensed_score
        }
    return json_response(mkview(Composition.objects.get(id=pk)))
