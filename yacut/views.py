from flask import render_template, redirect, abort

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap

INDEX_HTML = 'index.html'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template(INDEX_HTML, form=form)
    url_map = URLMap.create_link(form.original_link.data, form.custom_id.data)
    short_id = URLMap.full_short_id(url_map.short)
    return render_template(INDEX_HTML, form=form, short_link=short_id)


@app.route('/<short>')
def get_url_map(short):
    url = URLMap.get(short)
    if url:
        return redirect(url.original, 302)
    abort(404)
