from utils.base import *

#
# Сжатое квадродерево
#

#        
# Локализация
#

def cqtree_localize(root, point):
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
        
def cqtree_insertInternal(tree, point, node):
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
        
def cqtree_removeInternal(tree, point, node):
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

                
#
# Структура
#
        
class CQTree:
    """Реализация сжатого квадродерева"""
    
    def __init__(self, bounds, localize_fun=None, insert_fun=None, remove_fun=None):
        root_children = {}
        self.root = Node(bounds, root_children)
        for qt in Quarter:
            root_children[qt] = Node(quarter_bounds(bounds, qt), None, None)
        # Ассоциативный массив из интересных квадратов в содержащие их узлы
        self.ref = {bounds: self.root}
        self.localize_fun = localize_fun if localize_fun is not None else cqtree_localize
        self.insert_fun = insert_fun if insert_fun is not None else cqtree_insertInternal
        self.remove_fun = remove_fun if remove_fun is not None else cqtree_removeInternal
    
    def localize(self, point, start=None):
        if start is None:
            start = self.root
        return self.localize_fun(start, point)
    
    def insert(self, point):
        node = self.localize(point)
        if node is None:
            return
        self.insertInternal(point, node)
        
    def insertInternal(self, point, node):
        self.insert_fun(self, point, node)

    def remove(self, point):
        node = self.localize(point)
        if node is None:
            return
        self.removeInternal(point, node)

    def removeInternal(self, point, node):
        self.remove_fun(self, point, node)
    
    def toggle(self, point):
        node = self.localize(point)
        if self.exists_in(point, node):
            self.removeInternal(point, node)
        else:
            self.insertInternal(point, node)
    
    def exists_in(self, point, node):
        for child in node.children.values():
            if child.simple() and child.data == point:
                return True
        return False
    
    def empty(self):
        for root_child in self.root.children.values():
            if not root_child.empty():
                return False
        return True

#
# Skip-квадродерево
#

#
# Вставка
#

def sqtree_insert(tree, point):
    if len(tree.levels) > 0:
        # Локализация в последнем уровне
        level_index = len(tree.levels) - 1
        level = tree.levels[level_index]
        node = level.localize(point)
        nodes = [node]
        # Поуровневая локализация
        while level_index != 0:
            level_index -= 1
            level = tree.levels[level_index]
            # Используем результат предыдущей локализации
            new_node = level.ref[nodes[-1].bounds]
            nodes.append(level.localize(point, new_node))
        nodes.reverse()
    else:
        nodes = []
    
    #Добавляем точку
    level_index = 0
    while True:
        if level_index < len(tree.levels):
            # Вставляем точку в ноду, полученную при локализации
            node = nodes[level_index]
            level = tree.levels[level_index]
            level.insertInternal(point, node)
            if rnd_bool():
                # Переходим на уровень выше
                level_index += 1
            else:
                return
        else:
            # Создаем новый уровень, который будет содержать только добавленную вершину
            new_level = tree.new_level()
            tree.levels.append(new_level)
            new_level.insert(point)
            return
        
#
# Удаление
#

def sqtree_remove(tree, point):
    if len(tree.levels) > 0:
        # Локализация в последнем уровне
        level_index = len(tree.levels) - 1
        level = tree.levels[level_index]
        node = level.localize(point)
        bounds = node.bounds
        # Удаляем точку с уровня
        level.removeInternal(point, node)
        # Поуровневая локализация
        while level_index != 0:
            level_index -= 1
            level = tree.levels[level_index]
            # Используя результат предыдущей локализации, делаем локализацию на текущем уровне
            node = level.localize(point, level.ref[bounds])
            bounds = node.bounds
            # Удаляем точку с уровня
            level.removeInternal(point, node)
           
        if tree.levels[-1].empty():
            # Удаляем последний пустой уровень
            del tree.levels[-1]
