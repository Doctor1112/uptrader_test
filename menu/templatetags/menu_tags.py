from django import template
from menu.models import MenuItem
from django.utils.html import format_html

register = template.Library()

def build_menu(menu_items):
    low_lvl = ""
    cur_lvl = ""
    low_lvl_parent_id = None
    prev_item = None
    for item in menu_items:
        if prev_item and item.parent_id != prev_item.parent_id:
            low_lvl_parent_id = prev_item.parent_id
            low_lvl = cur_lvl
            cur_lvl = ""
        if low_lvl_parent_id:
            if item.id != low_lvl_parent_id:
                cur_lvl += f'<li><a href="{item.get_absolute_url()}">{item.content}</a></li>'
            else:
                cur_lvl += f'<li><a href="{item.get_absolute_url()}">{item.content}</a></li><ul>' + low_lvl + "</ul>"
                low_lvl_parent_id = None
        else:
            cur_lvl += f'<li><a href="{item.get_absolute_url()}">{item.content}</a></li>'
        prev_item = item

    return format_html(f"<ul>{cur_lvl}</ul>")

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_pk):
    request = context["request"]
    menu_item_pk = request.GET.get("menu_item_pk")

    if menu_item_pk is None:
        menu_items = MenuItem.objects.filter(menu_id=menu_pk, parent=None)
    else:
        menu_item_pk = int(menu_item_pk)
        menu_items = list(MenuItem.objects.raw(f"""WITH RECURSIVE MenuAncestors AS (
    SELECT id, content, parent_id
    FROM menu_menuitem
    WHERE id = {menu_item_pk}

    UNION ALL

    SELECT m.id, m.content, m.parent_id
    FROM menu_menuitem m
    INNER JOIN MenuAncestors ma ON m.id = ma.parent_id
    )
    SELECT mm.id, mm.content, mm.parent_id FROM MenuAncestors m
    inner join menu_menuitem mm on m.id = mm.parent_id
	
	union ALL
	
	select id, content, parent_id from menu_menuitem
	where parent_id is null and menu_id = "{menu_pk}"
    order by mm.parent_id desc, mm.id asc
    """))
    

    return build_menu(menu_items)