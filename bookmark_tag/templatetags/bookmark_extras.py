from django import template

register = template.Library()

@register.filter(name='join_on_attr')
def join_on_attr(obj_list, attr_name, join_val):
    join_str = ''

    for i, obj in obj_list:
        if obj.attr_name:
            join_str += obj.attr_name
        
        if (not (i == len(obj_list))):
            join_str += join_val
    
    return join_str
