from tabnanny import check

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QStyle, QTabBar, QStylePainter
, QStyleOptionTab, QTabWidget, QGridLayout, QVBoxLayout, QWidget, QLabel,
                               QLineEdit, QGroupBox, QComboBox, QDateEdit, QTableWidget, QHeaderView, QAbstractItemView,
                               QTableView, QMessageBox, QHBoxLayout, QSizePolicy, QFrame, QHeaderView,
                               QAbstractItemView, QRadioButton, QCheckBox,QTableWidgetItem )

from PySide6.QtCore import QSize, Qt, QDate, QUrl
from PySide6.QtGui import QFont, QPalette, QColor,QPixmap,QBrush, QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtSql import QSqlTableModel, QSqlDatabase
import sys

from PySide6.QtCore import QDate
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np





class elementos():

    def barra_lateral(self,botones):
        barraLateral_frame = QFrame()
        barraLateral_frame.setFixedWidth(195)
        barraLateral_frame.setStyleSheet("""QFrame {
                                                background-color: #B71C1C;
                                                    align-items:center;} """)

        barraLateral_layout = QVBoxLayout(barraLateral_frame)
        barraLateral_layout.setSpacing(1)
        barraLateral_layout.setContentsMargins(10, 20, 10, 20)
        self.botones_barra = {}

        def create_sidebar_button(text):
            btn = QPushButton(text)
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
            return btn

        for texto in botones:

            boton = create_sidebar_button(texto)
            boton.setObjectName(f"btn_{texto}")
            self.botones_barra[texto] = boton
            barraLateral_layout.addWidget(boton)

        barraLateral_layout.addStretch(1)

        btn_salir = create_sidebar_button("Salir")
        btn_salir.setObjectName("btn_Salir")
        self.botones_barra["Salir"] = btn_salir
        barraLateral_layout.addWidget(btn_salir)

        return barraLateral_frame,self.botones_barra



    def create_large_action_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(200, 80)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #000000;
                color: white; 
            }}
        """)
        return btn

    def crear_etiqueta(self, texto):
        etiqueta = QLabel(texto)
        etiqueta.setFixedSize(190,20)

        return etiqueta

    def crear_lineEdit(self):
        lineEdit = QLineEdit()
        lineEdit.setFixedSize(160,30)

        return lineEdit

    def crear_lineEditFijo(self):
        lineEdit = QLineEdit()
        lineEdit.setFixedHeight(30)
        lineEdit.setReadOnly(True)
        return lineEdit

    def crear_lista(self,opciones):
        combo=QComboBox()
        combo.setFixedSize(160,30)
        combo.addItems(opciones)
        return combo


    def crear_grafica(self,titulo,x,y):
        fig = Figure(figsize=(3, 2))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(titulo)
        fig.tight_layout()
        return canvas

    def crear_grafica_barras_h(self, titulo, categorias, capas):

        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        x = np.arange(len(categorias))

        n = len(capas)
        ancho_max = 0.5

        for idx, valores in enumerate(capas):
            ancho = ancho_max
            z = idx + 1
            ax.bar(
                x,
                valores,
                width=ancho,
                #color=color,
                label=f"Capa {idx + 1}",
                zorder=z
            )

        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.set_title(titulo)

        ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

        fig.tight_layout()

        return FigureCanvas(fig)

    def crear_tabla(self):

        tabla=QTableView()

        #Encabezado
        encabezado=tabla.horizontalHeader()
        encabezado.setSectionResizeMode(QHeaderView.ResizeToContents)

        tabla.setSelectionBehavior(QTableView.SelectRows)
        tabla.setAlternatingRowColors(True)

        return tabla

    def crear_tabladOS(self, filas, columnas, encabezados, columUno=None):
        tabla = QTableWidget()
        tabla.setRowCount(filas)
        tabla.setColumnCount(columnas)

        tabla.setHorizontalHeaderLabels(encabezados)


        # Ajuste visual recomendado
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.verticalHeader().setVisible(True)
        tabla.verticalHeader().setVisible(False)
        tabla.setAlternatingRowColors(True)

        # Llenar primera columna
        if columUno:
            for fila, texto in enumerate(columUno):
                item = QTableWidgetItem(str(texto))
                tabla.setItem(fila, 0, item)

            ultima_fila = filas - 1
            color_fondo = QColor("#D6EAF8")  # azul claro
            fuente_negrita = QFont()
            fuente_negrita.setBold(True)

            for col in range(columnas):
                item = tabla.item(ultima_fila, col)

                # Si no existe el item, créalo
                if item is None:
                    item = QTableWidgetItem("")
                    tabla.setItem(ultima_fila, col, item)

                item.setBackground(QBrush(color_fondo))
                item.setFont(fuente_negrita)
                item.setTextAlignment(Qt.AlignCenter)

                # (opcional) evitar edición
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        return tabla

    def crear_mapa(self):
        mapa=QWebEngineView()
        mapa.setMinimumSize(300, 300)

        html_mapa = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <meta charset="utf-8" />
                    <title>Mapa de coordenadas</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
                    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
                    <style>
                    html, body { margin: 0; padding: 0; height: 100%; }
                    #mapid { height: 100%; width: 100%; border-radius: 10px; }
                    </style>
                    </head>
                    <body>
                    <div id="mapid"></div>
                    <script>
                    var map = L.map('mapid').setView([23.6345, -102.5528], 5);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 19,
                        attribution: '© OpenStreetMap contributors'
                    }).addTo(map);
                    </script>
                    </body>
                    </html>
                    """
        mapa.setHtml(html_mapa)

        return mapa


    def crear_buscador(self):

        area=QFrame()
        area_layout = QHBoxLayout(area)

        icono=QLabel()
        icono.setPixmap(QPixmap(r"../imagenes/iconoBuscar.png").scaled(18, 20, Qt.KeepAspectRatio,
                                                                       Qt.SmoothTransformation))
        icono.setStyleSheet("padding-left: 4px;")
        icono.setAlignment(Qt.AlignCenter)

        buscador=QLineEdit()
        buscador.setPlaceholderText("Buscar campo por nombre...")
        buscador.setFixedHeight(40)

        area_layout.addWidget(icono)
        area_layout.addWidget(buscador)


        return area

    def crear_boton(self,texto):
        btn = QPushButton(texto)
        #btn.setStyleSheet("font-weight: bold;")
        return btn

    def crear_imagen_estructura(self):
        label = QLabel()
        pix = QPixmap(r"../imagenes/TorrePerforacionF.jpg")
        label.setPixmap(pix)
        label.setAlignment(Qt.AlignCenter)
        label.setScaledContents(True)
        label.setFixedSize(400,550)
        return label

    def crear_radio(self,texto):
        radio = QRadioButton(texto)
        return radio

    def crear_check(self):
        check=QCheckBox()
        check.setContentsMargins(0, 0, 0, 0)
        check.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                    padding: 0px;
                    margin: 5px;
                }
                QCheckBox::indicator {
                    width: 14px;
                    height: 14px;
                    margin: 0px;
                }
            """)
        return check
