from utils.base import *

#        
# Локализация 
#

def localize(root, point):
    # Проверка на то, что точка геометрически лежит в этом дереве
    if not contains(root.bounds, point):
        return None

    current = root
    while True:
        # Понимаем в какой четверти текущего узла лежит точка
        qt = quarter_by(current.bounds, point)
        child = current.children[qt]
        if (not child.simple()) and contains(child.bounds, point):
            # Точка также лежит в интересном ребенке - спускаемся ниже по дереву
            current = child
        else:    
            return current

#        
# Вставка
#

def compressed_by(bounds, a, b):
    # Получаем рамки интересного квадрата по точкам, которые он содержит
    # Полученный квадрат является одной из под-четвертей исходного квадрата
    a_qt = quarter_by(bounds, a)
    b_qt = quarter_by(bounds, b)
    if a_qt is b_qt:
        # bounds задают неинтерсный квадрат, значит его квадрат в его под-четверти - интересный
        return compressed_by(quarter_bounds(bounds, a_qt), a, b)
    return bounds, a_qt, b_qt
    
def add(node, point, bounds):
    # Добавляем точку в простой узел
    if not node.simple():
        return
    if node.data == None:
        # Узел не содержит точку - просто добавим
        node.data = point
    else:
        if node.data == point:
            return
        # Узел содержит точку - создадим интересный квадрат по 2 точкам
        compressed_bounds, qt_p1, qt_p2 = compressed_by(bounds, node.data, point)
        # Инициализируем необходимые для хранения интресного квадрата поля
        node.bounds = compressed_bounds
        node.children = {}
        for qt in Quarter:
            node.children[qt] = Node(quarter_bounds(node.bounds, qt), None, None)
        node.children[qt_p1].data = node.data
        node.children[qt_p2].data = point
        node.data = None

def combine(node, point, bounds):
    # Создаем новый интересный квадрат по непростому узлу и точке
    compressed_bounds, qt_point, qt_node = compressed_by(bounds, point, (node.bounds[1], node.bounds[3]))
    new_node = Node(compressed_bounds, {}, None)
    for qt in Quarter:
        if qt == qt_point:
            new_node.children[qt] = Node(None, None, point)
        elif qt == qt_node:
            new_node.children[qt] = node
        else:
            new_node.children[qt] = Node(None, None, None)
    return new_node
        
def insertInternal(tree, point, node):
    qt = quarter_by(node.bounds, point)
    child = node.children[qt]
    if child.simple():
        # Добавляем точку в простой узел
        add(child, point, quarter_bounds(node.bounds, qt))
        # После этого узел может перестать быть простым, и уже будет содержать интересный квадрат
        if not child.simple():
            tree.ref[child.bounds] = child     # Обновим ref
    else:
        # В узле уже лежит ссылка на интересный квадрат
        # Надо создать новый квадрат, который будет содержить текущий квадрат и новую точку
        new_child = combine(child, point, quarter_bounds(node.bounds, qt))
        node.children[qt] = new_child          # Вставим в дерево
        tree.ref[new_child.bounds] = new_child # Обновим ref


#
# Удаление
#
        
def replace_with(node, other):
    # Перевещиваем узлы
    node.data = other.data
    node.bounds = other.bounds
    node.children = other.children        
        
def removeInternal(tree, point, node):
    qt = quarter_by(node.bounds, point)
    child = node.children[qt]
    if child.simple():
        # Проверяем лежит ли point в этом узле
        if child.data is not None and child.data == point:
            child.data = None
            # После удаления точки, квадрат, соотвествующий node, мог стать неинтересным
            if node == tree.root:
                # Корень по определению интересный
                return
            become_simple = True
            non_empty_child = None
            for child in node.children.values():
                if not child.empty():
                    if non_empty_child is None:
                        non_empty_child = child
                    else:
                        become_simple = False
                        break
            if become_simple:
                del tree.ref[node.bounds]           # Обновим ref
                replace_with(node, non_empty_child) # Удалим из дерева
