from re import match
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return jsonify({'url': link.original}), HTTPStatus.OK

    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is not None:
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        if not match(
                r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$', data['url']):
            raise InvalidAPIUsage('Указан недопустимый URL')
        if not data.get('custom_id'):
            data['custom_id'] = get_unique_short_id()
        if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()

        return jsonify(url_map.to_dict()), HTTPStatus.CREATED

    raise InvalidAPIUsage('Отсутствует тело запроса')
