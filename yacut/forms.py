from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional,
                                ValidationError, Regexp, URL)

from .models import URLMap
from .constants import (SHORT_URL_MAX_LENGHT, SHORT_URL_MIN_LENGHT,
                        ORIGINAL_URL_MAX_LENGHT, ORIGINAL_URL_MIN_LENGHT,
                        PATTERN_SHORT_URL)


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            Length(ORIGINAL_URL_MIN_LENGHT, ORIGINAL_URL_MAX_LENGHT),
            DataRequired(message='Обязательное поле'),
            URL(require_tld=True, message='Некорректный URL')
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(SHORT_URL_MIN_LENGHT, SHORT_URL_MAX_LENGHT),
            Optional(),
            Regexp(PATTERN_SHORT_URL,
                   message='Можно использовать только [A-Za-z0-9]')
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')
