@register.filter
def add_classname(field, classname):
attrs = field.field.widget.attrs
attrs["class"] = attrs.get("class", "") + " " + classname
attrs["autocomplete"] = "off"
return field.as_widget(attrs=attrs)

---

<div class="input-group mr-2">
                                {{ form.username|add_classname:"custom-select custom-select-sm" }}
                            </div>
