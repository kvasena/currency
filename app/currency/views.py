from django.db import IntegrityError
from django.http import HttpResponse
from models import Currency, Multiplier
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .algorithm import find_sequence

import json
import csv


def __response(status=200, **kwargs):
    return HttpResponse(json.dumps(kwargs, cls=DjangoJSONEncoder), content_type='application/json', status=status)


def currencies(request):
    if request.method == 'GET':
        kwargs = {}
        for c in Currency.objects.all():
            kwargs[c.name] = {}
            for multiplier in Multiplier.objects.filter(Q(currency_first=c.pk) | Q(currency_second=c.pk)):
                kwargs[c.name].update(multiplier.get_row())
        return __response(**kwargs)
    else:
        return __response(405)


def currency(request, name):
    if request.method == 'GET':
        c = get_object_or_404(Currency, name=name)
        kwargs = {c.name: {}}
        for multiplier in Multiplier.objects.filter(Q(currency_first=c.pk) | Q(currency_second=c.pk)):
            kwargs[c.name].update(multiplier.get_row())

        return __response(**kwargs)
    elif request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        currency_first, _ = Currency.objects.get_or_create(name=name)
        for cur, rate in body.iteritems():
            currency_second, _ = Currency.objects.get_or_create(name=cur)
            if Multiplier.objects.filter(currency_first=currency_first.pk,
                                         currency_second=currency_second.pk).exists():
                return __response(409)
            obj, _ = Currency.objects.get_or_create(name=name)
            obj, _ = Currency.objects.get_or_create(name=cur)
            Multiplier.objects.create(currency_first=currency_first, currency_second=currency_second, rate=rate)

        return __response()
    elif request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        currency_first = get_object_or_404(Currency, name=name)
        for cur, rate in body.iteritems():
            currency_second = get_object_or_404(Currency, name=cur)
            multiplier = Multiplier.objects.get(currency_first=currency_first, currency_second=currency_second)
            multiplier.rate = rate
            multiplier.save()

        return __response()
    else:
        return __response(405)


def sequence(request):
    if request.method == 'GET':
        try:
            add_data()
            return __response(**find_sequence())
        except MyError as e:
            return __response(**{'msg': e.msg})
    else:
        return __response(405)


def add_data():
    Currency.objects.all().delete()
    with open('start.csv', 'rU') as file:
        matrix = [row for row in csv.reader(file)]
    for array in matrix:
        currency_from, time = Currency.objects.get_or_create(name=array[0].strip())
        currency_to, time2 = Currency.objects.get_or_create(name=array[1].strip())
        try:
            Multiplier.objects.get_or_create(currency_first=currency_from, currency_second=currency_to, rate=array[2])
        except IntegrityError:
            raise MyError('Already exists')


class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg



