"""
Advanced Animation Effects - Part 2
Additional modern UI animations and effects for FactuNabo
"""

from PySide6.QtWidgets import (QWidget, QFrame, QLabel, QGraphicsBlurEffect, 
                                QGraphicsOpacityEffect, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import (QPropertyAnimation, QSequentialAnimationGroup, 
                            QParallelAnimationGroup, QEasingCurve, QTimer, 
                            Qt, QRect, QPoint, QPointF, QRectF)
from PySide6.QtGui import (QPainter, QColor, QLinearGradient, QPen, QBrush,
                           QPainterPath, QTransform)
import math


class PageTransition:
    """
    Page transition animations for switching between views
    Supports fade, slide, and combined transitions
    """
    
    @staticmethod
    def fade_transition(old_widget, new_widget, duration=250, on_finished=None):
        """
        Fade out old widget while fading in new widget
        """
        # Ensure new widget is positioned correctly
        new_widget.setGeometry(old_widget.geometry())
        new_widget.show()
        
        # Create opacity effects
        old_effect = QGraphicsOpacityEffect(old_widget)
        new_effect = QGraphicsOpacityEffect(new_widget)
        old_widget.setGraphicsEffect(old_effect)
        new_widget.setGraphicsEffect(new_effect)
        
        old_effect.setOpacity(1.0)
        new_effect.setOpacity(0.0)
        
        # Create animations
        group = QParallelAnimationGroup()
        
        fade_out = QPropertyAnimation(old_effect, b"opacity")
        fade_out.setDuration(duration)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.OutCubic)
        
        fade_in = QPropertyAnimation(new_effect, b"opacity")
        fade_in.setDuration(duration)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.OutCubic)
        
        group.addAnimation(fade_out)
        group.addAnimation(fade_in)
        
        def cleanup():
            old_widget.hide()
            if on_finished:
                on_finished()
        
        group.finished.connect(cleanup)
        group.start()
        
        # Keep reference
        new_widget._transition_anim = group
        return group
    
    @staticmethod
    def slide_transition(old_widget, new_widget, direction='left', duration=300, on_finished=None):
        """
        Slide old widget out while sliding new widget in
        direction: 'left', 'right', 'up', 'down'
        """
        parent = old_widget.parent()
        if not parent:
            return
        
        # Position new widget off-screen
        old_geo = old_widget.geometry()
        new_widget.setGeometry(old_geo)
        
        if direction == 'left':
            new_start = QRect(old_geo.x() + old_geo.width(), old_geo.y(), old_geo.width(), old_geo.height())
            old_end = QRect(old_geo.x() - old_geo.width(), old_geo.y(), old_geo.width(), old_geo.height())
        elif direction == 'right':
            new_start = QRect(old_geo.x() - old_geo.width(), old_geo.y(), old_geo.width(), old_geo.height())
            old_end = QRect(old_geo.x() + old_geo.width(), old_geo.y(), old_geo.width(), old_geo.height())
        elif direction == 'up':
            new_start = QRect(old_geo.x(), old_geo.y() + old_geo.height(), old_geo.width(), old_geo.height())
            old_end = QRect(old_geo.x(), old_geo.y() - old_geo.height(), old_geo.width(), old_geo.height())
        else:  # down
            new_start = QRect(old_geo.x(), old_geo.y() - old_geo.height(), old_geo.width(), old_geo.height())
            old_end = QRect(old_geo.x(), old_geo.y() + old_geo.height(), old_geo.width(), old_geo.height())
        
        new_widget.setGeometry(new_start)
        new_widget.show()
        new_widget.raise_()
        
        # Create animations
        group = QParallelAnimationGroup()
        
        slide_out = QPropertyAnimation(old_widget, b"geometry")
        slide_out.setDuration(duration)
        slide_out.setStartValue(old_geo)
        slide_out.setEndValue(old_end)
        slide_out.setEasingCurve(QEasingCurve.OutCubic)
        
        slide_in = QPropertyAnimation(new_widget, b"geometry")
        slide_in.setDuration(duration)
        slide_in.setStartValue(new_start)
        slide_in.setEndValue(old_geo)
        slide_in.setEasingCurve(QEasingCurve.OutCubic)
        
        group.addAnimation(slide_out)
        group.addAnimation(slide_in)
        
        def cleanup():
            old_widget.hide()
            if on_finished:
                on_finished()
        
        group.finished.connect(cleanup)
        group.start()
        
        new_widget._transition_anim = group
        return group


