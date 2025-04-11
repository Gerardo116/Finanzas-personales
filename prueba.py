import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DonutChart(FigureCanvas):
    def __init__(self, progress=75):
        fig = Figure(figsize=(2.5, 2.5), tight_layout=True)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.draw_chart(progress)

    def draw_chart(self, progress):
        self.ax.clear()
        self.ax.pie(
            [progress, 100 - progress],
            colors=["#3CB371", "#E0E0E0"],
            startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='white')
        )
        self.ax.text(0, 0, f"{progress}%", ha='center', va='center', fontsize=16, weight='bold')
        self.ax.axis('equal')
        self.draw()


class StyledApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor Estético de Tareas")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(self.styles())
        self.init_ui()

    def styles(self):
        return """
        QWidget {
            background-color: #F9FAFB;
            font-family: Arial;
        }
        QFrame#sidebar {
            background-color: #E5E7EB;
        }
        QPushButton {
            background-color: transparent;
            border: none;
            padding: 12px;
            text-align: left;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #D1D5DB;
        }
        QListWidget {
            border: none;
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 10px;
        }
        QListWidget::item {
            padding: 10px;
            margin-bottom: 5px;
            background-color: #F3F4F6;
            border-radius: 6px;
        }
        QLabel#sectionTitle {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        """

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QVBoxLayout()
        for name in ["Dashboard", "Tareas", "Proyectos", "Ajustes"]:
            btn = QPushButton(name)
            sidebar.addWidget(btn)
        sidebar.addStretch()
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar")
        sidebar_frame.setFixedWidth(180)
        sidebar_frame.setLayout(sidebar)

        # Main content
        content_layout = QVBoxLayout()
        title = QLabel("Mis Tareas")
        title.setObjectName("sectionTitle")
        task_list = QListWidget()
        for tarea in ["Enviar reporte", "Planificar reunión", "Actualizar KPIs"]:
            item = QListWidgetItem(tarea)
            task_list.addItem(item)
        content_layout.addWidget(title)
        content_layout.addWidget(task_list)

        # Right panel
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Progreso del Proyecto"))
        right_panel.addWidget(DonutChart(65))
        right_panel.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add to main layout
        main_layout.addWidget(sidebar_frame)
        main_layout.addLayout(content_layout, 3)
        main_layout.addLayout(right_panel, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StyledApp()
    window.show()
    sys.exit(app.exec_())
