import django_filters
from .models import Cat


class CatFilter(django_filters.FilterSet):
    color = django_filters.MultipleChoiceFilter(
        choices=[
            ('red', 'Красный'),
            ('black', 'Чёрный'),
            ('white', 'Белый'),
            ('gray', 'Серый'),
            ('orange', 'Оранжевый'),
            ('bisque', 'Бежевый'),
            ('saddlebrown', 'Коричневый'),
        ]
    )

    class Meta:
        model = Cat
        fields = ['color']