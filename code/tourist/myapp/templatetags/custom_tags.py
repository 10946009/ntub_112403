from django import template
register = template.Library()

#讓html可以抓到前一筆資料
@register.filter
def get_previous_item(data_list, current_index):
    try:
        return data_list[current_index - 1]
    except IndexError:
        return None
