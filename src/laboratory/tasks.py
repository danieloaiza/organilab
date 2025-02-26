from __future__ import absolute_import, unicode_literals

import importlib
import re

from click.core import F
from django.conf import settings


from laboratory.models import ShelfObject, Laboratory, PrecursorReport, InformScheduler, Furniture

from datetime import date

from .limit_shelfobject import send_email_limit_objs
from .task_utils import create_informsperiods

app = importlib.import_module(settings.CELERY_MODULE).app

def get_limited_shelf_objects(lab):
    return ShelfObject.objects.filter(in_where_laboratory=lab, quantity__lte=F('limit_quantity'))


@app.task
def notify_about_product_limit_reach():
    labs = Laboratory.objects.all()
    object_list=[]
    for lab in labs:
        for shelfobjects in get_limited_shelf_objects(lab):
                object_list.append(shelfobjects)
        send_email_limit_objs(lab,object_list, enqueued=False)
        object_list.clear()


@app.on_after_configure.connect
def setup_daily_tasks(sender, **kwargs):
    sender.add_periodic_task(
        2, notify_about_product_limit_reach.s(), name='notify')


@app.task()
def create_precursor_reports():
    day = date.today()
    for lab in Laboratory.objects.all():
        PrecursorReport.objects.create(
                month=day.month,
                year=day.year,
                laboratory=lab,
                consecutive=add_consecutive(lab)
            )


def add_consecutive(lab):
    report = PrecursorReport.objects.filter(laboratory=lab).last()
    consecutive = 1
    if report is not None:
        consecutive = int(report.consecutive)+1

    return consecutive


@app.task
def create_informs_based_on_period():
    informschedulerquery = InformScheduler.objects.filter(active=True)
    for informscheduler in informschedulerquery:
        create_informsperiods(informscheduler)

@app.task()
def remove_shelf_not_furniture():
    furnitures = Furniture.objects.all()
    for furniture in furnitures:
        obj_pks= re.findall(r'\d+', furniture.dataconfig)
        furniture.shelf_set.all().exclude(pk__in=obj_pks).delete()