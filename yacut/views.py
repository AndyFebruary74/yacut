from flask import render_template, redirect, abort

from yacut import app
from yacut.error_handlers import InvalidCreateObject
from yacut.forms import URLForm
from yacut.models import URLMap

INDEX_HTML = 'index.html'
INVALID_CREATE_OBJECT = 'Произошла ошибка при записи в базу данных'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template(INDEX_HTML, form=form)
    short_id = form.custom_id.data
    try:
        url_map = URLMap.create_link(form.original_link.data, short_id)
        short_id = URLMap.full_short_id(url_map.short)
    except InvalidCreateObject:
        raise InvalidCreateObject(INVALID_CREATE_OBJECT)
    return render_template(INDEX_HTML, form=form, short_link=short_id)


@app.route('/<short>')
def get_url_map(short):
    url = URLMap.get(short)
    if url:
        return redirect(url.original, 302)
    abort(404)