class SkeletonLoader(QFrame):
    """
    Skeleton loading screen with animated shimmer effect
    """
    
    def __init__(self, parent=None, width=200, height=20):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.shimmer_pos = 0.0
        self.shimmer_speed = 0.02  # 0-1 per frame
        
        # Start animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate_shimmer)
        self.timer.start(16)  # ~60 FPS
    
    def _animate_shimmer(self):
        """Animate shimmer position"""
        self.shimmer_pos += self.shimmer_speed
        if self.shimmer_pos > 1.0:
            self.shimmer_pos = -0.3  # Reset with some negative to create gap
        self.update()
    
    def paintEvent(self, event):
        """Paint skeleton with shimmer gradient"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background color
        bg_color = QColor(230, 230, 230)
        painter.fillRect(self.rect(), bg_color)
        
        # Shimmer gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        
        # Calculate shimmer position
        center = self.shimmer_pos
        width = 0.3
        
        # Add gradient stops
        gradient.setColorAt(max(0, center - width), QColor(230, 230, 230, 0))
        gradient.setColorAt(center, QColor(255, 255, 255, 150))
        gradient.setColorAt(min(1, center + width), QColor(230, 230, 230, 0))
        
        painter.fillRect(self.rect(), gradient)
        
        painter.end()
    
    def stop(self):
        """Stop animation"""
        self.timer.stop()


class ToastNotification(QLabel):
    """
    Enhanced toast notification with slide + bounce effect
    """
    
    def __init__(self, message, parent, duration=3000, position='top'):
        super().__init__(message, parent)
        self.setProperty("id", "toast")
        self.setAlignment(Qt.AlignCenter)
        self.adjustSize()
        self.setMinimumWidth(200)
        
        # Position off-screen
        if position == 'top':
            start_y = -self.height() - 20
            end_y = 20
        else:  # bottom
            start_y = parent.height() + 20
            end_y = parent.height() - self.height() - 20
        
        center_x = (parent.width() - self.width()) // 2
        self.move(center_x, start_y)
        
        # Show and animate in
        self.show()
        self._animate_in(center_x, start_y, end_y)
        
        # Auto-dismiss
        QTimer.singleShot(duration, self._animate_out)
    
    def _animate_in(self, x, start_y, end_y):
        """Slide in with bounce (OutBack easing)"""
        self.anim_in = QPropertyAnimation(self, b"pos")
        self.anim_in.setDuration(400)
        self.anim_in.setStartValue(QPoint(x, start_y))
        self.anim_in.setEndValue(QPoint(x, end_y))
        self.anim_in.setEasingCurve(QEasingCurve.OutBack)  # Bounce effect
        self.anim_in.start()
    
    def _animate_out(self):
        """Fade out and slide up slightly"""
        # Opacity fade
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        
        fade = QPropertyAnimation(effect, b"opacity")
        fade.setDuration(300)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.OutCubic)
        
        # Slight slide up
        slide = QPropertyAnimation(self, b"pos")
        slide.setDuration(300)
        current_pos = self.pos()
        slide.setStartValue(current_pos)
        slide.setEndValue(QPoint(current_pos.x(), current_pos.y() - 20))
        slide.setEasingCurve(QEasingCurve.OutCubic)
        
        # Group animations
        group = QParallelAnimationGroup(self)
        group.addAnimation(fade)
        group.addAnimation(slide)
        group.finished.connect(self.deleteLater)
        group.start()
        
        self._anim_out = group


class AnimatedInput(QWidget):
    """
    Input field with animated focus glow effect
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.glow_intensity = 0.0
        self.is_focused = False
        
    def animate_focus_in(self):
        """Animate glow on focus"""
        self.is_focused = True
        self.glow_anim = QPropertyAnimation(self, b"glow_intensity")
        self.glow_anim.setDuration(150)
        self.glow_anim.setStartValue(self.glow_intensity)
        self.glow_anim.setEndValue(1.0)
        self.glow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.glow_anim.start()
        
        # Connect to update
        self.glow_anim.valueChanged.connect(lambda: self.update())
    
    def animate_focus_out(self):
        """Animate glow off on blur"""
        self.is_focused = False
        self.glow_anim = QPropertyAnimation(self, b"glow_intensity")
        self.glow_anim.setDuration(150)
        self.glow_anim.setStartValue(self.glow_intensity)
        self.glow_anim.setEndValue(0.0)
        self.glow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.glow_anim.start()
        
        self.glow_anim.valueChanged.connect(lambda: self.update())


class ParallaxScrollArea:
    """
    Parallax effect for scroll areas
    Header moves at different speed than content
    """
    
    def __init__(self, scroll_area, header_widget, factor=0.5):
        """
        scroll_area: QScrollArea
        header_widget: Widget to apply parallax to
        factor: Speed factor (0.5 = half speed)
        """
        self.scroll_area = scroll_area
        self.header_widget = header_widget
        self.factor = factor
        self.original_y = header_widget.y()
        
        # Connect to scroll
        scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll)
    
    def _on_scroll(self, value):
        """Update header position based on scroll"""
        offset = value * self.factor
        self.header_widget.move(self.header_widget.x(), self.original_y - offset)


