"""
Animations Helper Module
Provides reusable animation utilities for FactuNabo UI
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QRect, QTimer, QSequentialAnimationGroup, QParallelAnimationGroup
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget
from PySide6.QtGui import QPainter, QColor, QPainterPath
from PySide6.QtCore import Qt, QPointF
import math


class RippleEffect:
    """
    Ripple effect for buttons (Material Design inspired)
    Usage: ripple = RippleEffect(button, color)
           ripple.start(click_pos)
    """
    def __init__(self, widget, color=QColor(160, 191, 110, 100)):
        self.widget = widget
        self.color = color
        self.ripples = []
        self.widget.installEventFilter(self)
    
    def start(self, pos):
        """Start a ripple animation at the given position"""
        ripple = {
            'center': pos,
            'radius': 0,
            'max_radius': self._calculate_max_radius(pos),
            'opacity': 1.0
        }
        self.ripples.append(ripple)
        
        # Animate ripple expansion
        timer = QTimer(self.widget)
        timer.timeout.connect(lambda: self._animate_ripple(ripple, timer))
        timer.start(16)  # ~60 FPS
    
    def _calculate_max_radius(self, pos):
        """Calculate maximum ripple radius to cover entire widget"""
        corners = [
            QPointF(0, 0),
            QPointF(self.widget.width(), 0),
            QPointF(0, self.widget.height()),
            QPointF(self.widget.width(), self.widget.height())
        ]
        max_dist = 0
        for corner in corners:
            dx = corner.x() - pos.x()
            dy = corner.y() - pos.y()
            dist = math.sqrt(dx*dx + dy*dy)
            max_dist = max(max_dist, dist)
        return max_dist
    
    def _animate_ripple(self, ripple, timer):
        """Animate single ripple frame"""
        ripple['radius'] += ripple['max_radius'] / 25  # 400ms total
        ripple['opacity'] = max(0, 1.0 - (ripple['radius'] / ripple['max_radius']))
        
        if ripple['radius'] >= ripple['max_radius']:
            timer.stop()
            if ripple in self.ripples:
                self.ripples.remove(ripple)
        
        self.widget.update()
    
    def paint(self, painter):
        """Paint all active ripples"""
        for ripple in self.ripples:
            painter.setRenderHint(QPainter.Antialiasing)
            color = QColor(self.color)
            color.setAlphaF(ripple['opacity'])
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(ripple['center'], ripple['radius'], ripple['radius'])


class FadeAnimation:
    """
    Fade in/out animation for widgets
    Usage: FadeAnimation.fade_in(widget, duration=300)
    """
    @staticmethod
    def fade_in(widget, duration=300, on_finished=None):
        """Fade in widget from transparent to opaque"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        
        if on_finished:
            anim.finished.connect(on_finished)
        
        anim.start()
        return anim
    
    @staticmethod
    def fade_out(widget, duration=300, on_finished=None):
        """Fade out widget from opaque to transparent"""
        effect = widget.graphicsEffect()
        if not effect:
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        
        if on_finished:
            anim.finished.connect(on_finished)
        
        anim.start()
        return anim


class SlideAnimation:
    """
    Slide animation for widgets
    Usage: SlideAnimation.slide_in(widget, direction='down')
    """
    @staticmethod
    def slide_in(widget, direction='down', distance=50, duration=300, on_finished=None):
        """Slide widget into view"""
        start_pos = widget.pos()
        
        if direction == 'down':
            offset = QPoint(0, -distance)
        elif direction == 'up':
            offset = QPoint(0, distance)
        elif direction == 'left':
            offset = QPoint(distance, 0)
        else:  # right
            offset = QPoint(-distance, 0)
        
        widget.move(start_pos + offset)
        
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setStartValue(start_pos + offset)
        anim.setEndValue(start_pos)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        
        if on_finished:
            anim.finished.connect(on_finished)
        
        anim.start()
        return anim
    
    @staticmethod
    def slide_out(widget, direction='up', distance=50, duration=300, on_finished=None):
        """Slide widget out of view"""
        start_pos = widget.pos()
        
        if direction == 'down':
            offset = QPoint(0, distance)
        elif direction == 'up':
            offset = QPoint(0, -distance)
        elif direction == 'left':
            offset = QPoint(-distance, 0)
        else:  # right
            offset = QPoint(distance, 0)
        
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setStartValue(start_pos)
        anim.setEndValue(start_pos + offset)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        
        if on_finished:
            anim.finished.connect(on_finished)
        
        anim.start()
        return anim


