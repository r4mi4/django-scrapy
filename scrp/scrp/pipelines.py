# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django.forms import model_to_dict
from itemadapter import ItemAdapter


def item_to_model(item):
    model_class = getattr(item, 'django_model')
    if not model_class:
        raise TypeError("Item is not a `DjangoItem` or is misconfigured")
    return item.instance


def get_or_create(model):
    model_class = type(model)
    created = False
    try:
        # We have no unique identifier at the moment; use the company for now.
        obj = model_class.objects.get(company=model.company)
    except model_class.DoesNotExist:
        created = True
        obj = model  # DjangoItem created a model for us.

    return (obj, created)


def update_model(destination, source, commit=True):
    pk = destination.pk

    source_dict = model_to_dict(source)
    for (key, value) in source_dict.items():
        setattr(destination, key, value)
    setattr(destination, 'pk', pk)
    if commit:
        destination.save()

    return destination


class ScrpPipeline:
    """
    Saves Item to the database
    """

    def process_item(self, item, spider):
        try:
            item_model = item_to_model(item)
        except TypeError:
            return item

        model, created = get_or_create(item_model)

        update_model(model, item_model)
        return item
