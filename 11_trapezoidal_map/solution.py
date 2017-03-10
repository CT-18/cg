from TMapClasses import *

import numpy as np
from cg import Point, turn
from enum import Enum


def intersect_segment(s: Segment, left_tr: Trapezoid):
    """Возвращает список трапецоидов, которые пересекает отрезок"""
    while not left_tr.is_rightmost():
        # Поиск остановится, если у трапецоида нет соседей справа или конец отрезка внутри трапецоида.
        if s.q <= left_tr.rightp:
            break
        else:
            # Надо понять, в какого соседа пойдет отрезок. Считаем поворот rightp относительно прямой s
            sign = turn(left_tr.rightp, s.p, s.q)
            if sign == 1:
                # Отрезок пересекает нижнего соседа
                left_tr = left_tr.rightnb[1]
            elif sign == -1:
                # Отрезок пересекает верхнего соседа
                left_tr = left_tr.rightnb[0]
            else:  # sign == 0
                # Отрезок касается вершины внутренней точкой, такой отрезок не подходит под условие!
                raise Exception('Error')
            assert left_tr is not None
            yield left_tr


def localize(tmap: TrapezoidMap, s: Segment):
    """Возвращает список трапецоидов, в которые попала точка"""
    return tmap.root.visit(s)


def update_node_links(old_node, new_node):
    # Подвешиваем новый узел в дерево вместо старого
    for parent in old_node.links:
        if parent.left == old_node:
            parent.left = new_node
        elif parent.right == old_node:
            parent.right = new_node
        else:
            raise Exception('Error')


def update_left_nb(old_tr, new_tr, indexes):
    # Обновим левых соседей у трапецоида
    for i in indexes:
        if old_tr.leftnb[i] is not None:
            # Трапецоиды могут быть соседними только по 1 ссылке, проверяем это
            if old_tr.leftnb[i].rightnb[0] == old_tr:
                j = 0
            elif old_tr.leftnb[i].rightnb[1] == old_tr:
                j = 1
            else:
                raise Exception('Error')
            old_tr.leftnb[i].rightnb[j] = new_tr


def update_right_nb(old_tr, new_tr, indexes):
    # Обновим правых соседей у трапецоида
    for i in indexes:
        if old_tr.rightnb[i] is not None:
            # Трапецоиды могут быть соседними только по 1 ссылке, проверяем это
            if old_tr.rightnb[i].leftnb[0] == old_tr:
                j = 0
            elif old_tr.rightnb[i].leftnb[1] == old_tr:
                j = 1
            else:
                raise Exception('Error')
            old_tr.rightnb[i].leftnb[j] = new_tr


def insert_segment(tmap: TrapezoidMap, s, parent):
    """Метод для вставки отрезка, попавшего целиком в трапецоид"""
    # Создаем 4 новых трапецоида
    up = Trapezoid(parent.top, s, s.p, s.q)
    down = Trapezoid(s, parent.bottom, s.p, s.q)
    left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
    right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
    # Запоминаем их
    tmap.tr += [up, down, left, right]
    # Расставляем соседей
    up.leftnb = [left, None]
    up.rightnb = [right, None]
    down.leftnb = [None, left]
    down.rightnb = [None, right]
    left.leftnb = parent.leftnb
    left.rightnb = [up, down]
    right.rightnb = parent.rightnb
    right.leftnb = [up, down]
    # У соседей parent-a теперь новые трапецоиды
    update_left_nb(parent, left, [0, 1])
    update_right_nb(parent, right, [0, 1])
    # Строим новое поддерево"
    up_node = TrapezoidNode(up)
    down_node = TrapezoidNode(down)
    left_node = TrapezoidNode(left)
    right_node = TrapezoidNode(right)
    segment_node = YNode(s, up_node, down_node)
    q_node = XNode(s.q, segment_node, right_node)
    p_node = XNode(s.p, left_node, q_node)
    # Обновим ссылки между узлами и трапецоидами
    up_node.links.append(segment_node)
    down_node.links.append(segment_node)
    left_node.links.append(p_node)
    right_node.links.append(q_node)
    update_node_links(parent.node, p_node)
    # Удалим старый трапецоид
    tmap.tr.remove(parent)
    # Обновим корень, если это первое добавление
    if type(tmap.root) == type(up_node):
        tmap.root = p_node


