from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QCursor

class ResizeHandler:
    def __init__(self, window, margin=8):
        self.window = window
        self.margin = margin
        self.dragging = False
        self.drag_direction = None
        self.drag_start_pos = None
        self.drag_start_geometry = None

        self.window.setMouseTracking(True)
    
    def get_resize_direction(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.window.width(), self.window.height()
        
        if x <= self.margin and y <= self.margin:
            return 'top_left'
        elif x >= w - self.margin and y <= self.margin:
            return 'top_right'
        elif x <= self.margin and y >= h - self.margin:
            return 'bottom_left'
        elif x >= w - self.margin and y >= h - self.margin:
            return 'bottom_right'
        elif x <= self.margin:
            return 'left'
        elif x >= w - self.margin:
            return 'right'
        elif y <= self.margin:
            return 'top'
        elif y >= h - self.margin:
            return 'bottom'
        return None
    
    def direction_to_cursor(self, direction):
        """Преобразуем направление в курсор"""
        cursors = {
            'top_left': Qt.SizeFDiagCursor,
            'top_right': Qt.SizeBDiagCursor,
            'bottom_left': Qt.SizeBDiagCursor,
            'bottom_right': Qt.SizeFDiagCursor,
            'left': Qt.SizeHorCursor,
            'right': Qt.SizeHorCursor,
            'top': Qt.SizeVerCursor,
            'bottom': Qt.SizeVerCursor
        }
        return cursors.get(direction, Qt.ArrowCursor)

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_direction = self.get_resize_direction(event.pos())
            if self.drag_direction:
                self.dragging = True
                self.drag_start_pos = event.globalPos()
                self.drag_start_geometry = self.window.geometry()
                return True
        return False

    def mouse_move(self, event):
        if not self.dragging:
            # Меняем курсор при наведении
            direction = self.get_resize_direction(event.pos())
            cursor = self.direction_to_cursor(direction)
            self.window.setCursor(cursor)
        else:
            # Обрабатываем ресайз
            self.handle_resize(event.globalPos())
        return False

    def mouse_release(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.drag_direction = None
            self.window.setCursor(Qt.ArrowCursor)
            return True
        return False

    def handle_resize(self, global_pos):
        if not self.dragging or not self.drag_direction:
            return
            
        delta = global_pos - self.drag_start_pos
        new_geometry = QRect(self.drag_start_geometry)
        
        direction = self.drag_direction
        
        if 'left' in direction:
            new_geometry.setLeft(new_geometry.left() + delta.x())
        if 'right' in direction:
            new_geometry.setRight(new_geometry.right() + delta.x())
        if 'top' in direction:
            new_geometry.setTop(new_geometry.top() + delta.y())
        if 'bottom' in direction:
            new_geometry.setBottom(new_geometry.bottom() + delta.y())
        
        # Проверяем минимальный размер
        if new_geometry.width() >= self.window.minimumWidth() and new_geometry.height() >= self.window.minimumHeight():
            self.window.setGeometry(new_geometry)