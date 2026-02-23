###############################################################
#                                                             #
#               DESARROLLO APLIACIÓN                          #
#                    DETICAES                                 #
#                                                             #
#             FRONTEND - PANTALLA PRINCIPAL                   #
#                                                             #
###############################################################


############################Librerias##########################

import sys

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit,
    QTabWidget,QGridLayout)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import (QFont, QPalette, QColor,QPixmap,QIcon)

from qt_material import apply_stylesheet

from fron_General import seccion_informacion
from fron_Instalaciones import seccion_instalaciones
from fron_economia import seccion_evalE
from font_acerca import seccion_about
###############################################################

class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DETICAES")

        self.setWindowIcon(QIcon(r"../imagenes/DTC.ico"))

        #Tamaño de la pantalla
        tamanoPantalla=QApplication.primaryScreen().availableGeometry()
        self.ancho=int(tamanoPantalla.width()*0.95)
        self.altura=int(tamanoPantalla.height()*0.95)
        self.resize(self.ancho, self.altura)

        #ubicacion de apertura
        self.move(int((tamanoPantalla.width()-self.ancho)/1.8),
                  int((tamanoPantalla.height()-self.altura)/3)-10)

        #self.estilos()

        #Creacion de pestañas
        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        tab_General = QWidget()
        self.pestania_general = seccion_informacion()
        self.pestania_general.cargar_contenido(tab_General)

        tab_instalaciones = QWidget()
        self.pestania_instalaciones = seccion_instalaciones()
        self.pestania_instalaciones.cargar_contenido(tab_instalaciones)


        tab_costos = QWidget()
        self.pestania_costos = seccion_evalE()
        self.pestania_costos.cargar_contenido(tab_costos)

        tab_acerca = QWidget()
        self.pestania_acerca=seccion_about()
        self.pestania_acerca.cargar_contenido(tab_acerca)

        tabs.addTab(tab_General, "Información General")
        tabs.addTab(tab_instalaciones, "Instalaciones")
        tabs.addTab(tab_costos, "Costos")
        tabs.addTab(tab_acerca, "Acerca de")


    def estilos(self):
        palette = QPalette()
        self.COLOR_DARK_TEAL = QColor(0, 105, 120)
        self.COLOR_LIGHT_GRAY = QColor(240, 240, 240)
        self.COLOR_ACCENT = QColor(0, 139, 139)

        palette.setColor(QPalette.Window, self.COLOR_DARK_TEAL)
        self.setPalette(palette)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyle("Fusion")
    app.setStyle("windows11")
    app.setStyleSheet("""
    /* =================== GENERAL =================== */
    QWidget {
        background-color: #EEEEEE;
        
    }
    
    QTabWidget::pane {
    border: 1px solid #BDBDBD;
    }
    
    QTabBar::tab {
        background: #ECECEC;
        color: #424242;
        padding: 10px 18px;
        margin-right: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    
    QTabBar::tab:selected {
        background: #424242;
        color: white;
        font-weight: bold;
    }
    
    QTabBar::tab:hover {
        background: #90CAF9;
    }
    
    QFrame {background: #EOEOEO;}
    
    QPushButton {
                    background-color: white;
                    color: black;
                    border: 1px solid black;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
    QPushButton:hover {
                    background-color: #EF9A9A;
                    color: black;
                }
                
    QPushButton:pressed {
        background-color: #B71C1C; 
        padding-left: 2px;        
        padding-top: 2px;
        border: 3px solid #555555;
        color: white;
    } 
    

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())