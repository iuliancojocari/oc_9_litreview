from django import template
register = template.Library()

@register.filter
def add_classname(field, classname):
    attrs = field.field.widget.attrs
    attrs["class"] = attrs.get("class", "") + " " + classname
    attrs["autocomplete"] = "off"
    return field.as_widget(attrs=attrs)