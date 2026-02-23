import sys
from PySide6.QtWidgets import (
    QApplication)

class barraNav:

    @staticmethod
    def cerrar_barra():
        app = QApplication.instance()
        if app:
            app.quit()
        else:
            sys.exit(0)


    def cambiaPestaña(self, ventana, nombre):
        # Ocultar todas
        ventana.contenido.hide()
        ventana.contenidoAnalogias.hide()
        ventana.contenidoReservas.hide()
        ventana.contenidoPronosticos.hide()

        # Mostrar la seleccionada
        if nombre == "Información General":
            ventana.contenido.show()

        elif nombre == "Analogías":
            ventana.contenidoAnalogias.show()

        elif nombre == "Reservas":
            ventana.contenidoReservas.show()

        elif nombre == "Pronosticos":
            ventana.contenidoPronosticos.show()

    def cambiaPestañaIns(self, ventana, nombre):
            # Ocultar todas
            ventana.cont_Menajo.hide()
            ventana.cont_red.hide()
            ventana.cont_separadores.hide()
            ventana.cont_analisis.hide()

            # Mostrar la seleccionada
            if nombre == "Manejo de la producción":
                ventana.cont_Menajo.show()

            elif nombre == "Red de transporte":
                ventana.cont_red.show()

            elif nombre == "Separadores":
                ventana.cont_separadores.show()

            elif nombre == "Analisis hidraulico":
                ventana.cont_analisis.show()

    def cambiaPestañaCostos(self, ventana, nombre):
            # Ocultar todas
            ventana.contenido_eval.hide()
            ventana.copntenido_esce.hide()


            # Mostrar la seleccionada
            if nombre == "Evaluación económica":
                ventana.contenido_eval.show()

            elif nombre == "Esceanrio tipo":
                ventana.copntenido_esce.show()



class UIcoreInsta:
    def cambiar_servicio(self, ventana, nombre):
        # Ocultar
        ventana.oleo_datos.hide()
        ventana.oleo_resul.hide()
        ventana.oil_datos.hide()
        ventana.oil_resul.hide()
        ventana.gas_datos.hide()
        ventana.gas_resul.hide()

        # Mostrar según servicio
        if nombre == "ViewOleogaso":
            ventana.oleo_datos.show()
            ventana.oleo_resul.show()

        elif nombre == "ViewOleo":
            ventana.oil_datos.show()
            ventana.oil_resul.show()

        elif nombre == "ViewGas":
            ventana.gas_datos.show()
            ventana.gas_resul.show()

    def cambiar_componente(self, ventana, nombre):
        # Ocultar

        ventana.cabezal_grupo.hide()
        ventana.bajante_grupo.hide()
        ventana.servicio_grupo.hide()


        # Mostrar según servicio
        if nombre == "Viewcabezal":
            ventana.cabezal_grupo.show()


        elif nombre == "Viewbajante":

            ventana.bajante_grupo.show()


        elif nombre == "Viewducto":
            ventana.servicio_grupo.show()