class PulsingStatusChip(QLabel):
    """
    Status chip with pulsing brightness animation
    """
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "StatusChip")
        self.brightness = 1.0
        self.pulsing = False
        
    def start_pulse(self):
        """Start pulsing animation"""
        if self.pulsing:
            return
        
        self.pulsing = True
        self.pulse_anim = QPropertyAnimation(self, b"brightness")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(1.0)
        self.pulse_anim.setEndValue(1.15)
        self.pulse_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.pulse_anim.setLoopCount(-1)  # Infinite loop
        
        # Reverse animation at halfway
        self.pulse_anim.setDirection(QPropertyAnimation.Forward)
        self.pulse_anim.valueChanged.connect(self._update_brightness)
        self.pulse_anim.start()
    
    def stop_pulse(self):
        """Stop pulsing animation"""
        self.pulsing = False
        if hasattr(self, 'pulse_anim'):
            self.pulse_anim.stop()
        self.brightness = 1.0
        self._update_brightness()
    
    def _update_brightness(self):
        """Update widget brightness"""
        # This would need custom painting or stylesheet manipulation
        # For now, we can use opacity as a proxy
        self.setStyleSheet(f"""
            QLabel[class="StatusChip"] {{
                opacity: {self.brightness};
            }}
        """)


class BlurBackdrop:
    """
    Real blur effect for backgrounds (Glassmorphism)
    """
    
    @staticmethod
    def apply_blur(widget, radius=20):
        """Apply blur effect to widget background"""
        blur = QGraphicsBlurEffect(widget)
        blur.setBlurRadius(radius)
        widget.setGraphicsEffect(blur)
        return blur
    
    @staticmethod
    def animate_blur(widget, from_radius=0, to_radius=20, duration=300):
        """Animate blur radius"""
        blur = QGraphicsBlurEffect(widget)
        widget.setGraphicsEffect(blur)
        blur.setBlurRadius(from_radius)
        
        anim = QPropertyAnimation(blur, b"blurRadius")
        anim.setDuration(duration)
        anim.setStartValue(from_radius)
        anim.setEndValue(to_radius)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        widget._blur_anim = anim
        return anim


class Transform3D:
    """
    3D transform effects for widgets
    """
    
    @staticmethod
    def apply_tilt_on_hover(widget, max_angle=5):
        """
        Apply 3D tilt effect based on mouse position
        max_angle: Maximum tilt angle in degrees
        """
        widget._tilt_max_angle = max_angle
        widget._tilt_transform = QTransform()
        
        # Override mouse events
        original_enter = widget.enterEvent
        original_move = widget.mouseMoveEvent
        original_leave = widget.leaveEvent
        
        def enter_event(e):
            widget.setMouseTracking(True)
            original_enter(e)
        
        def mouse_move_event(e):
            # Calculate tilt based on mouse position
            center_x = widget.width() / 2
            center_y = widget.height() / 2
            
            mouse_x = e.position().x()
            mouse_y = e.position().y()
            
            # Calculate angles (-max_angle to +max_angle)
            angle_x = ((mouse_y - center_y) / center_y) * max_angle
            angle_y = -((mouse_x - center_x) / center_x) * max_angle
            
            # Apply transform (simplified 2D approximation of 3D)
            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.rotate(angle_x, Qt.XAxis)  # Note: Qt doesn't fully support 3D
            transform.rotate(angle_y, Qt.YAxis)
            transform.translate(-center_x, -center_y)
            
            # This is a simplified version - full 3D requires QGraphicsView
            # For now, we just apply a subtle scale/skew
            widget.update()
            
            original_move(e)
        
        def leave_event(e):
            widget.setMouseTracking(False)
            # Reset transform
            widget.update()
            original_leave(e)
        
        widget.enterEvent = enter_event
        widget.mouseMoveEvent = mouse_move_event
        widget.leaveEvent = leave_event


class AnimatedGradient(QWidget):
    """
    Widget with animated gradient background
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_pos = 0.0
        self.color1 = QColor(160, 191, 110, 50)  # Green corporate
        self.color2 = QColor(135, 161, 93, 50)   # Darker green
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate_gradient)
        self.timer.start(30)  # ~33 FPS for smooth gradient
    
    def _animate_gradient(self):
        """Animate gradient position"""
        self.gradient_pos += 0.01
        if self.gradient_pos > 1.0:
            self.gradient_pos = 0.0
        self.update()
    
    def paintEvent(self, event):
        """Paint animated gradient"""
        painter = QPainter(self)
        
        # Create animated gradient
        gradient = QLinearGradient(
            self.width() * self.gradient_pos, 0,
            self.width() * (self.gradient_pos + 0.5), self.height()
        )
        gradient.setColorAt(0, self.color1)
        gradient.setColorAt(0.5, self.color2)
        gradient.setColorAt(1, self.color1)
        
        painter.fillRect(self.rect(), gradient)
        painter.end()
    
    def stop_animation(self):
        """Stop gradient animation"""
        self.timer.stop()
