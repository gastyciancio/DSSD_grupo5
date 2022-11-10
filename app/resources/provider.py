from flask import render_template, request
from flask.helpers import flash

from app.helpers.providers_maker_api import get_providers_by_data, reserve_providers_by_data

def index():
    return render_template('providers/reserve_providers.html')

def search():
    response = get_providers_by_data(request.form)
    materiales_sin_prov = response['metadata']['materiales_sin_proveedor']
    materiales_con_prov = response['suppliers']
    return render_template('providers/reserve_providers.html',materiales_con_prov=materiales_con_prov, materiales_sin_prov=materiales_sin_prov)


def reserve():
    response = reserve_providers_by_data(request.form)
    flash(response)
    return render_template('providers/reserve_providers.html')