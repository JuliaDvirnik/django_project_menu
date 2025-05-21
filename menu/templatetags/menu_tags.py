from venv import logger
import sys
sys.stdout.reconfigure(encoding='utf-8')

from django import template
from django.template.loader import render_to_string
from ..models import Menu, MenuItem
from collections import defaultdict

register = template.Library()


# class MenuItemExt(MenuItem):
#     pass

@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context['request'] # зачем??
    current_path = request.path

    menu_items = MenuItem.objects.filter(menu__name=menu_name) #один запрос в базу
    # Без select_related:
    # SELECT * FROM
    # menu_menuitem
    # WHERE
    # menu_id = ?;
    #
    # С select_related('parent'):
    # SELECT *
    # FROM menu_menuitem
    # LEFT OUTER JOIN menu_menuitem
    # AS parent ON menu_menuitem.parent_id = parent.id
    # WHERE menu_menuitem.menu_id = ?;

    # select_related('parent') загружает сами объекты parent вместе с MenuItem
    # иначе Django лениво загружает ForeignKey, и для каждого .parent делает отдельный запрос, если ты не указал select_related.
    # без запроса можно получить только item.parent_id, но для этого тогда надо хранить словарь {item_id:item}
    # т.к. в find_active нам нужно получать родителя

    def build_tree(items): #сложность O(N) here find active element
        tree = []
        children_map = defaultdict(list)
        items_by_id = {}

        for item in items:
            items_by_id[item.id] = item
            item.visible = False  # ← инициализация
            if item.parent_id is None:
                tree.append(item)
            else:
                children_map[item.parent_id].append(item)
        for item in items:
            item.children_list = children_map.get(item.id, [])
        return tree, items_by_id

    def find_and_mark_active_branch(items, path, root_items):
        active_item = None
        for item in items:
            if item.get_url() == path:
                item.visible = True
                for child in item.children_list:
                    child.visible = True
                parent = items_by_id.get(item.parent_id)
                while parent:
                    parent.visible = True
                    for sibling in parent.children_list:
                        sibling.visible = True  # ← показываем всех детей родителя
                    parent = items_by_id.get(parent.parent_id)
                active_item = item  # это активный пункт
            elif item in root_items:
                item.visible = True
            result = find_and_mark_active_branch(item.children_list, path, root_items)
            if result:
                item.visible = True
                active_item = result
        return active_item

    root_items, items_by_id = build_tree(menu_items)
    active_item = find_and_mark_active_branch(root_items, current_path, root_items)
    # debug
    for item in menu_items:
        if item.visible:
            print('visible', item)
        else:
            print('not visible', item)
    # active_items = find_visible_items(root_items, current_path)
    #
    # def find_visible_items(items, path): #сложность O(N) (проход по всем пунктам)
    #     for item in items:
    #         if item.get_url() == path: #интересно как будет работать там где никак не задана ссылка
    #             return [item] + item.children_list
    #         branch = find_visible_items(item.children_list, path)
    #         if branch:
    #             return [item] + branch
    #     return []

    # def mark_visibility(items, branch):
    #     for item in items:
    #         item.visible = item in branch or item in (branch[0].children_list if branch else [])
    #         mark_visibility(item.children_list, branch)
    #
    # mark_visibility(root_items, active_branch)

    return {'root_items': root_items, 'active_item': active_item, 'request': request} # set of visible elements, dict of ind and child