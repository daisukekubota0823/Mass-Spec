from PyQt5.QtCore import QPointF
    from PyQt5.QtGui import QPainterPath, QGraphicsItem, QGraphicsEllipseItem


    class AnnotatedDrawingVisual(QGraphicsEllipseItem):
        def __init__(self, annotation, center=None, radius=10, parent=None):
            """
            Initialize the AnnotatedDrawingVisual object.

            :param annotation: The annotation associated with this visual.
            :param center: The center point (QPointF) of the visual.
            :param radius: The radius of the visual (default is 10).
            :param parent: The parent QGraphicsItem (optional).
            """
            super().__init__(parent)
            self.annotation = annotation
            self.setRect(-radius, -radius, radius * 2, radius * 2)  # Default size of the visual
            self.center = center if center else QPointF(0, 0)
            self.setPos(self.center)

        @property
        def annotation(self):
            return self._annotation

        @annotation.setter
        def annotation(self, value):
            self._annotation = value

        @property
        def center(self):
            return self.pos()

        @center.setter
        def center(self, value):
            self.setPos(value)
    