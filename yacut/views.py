from string import ascii_letters, digits
from random import choices
from http import HTTPStatus

from flask import redirect, url_for, flash, render_template

from . import app, db
from .forms import LinkForm
from .models import URLMap
from .constants import SHORT_URL_DEFAULT_LENGHT


def get_unique_short_id(
        chars=ascii_letters + digits,
        size=SHORT_URL_DEFAULT_LENGHT
):
    while True:
        short_id = ''.join(choices(chars, k=size))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        flash(url_for('short_view', short=short, _external=True))

    return render_template('index.html', form=form), HTTPStatus.OK


@app.route('/<string:short>')
def short_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
