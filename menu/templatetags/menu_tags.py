from django import template
from ..models import MenuItem
from collections import defaultdict

register = template.Library()


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    menu_items = MenuItem.objects.filter(menu__name=menu_name)

    def build_tree(items):
        tree = []
        children_map = defaultdict(list)
        items_by_id = {}
        active_item = None
        for item in items:
            items_by_id[item.id] = item
            if normalize_path(item.get_url()) == normalize_path(current_path):
                active_item = item
            if item.parent_id is None:
                tree.append(item)
            else:
                children_map[item.parent_id].append(item)

        return tree, items_by_id, active_item, children_map

    def find_visible_items():
        visible_items = set()
        visible_items.update(root_items)
        visible_items.add(active_item)
        for child in dict_of_children.get(active_item.id, []):
            visible_items.add(child)
        parent = menu_items_by_id.get(active_item.parent_id)
        while parent:
            visible_items.add(parent)
            visible_items.update(dict_of_children.get(parent.id, []))
            parent = menu_items_by_id.get(parent.parent_id)
        return visible_items

    def normalize_path(path):
        return path.rstrip('/')

    root_items, menu_items_by_id, active_item, dict_of_children = build_tree(menu_items)
    print('active_item', active_item)
    print('dict_of_children', dict_of_children)
    visible_items = find_visible_items()

    return {'root_items': root_items, 'active_item': active_item, 'visible_items': visible_items, 'dict_of_children': dict_of_children, 'request': request}


# шаблонный парсер не понимает dict[key] в with и for
@register.filter
def get(d: dict, key):
    return d.get(key, [])