class StaggerAnimation:
    """
    Stagger animation for list items
    Usage: StaggerAnimation.animate_list(list_widget, items)
    """
    @staticmethod
    def animate_items(items, delay=50, duration=250):
        """Animate list of widgets with stagger effect"""
        animations = []
        for i, item in enumerate(items):
            # Fade in
            effect = QGraphicsOpacityEffect(item)
            item.setGraphicsEffect(effect)
            effect.setOpacity(0.0)
            
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(duration)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            
            # Delay start based on index
            QTimer.singleShot(i * delay, anim.start)
            animations.append(anim)
        
        return animations


class HoverScaleEffect:
    """
    Scale effect on hover for cards
    Usage: effect = HoverScaleEffect(card, scale_factor=1.02)
    """
    def __init__(self, widget, scale_factor=1.02, duration=200):
        self.widget = widget
        self.scale_factor = scale_factor
        self.duration = duration
        self.original_size = None
        self.is_hovered = False
        
        self.widget.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if obj == self.widget:
            if event.type() == event.Type.Enter:
                self._scale_up()
                return False
            elif event.type() == event.Type.Leave:
                self._scale_down()
                return False
        return False
    
    def _scale_up(self):
        """Scale widget up on hover"""
        if not self.original_size:
            self.original_size = self.widget.size()
        
        new_width = int(self.original_size.width() * self.scale_factor)
        new_height = int(self.original_size.height() * self.scale_factor)
        
        # Animate size
        anim = QPropertyAnimation(self.widget, b"geometry")
        anim.setDuration(self.duration)
        
        current_geo = self.widget.geometry()
        dx = (new_width - current_geo.width()) // 2
        dy = (new_height - current_geo.height()) // 2
        
        new_geo = QRect(
            current_geo.x() - dx,
            current_geo.y() - dy,
            new_width,
            new_height
        )
        
        anim.setStartValue(current_geo)
        anim.setEndValue(new_geo)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        self.widget._hover_anim = anim  # Keep reference
    
    def _scale_down(self):
        """Scale widget back to original size"""
        if not self.original_size:
            return
        
        anim = QPropertyAnimation(self.widget, b"geometry")
        anim.setDuration(self.duration)
        
        current_geo = self.widget.geometry()
        dx = (current_geo.width() - self.original_size.width()) // 2
        dy = (current_geo.height() - self.original_size.height()) // 2
        
        new_geo = QRect(
            current_geo.x() + dx,
            current_geo.y() + dy,
            self.original_size.width(),
            self.original_size.height()
        )
        
        anim.setStartValue(current_geo)
        anim.setEndValue(new_geo)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        self.widget._hover_anim = anim  # Keep reference


class ProgressAnimation:
    """
    Smooth progress bar animation
    Usage: ProgressAnimation.animate_to(progress_bar, target_value, duration=300)
    """
    @staticmethod
    def animate_to(progress_bar, target_value, duration=300):
        """Animate progress bar to target value"""
        anim = QPropertyAnimation(progress_bar, b"value")
        anim.setDuration(duration)
        anim.setStartValue(progress_bar.value())
        anim.setEndValue(target_value)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        
        # Keep reference to prevent garbage collection
        progress_bar._progress_anim = anim
        return anim
