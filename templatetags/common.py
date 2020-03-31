from django import template

register = template.Library()


@register.filter
def model_name(model):
    """
    {{ view.model|model_name }}
    """
    return model.__class__.__name__


@register.filter
def create_url(model):
    """
    {{view.model|create_url}}
    """
    app_label = model._meta.app_label
    model_name = model.__class__.__name__.lower()
    return app_label + ':' + model_name + '-create'


@register.filter
def list_url(model):
    """
    {{view.model|create_url}}
    """
    app_label = model._meta.app_label
    model_name = model.__class__.__name__.lower()
    return app_label + ':' + model_name + '-list'