def left_insert(tmap, s, parent):
    """Метод для вставки отрезка в самый левый трапецоид. Отрезок пересекает как минимум 2 трапецоида"""
    assert s.p != parent.rightp  # отрезок не должен был попасть в этот трапецоид
    up = Trapezoid(parent.top, s, s.p, parent.rightp)
    down = Trapezoid(s, parent.bottom, s.p, parent.rightp)  # одна из rightp ещё не известна
    left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
    tmap.tr += [up, down, left]
    up.leftnb = [left, None]
    down.leftnb = [None, left]
    left.leftnb = parent.leftnb
    left.rightnb = [up, down]
    update_left_nb(parent, left, [0, 1])
    sign = turn(parent.rightp, s.p, s.q)
    if sign == 1:
        # точка выше отрезка, нижний трапецоид не закончен
        down.rightp = None
        up.rightnb = [parent.rightnb[0], None]  # нижний не известен
        update_right_nb(parent, up, [0])
    elif sign == -1:
        # точка ниже отрезка, верхний трапецоид не закончен
        up.rightp = None
        down.rightnb = [None, parent.rightnb[1]]
        update_right_nb(parent, down, [1])
    else:
        # отрезок попал в rightp
        assert parent.rightp == s.q
        up.rightnb = [parent.rightnb[0], None]
        down.rightnb = [None, parent.rightnb[1]]
        if parent.rightnb[0] is not None:
            assert parent.rightnb[0].leftnb[0] == parent
            parent.rightnb[0].leftnb[0] = up
        if parent.rightnb[1] is not None:
            assert parent.rightnb[1].leftnb[1] == parent
            parent.rightnb[1].leftnb[1] = down
    # Строим новое поддерево
    up_node = TrapezoidNode(up)
    down_node = TrapezoidNode(down)
    left_node = TrapezoidNode(left)
    segment_node = YNode(s, up_node, down_node)
    p_node = XNode(s.p, left_node, segment_node)
    # Обновим ссылки между узлами и трапецоидами
    up_node.links.append(segment_node)
    down_node.links.append(segment_node)
    left_node.links.append(p_node)
    update_node_links(parent.node, p_node)
    tmap.tr.remove(parent)
    return [up, down]  # будем возвращать сначала верхний, а затем нижний


def segment_insert(tmap, s, parent, left_tr):
    """Вставка отрезка в очередной трапецоид, возможно последний"""
    # Либо верхний, либо нижний трапецоид недоделан, либо начало отрезка совпало с точкой другого отрезка
    # Определим это по левым соседям трапецоида
    if left_tr[0] is not None and left_tr[0].rightp is None:
        assert left_tr[1].rightp is not None and parent.leftp == left_tr[1].rightp
        # новый трапецоид - нижний; верхний недоделан
        up = left_tr[0]
        down = Trapezoid(s, parent.bottom, parent.leftp, parent.rightp)
        tmap.tr += [down]
        left_tr[1].rightnb[0] = down
        down.leftnb = [left_tr[1], parent.leftnb[1]]
        update_left_nb(parent, down, [1])
        up_node = up.node
        down_node = TrapezoidNode(down)
    elif left_tr[1] is not None and left_tr[1].rightp is None:
        assert left_tr[0].rightp is not None and parent.leftp == left_tr[0].rightp
        # новый трапецоид - верхний, а нижний недоделан
        down = left_tr[1]
        up = Trapezoid(parent.top, s, parent.leftp, parent.rightp)
        tmap.tr += [up]
        left_tr[0].rightnb[1] = up
        up.leftnb = [parent.leftnb[0], left_tr[0]]
        update_left_nb(parent, up, [0])
        up_node = TrapezoidNode(up)
        down_node = down.node
    else:
        # s.p совпадает с leftp
        assert parent.leftp == s.p
        up = Trapezoid(parent.top, s, parent.leftp, parent.rightp)
        down = Trapezoid(s, parent.bottom, parent.leftp, parent.rightp)
        tmap.tr += [up, down]
        if parent.leftnb[0] is not None:
            up.leftnb = [parent.leftnb[0], None]
            update_left_nb(parent, up, [0])
        else:
            up.leftnb = [None, None]
        if parent.leftnb[1] is not None:
            down.leftnb = [None, parent.leftnb[1]]
            update_left_nb(parent, down, [1])
        else:
            down.leftnb = [None, None]
        up_node = TrapezoidNode(up)
        down_node = TrapezoidNode(down)
    # Надо понять, верхний или нижний трапецоид продлевать
    assert not parent.is_rightmost()  # не должны здесь оказаться
    sign = turn(parent.rightp, s.p, s.q)
    if sign == 1:
        # точка выше отрезка, нижний трапецоид не закончен
        down.rightp = None
        up.rightp = parent.rightp  # если в прошлый раз не закончили его
        up.rightnb = [parent.rightnb[0], None]
        update_right_nb(parent, up, [0])
    elif sign == -1:
        # точка ниже отрезка, верхний трапецоид не закончен
        up.rightp = None
        down.rightp = parent.rightp  # если в прошлый раз не закончили его
        down.rightnb = [None, parent.rightnb[1]]
        update_right_nb(parent, down, [1])
    else:
        # отрезок попал в вершину, значит это последний трапецоид
        assert parent.rightp == s.q
        up.rightnb = [parent.rightnb[0], None]
        down.rightnb = [None, parent.rightnb[1]]
        up.rightp = parent.rightp
        down.rightp = parent.rightp
    segment_node = YNode(s, up_node, down_node)
    up_node.links.append(segment_node)
    down_node.links.append(segment_node)
    update_node_links(parent.node, segment_node)
    tmap.tr.remove(parent)
    return [up, down]


