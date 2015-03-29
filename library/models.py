from django.conf import settings
from django.contrib import admin
from django.db import models


class Composer(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

def player_field(name, help_text=None):
    return models.CharField(max_length=60, verbose_name=name, blank=True, null=True, help_text=help_text)

def strfmt_date(date):
    if date is None:
        return ""
    else:
        return date.strftime(settings.DATE_FMT)

class Composition(models.Model):

    title = models.CharField(max_length=60)
    composer = models.ForeignKey(Composer)
    arranger = models.CharField(max_length=60, blank=True)
    publisher = models.CharField(max_length=60, blank=True)
    copyright_year = models.CharField(max_length=60, verbose_name ='Copyright year', blank=True, null=True)
    style = models.CharField(max_length=60, blank=True)

    duration = models.CharField(max_length=60, blank=True)
    date_last_passed_out = models.DateField(blank=True, null=True)
    date_last_performed = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True)

    full_score = models.CharField(max_length=60, blank=True)
    condensed_score = models.CharField(max_length=60, blank=True)

    c_piccolo = player_field('C Piccolo')
    d_flat_piccolo = player_field('D-flat Piccolo')
    flute_1 = player_field('Flute 1')
    flute_2 = player_field('Flute 2')
    flute_3 = player_field('Flute 3')
    oboe_1 = player_field('Oboe 1')
    oboe_2 = player_field('Oboe 2')
    e_flat_clarinet = player_field('E-flat clarinet')
    solo_b_flat_clarinet = player_field('Solo B-flat clarinet')
    b_flat_clarinet_1 = player_field('B-flat clarinet 1')
    b_flat_clarinet_2 = player_field('B-flat clarinet 2')
    b_flat_clarinet_3 = player_field('B-flat clarinet 3')
    b_flat_clarinet_4 = player_field('B-flat clarinet 4')
    alto_clarinet = player_field('Alto clarinet')
    bass_clarinet = player_field('Bass clarinet')
    contrabass_clarinet = player_field('Contrabass clarinet')
    bassoon_1 = player_field('Bassoon 1')
    bassoon_2 = player_field('Bassoon 2')
    soprano_saxophone = player_field('Soprano saxophone')
    alto_saxophone_1 = player_field('Alto saxophone 1')
    alto_saxophone_2 = player_field('Alto saxophone 2')
    tenor_saxophone = player_field('Tenor saxophone')
    baritone_saxophone = player_field('Baritone saxophone')
    solo_cornet = player_field('Solo Cornet')
    cornet_1 = player_field('Cornet 1')
    cornet_2 = player_field('Cornet 2')
    cornet_3 = player_field('Cornet 3')
    trumpet_1 = player_field('Trumpet 1')
    trumpet_2 = player_field('Trumpet 2')
    trumpet_3 = player_field('Trumpet 3')
    f_horn_1 = player_field('F horn 1')
    f_horn_2 = player_field('F horn 2')
    f_horn_3 = player_field('F horn 3')
    f_horn_4 = player_field('F horn 4')
    e_flat_horn_1 = player_field('E-flat horn 1')
    e_flat_horn_2 = player_field('E-flat horn 2')
    e_flat_horn_3 = player_field('E-flat horn 3')
    e_flat_horn_4 = player_field('E-flat horn 4')
    trombone_1 = player_field('Trombone 1')
    trombone_2 = player_field('Trombone 2')
    trombone_3 = player_field('Trombone 3')
    baritone_tc = player_field('Baritone TC')
    baritone_bc = player_field('Baritone BC')
    bass_tuba = player_field('Bass/Tuba')
    string_bass = player_field('String bass')
    timpani = player_field('Timpani')
    mallets = player_field('Mallets')
    percussion_1 = player_field('Percussion 1')
    percussion_2 = player_field('Percussion 2')
    percussion_other = player_field('Percussion other')

    def date_last_passed_out_strfmt(self):
        return strfmt_date(self.date_last_passed_out)

    def date_last_performed_strfmt(self):
        return strfmt_date(self.date_last_performed)

    def __str__(self):
        return '{} ({})'.format(self.title, self.composer.name)

admin.site.register(Composer)
admin.site.register(Composition)
