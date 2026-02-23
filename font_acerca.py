from PySide6.QtWidgets import (QPushButton, QGridLayout, QVBoxLayout,
                               QGroupBox, QHBoxLayout, QFrame, QLabel, QButtonGroup,
                               QStackedLayout, QWidget, QLineEdit, QTextEdit)
from PySide6.QtCore import QDate,Qt

from complementos import elementos
from PySide6.QtGui import QPixmap,QFont
from core.CoreUI import (barraNav,UIcoreInsta)
import os

class seccion_about(elementos):

    def cargar_contenido(self, tab):
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =================BOTONES DE BARRA DE NAVEGACION==================================
        barraLateral_frame = QFrame()
        barraLateral_frame.setFixedWidth(195)
        barraLateral_frame.setStyleSheet("""QFrame {
                                                        background-color: #B71C1C;
                                                            align-items:center;} """)

        barraLateral_layout = QVBoxLayout(barraLateral_frame)
        barraLateral_layout.setSpacing(1)
        barraLateral_layout.setContentsMargins(10, 20, 10, 20)
        barraLateral_layout.addStretch(1)

        btn = QPushButton("Salir")
        btn.setFixedSize(175, 40)
        btn.setStyleSheet("""
                        QPushButton {
                            background-color: white;
                            color: black;
                            border: 1px solid black;
                            border-radius: 5px;
                            font-size: 14px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #DDDDDD;
                        }
                    """)

        btn.clicked.connect(barraNav.cerrar_barra)

        barraLateral_layout.addWidget(btn)

        layout.addWidget(barraLateral_frame)

        # ================= Componentes ==================================

        ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_final = os.path.join(ruta_raiz, "imagenes", "Fondo.png").replace("\\", "/")

        fondo=QFrame()
        #fondo_layout = QVBoxLayout(fondo)

        fondo.setObjectName("ContenedorFondo")

        fondo.setStyleSheet(f"""
            #ContenedorFondo {{
        border-image: url("{ruta_final}") 0 0 0 0 stretch stretch;
        background-repeat: no-repeat;
        background-position: center;
                                    }}
            QLabel {{
                    background: transparent;
                    color: black;
                    font-weight: bold;
                }}
                                        """)


        link_espoil = QLabel(fondo)
        link_espoil.setFixedHeight(30)
        link_espoil.setFixedWidth(150)
        link_espoil.setObjectName("linkWeb")
        link_espoil.setText('<a href="https://espoil.net/index.html" style="color: #0055ff; font-size:20px; text-decoration: underline;">www.espoil.net</a>')
        link_espoil.setOpenExternalLinks(True)
        link_espoil.setCursor(Qt.PointingHandCursor)
        link_espoil.adjustSize()
        link_espoil.move(70, 295)
        #fondo_layout.addWidget(link_espoil)



        layout.addWidget(fondo)