def right_insert(tmap, s, parent, left_tr):
    """Вставка отрезка в последний трапецоид"""
    assert s.q != parent.leftp  # такой трапецоид не мог тут оказаться
    if (not parent.is_rightmost()) and s.q == parent.rightp:
        # правый конец отрезка попал в rightp
        # значит это последний трапецоид, новые создавать не надо
        left_tr = segment_insert(tmap, s, parent, left_tr)
        if parent.rightnb[0] is not None:
            assert parent.rightnb[0].leftnb[0] == parent
            parent.rightnb[0].leftnb[0] = left_tr[0]
        if parent.rightnb[1] is not None:
            assert parent.rightnb[1].leftnb[1] == parent
            parent.rightnb[1].leftnb[1] = left_tr[1]
        return
    if left_tr[0] is not None and left_tr[0].rightp is None:
        assert parent.leftp == left_tr[1].rightp
        # новый трапецоид - нижний; верхний продолжается
        up = left_tr[0]
        up.rightp = s.q
        down = Trapezoid(s, parent.bottom, parent.leftp, s.q)
        tmap.tr += [down]
        left_tr[1].rightnb[0] = down
        down.leftnb = [left_tr[1], parent.leftnb[1]]
        update_left_nb(parent, down, [1])
        up_node = up.node
        down_node = TrapezoidNode(down)
    elif left_tr[1] is not None and left_tr[1].rightp is None:
        assert parent.leftp == left_tr[0].rightp
        # новый трапецоид - верхний, а нижний продолжается
        down = left_tr[1]
        down.rightp = s.q
        up = Trapezoid(parent.top, s, parent.leftp, s.q)
        tmap.tr += [up]
        left_tr[0].rightnb[1] = up
        up.leftnb = [parent.leftnb[0], left_tr[0]]
        update_left_nb(parent, up, [0])
        up_node = TrapezoidNode(up)
        down_node = down.node
    else:
        # Отрезок целиком попал в трапецоид, его левая точка совпала с leftp, а правая с rightp нет
        assert s.p == parent.leftp
        assert parent.is_rightmost() or s.q != parent.rightp
        for i in range(2):
            if parent.leftnb[i] is not None:
                assert left_tr[i] == parent.leftnb[i]
        up = Trapezoid(parent.top, s, parent.leftp, s.q)
        down = Trapezoid(s, parent.bottom, parent.leftp, s.q)
        tmap.tr += [up, down]
        up.leftnb = [left_tr[0], None]
        down.leftnb = [None, left_tr[1]]
        if left_tr[0] is not None:
            left_tr[0].rightnb[0] = up
        if left_tr[1] is not None:
            left_tr[1].rightnb[1] = down
        up_node = TrapezoidNode(up)
        down_node = TrapezoidNode(down)
    right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
    tmap.tr += [right]
    right.leftnb = [up, down]
    up.rightnb = [right, None]
    down.rightnb = [None, right]
    right.rightnb = parent.rightnb
    update_right_nb(parent, right, [0, 1])
    # Строим новое поддерево
    right_node = TrapezoidNode(right)
    segment_node = YNode(s, up_node, down_node)
    q_node = XNode(s.q, segment_node, right_node)
    # Обновим ссылки между узлами и трапецоидами
    up_node.links.append(segment_node)
    down_node.links.append(segment_node)
    right_node.links.append(q_node)
    update_node_links(parent.node, q_node)
    tmap.tr.remove(parent)
    return


def insert(tmap: TrapezoidMap, s: Segment):
    """Вставка отрезка в трапецоидную карту"""
    tmap.segments.append(s)
    # Локализуемся, чтобы найти первый трапецоид
    first_tr = localize(tmap, s)
    if first_tr.is_leftmost() or first_tr.leftp < s.p:
        # Нужно создать левый трапецоид
        if first_tr.is_rightmost() or s.q < first_tr.rightp:
            # Простой случай: вставка отрезка целиком в один трапецоид
            insert_segment(tmap, s, first_tr)
            return
        else:
            # Вставим отрезок в самый левый трапецоид
            undone_left_tr = left_insert(tmap, s, first_tr)
            if s.q == first_tr.rightp:
                # s.q попала на другую вершину, значит уже закончили вставку
                return
    else:
        # Левая вершина отрезка попала на вершину другого отерзка
        assert s.p == first_tr.leftp
        undone_left_tr = first_tr.leftnb
        if not first_tr.is_rightmost() and first_tr.rightp < s.q:
            # Вставим отрезок, если трапецоид не последний
            undone_left_tr = segment_insert(tmap, s, first_tr, undone_left_tr)
    tr_list = intersect_segment(s, first_tr)
    last_tr = first_tr
    first_tr = next(tr_list, None)
    while first_tr is not None:
        last_tr = next(tr_list, None)
        if last_tr is None:  # Получили последний трапецоид
            last_tr, first_tr = first_tr, last_tr
        else:  # Вставляем очередной трапецоид
            undone_left_tr = segment_insert(tmap, s, first_tr, undone_left_tr)
            first_tr = last_tr
    # Вставляем последний трапецоид
    right_insert(tmap, s, last_tr, undone_left_tr)
