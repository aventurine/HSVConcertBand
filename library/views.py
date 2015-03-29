import json
from django.http import HttpResponse
from django.shortcuts import render
from library.models import Composition


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
			'LAST DIST': album.date_last_passed_out_strfmt(),
			'LAST PERF': album.date_last_performed_strfmt(),
			'PUBLISHER': album.publisher
		}

	compositions = Composition.objects.all()
	return json_response([mkview(c) for c in compositions])

def compositions(request):
	if request.method == 'GET':
		return get_compositions(request)

def composition_details(request, pk):
    def mkview(album):
        def filter_part(part):
            return getattr(album, part) != None and getattr(album, part) != ""
        parts = [{'count': getattr(album, part),
                  'name': part }
                    for part in POSSIBLE_PARTS if filter_part(part)]
        return {
            'PARTS': parts,
            'TITLE': album.title,
            'COMPOSER': album.composer.name,
            'ARRANGER': album.arranger,
            'PUBLISHER': album.publisher,
            'COPYRIGHT_YEAR': album.copyright_year,
            'STYLE': album.style,
            'DURATION': album.duration,
            'DATE_LAST_PASSED_OUT': album.date_last_passed_out_strfmt(),
            'DATE_LAST_PERFORMED': album.date_last_performed_strfmt(),
            'COMMENTS': album.comments,
            'FULL_SCORE': album.full_score,
            'CONDENSED_SCORE': album.condensed_score
        }
    return json_response(mkview(Composition.objects.get(id=pk)))
