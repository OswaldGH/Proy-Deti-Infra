from dataclasses import dataclass, asdict
from datetime import date

from PySide6.QtWidgets import QComboBox

#items
from ui.fron_General import *
from ui.fron_Instalaciones import *
from ui.fron_economia import *


@dataclass
class geologia:
    ambiente: str = ""
    yacimiento: str = ""
    fluido: str = ""
    porosidad:float = 0.0
    permeabilidad:float = 0.0

@dataclass
class fluido:
    api: float = 0.0
    rga:float = 0.0
    rgc:float = 0.0
    volAceite: float = 0.0
    volGas: float = 0.0


@dataclass
class pozo_expo:
    nombre: str = ""
    latitud: float = 0.0
    longitud: float = 0.0





class extractor:
    def __init__(self, valores : dict):
        self.valores = valores

    def leer(self, key):

        if key not in self.valores:
            raise KeyError(f"No existe la clave '{key}' en el diccionario")

        widget = self.valores[key]

        # Verificamos qué tipo de widget es para saber cómo extraer el dato
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QDateEdit):
            # Convertimos QDate a un objeto date de Python
            qdate = widget.date()
            return date(qdate.year(), qdate.month(), qdate.day())

        return None

    def leer_float(self, key):
        valor_texto = self.leer(key)
        try:
            return float(valor_texto) if valor_texto else 0.0
        except ValueError:
            return 0.0



@dataclass
class InfoGene:
    nombreCampo: str = ""
    descubrimiento: int = 0
    ubicacion: str = ""
    region: str = ""
    activo_extraccion: str = ""
    estatus: str = ""
    inicioPerforacion: date = date.today()

