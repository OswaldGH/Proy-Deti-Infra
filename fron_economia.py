from PySide6.QtWidgets import (QPushButton, QGridLayout, QVBoxLayout,
                               QGroupBox, QHBoxLayout, QFrame, QLabel,QButtonGroup,QLineEdit,QSizePolicy)
from PySide6.QtCore import QDate

from complementos import elementos
from core.CoreUI import (barraNav,UIcoreInsta)

class seccion_evalE(elementos):

    def cargar_contenido(self, tab):
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =================BOTONES DE BARRA DE NAVEGACION==================================
        bonotes_barra = [
                         "Evaluación económica",
                         "Esceanrio tipo"]

        self.barra_opciones, self.botones_barra = elementos.barra_lateral(tab, bonotes_barra)
        layout.addWidget(self.barra_opciones)

        self.botones_barra["Salir"].clicked.connect(barraNav.cerrar_barra)
        #======================== CARGAR CONTENIDO ========================================

        self.contenido_eval = self.contenido_evalEco()
        layout.addWidget(self.contenido_eval)

        self.copntenido_esce=self.contenido_esenario()
        layout.addWidget(self.copntenido_esce)

        self.contenido_eval.show()
        self.copntenido_esce.hide()

        nav = barraNav()

        for nombre, boton in self.botones_barra.items():
            if nombre != "Salir":
                boton.clicked.connect(lambda _, n=nombre: nav.cambiaPestañaCostos(self, n))

    def contenido_evalEco(self):
        content_eval = QFrame()
        content_eval.setStyleSheet(f"background-color: {(240, 240, 240)};")
        contenteval_layout = QGridLayout(content_eval)
        contenteval_layout.setSpacing(3)

        contenteval_layout.setColumnStretch(0, 7)
        contenteval_layout.setColumnStretch(1, 3)


        #CREACION DE GURPOS
        grupoCosotos=QGroupBox("Costos desarrollo tipo del campo", content_eval)
        grupoCosotos_layout = QGridLayout(grupoCosotos)

        grupoCosotos_layout.setRowStretch(0, 4)
        grupoCosotos_layout.setRowStretch(1, 3)
        grupoCosotos_layout.setRowStretch(2, 3)

        grupoFinanciera=QGroupBox("Evaluación financiera", content_eval)
        grupoFinanciera_layout=QGridLayout(grupoFinanciera)


        #=====================================COSOTOS DESAROLLO=====================================================
        self.grupos = {}
        self.grupos_layouts = {}

        grupos_etiquetas = {"CperTer": ("Peforación y terminación", 0, 0, 1, 1),
                            "Cproces": ("Equipos de proceso", 1, 0, 2, 1),
                            "CProdu": ("Soportes de producción", 0, 1, 1, 1),
                            "Ctranspor": ("Sistema de ductos", 1, 1, 1, 1),
                            "CTotal": ("Inversión", 2, 1, 1, 1),
                            }
        for i, (key, (Titulo, x, y, xs, ys)) in enumerate(grupos_etiquetas.items()):

            grupo = QGroupBox(Titulo)
            self.grupos[key] = grupo

            layout_grupo = QVBoxLayout()
            layout_grupo.setSpacing(0)
            grupo.setLayout(layout_grupo)

            self.grupos_layouts[key] = layout_grupo

            grupoCosotos_layout.addWidget(grupo, x, y, xs, ys)

        contenteval_layout.addWidget(grupoCosotos, 0,0)
        contenteval_layout.addWidget(grupoFinanciera, 0,1)

        self.editCostos={}
        editCostos_valores={
                            "CNoPozos":"Numero de pozos",
                            "TotalInver":"Total inversión estratégica (MMUSD)",
                            "OTRinver":"Otras inversiones (12% margen error)",
                            "Copex":"OPEX (38.3% de la inversión)(MMUSD)"
        }

        for j,(key,TEXT) in enumerate(editCostos_valores.items()):
            filaC=QFrame(content_eval)
            filaC_layout = QHBoxLayout(filaC)

            etiqueta=QLabel(TEXT)
            filaC_layout.addWidget(etiqueta)

            valor=QLineEdit(content_eval)
            valor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.editCostos[key] = valor
            filaC_layout.addWidget(valor)

            if j==0:
                self.grupos_layouts["CperTer"].addWidget(filaC)
            else:
                self.grupos_layouts["CTotal"].addWidget(filaC)

        #========================== TABLAS =========================================================
        #encabezados
        encabezadoPerfo=["Concepto", "Precio unitario\n(MMUSD)", "Costo total\n(MMUSD)"]
        encabezadoProce=["Concepto", "Costo total\n(MMUSD)"]
        encabezadoProduc=["Estructura", "Cant", "Precio unitario\n(MMUSD)", "Costo total\n(MMUSD)"]
        encabezadoTransporte=["Ductos", "Longitud (km)", "Diámetro (pulg)", "Costo ducto\n(MMUSD)"]

        #Primera columna
        firstPerfo=["Perforación", "Terminación","Total"]
        firstProce=["Separador de prueba",
                    "Bombeo multifásico",
                    "Separador remoto",
                    "Batería de separación",
                    "Separadores 1ra y 2da etapa",
                    "Rectificadores 1ra y 2da etapa",
                    "Bombas",
                    "Compresor de baja y alta presión",
                    "Otros equipos",
                    "Total"]
        firstProduc=["Macropera - 16 pozos",
                     "Macropera - 12 pozos",
                     "Macropera - 4/6 pozos",
                     "Macropera - 2/3 pozos",
                     "Pera - 1 Pozo",
                     "Total"]
        firstTransporte=["oleogasoducto",
                         "Oleoducto",
                         "Gasoducto",
                         "Total"]

        self.tablas_item={}
        tablas_etis={
                    "tablaPerfo":(3,3,encabezadoPerfo,"CperTer",firstPerfo ),
                    "tablaProce":(10,2,encabezadoProce, "Cproces",firstProce),
                    "tablaProdu":(6,4,encabezadoProduc, "CProdu", firstProduc),
                    "tablaTransporte":(4,4,encabezadoTransporte, "Ctranspor", firstTransporte),
                    }

        for t,(key,(fila,columna, encabezado, destino,CUNO)) in enumerate(tablas_etis.items()):

            tabla=elementos.crear_tabladOS(content_eval, fila,columna,encabezado,CUNO)
            self.tablas_item[key]=tabla
            self.grupos_layouts[destino].addWidget(tabla)


        #================================== EVALUACIÓN FINANCIERA ====================================================
        textoE="Seleccione el tipo de escenario para verificar\n la rentabilidad del campo nuevo"
        self.elementos_evaluacion={}
        self.etiquetas_evaluacion={
                                    "eCapex":"CAPEX (MMUSD)",
                                    "eOPEX":"OPEX (MMUSD)",
                                    "eTotal":"TOTAL (MMUSD)",
                                    "T": textoE,
                                    "RentLis":["Minima rentabilidad", "Media rentabilidad", "Maxima rentabilidad"],
                                    "Tdescu":"Tasa de descuento",
                                    "baPRICE":"Precio del barril (USD)",
                                    "VPN":"VPN (MMUSD)",
                                    "tir":"TIR (%)",
                                    "BC":"B/C"
                                    }

        for i,(key,contenido) in enumerate(self.etiquetas_evaluacion.items()):
            filaEvla=QFrame(content_eval)
            filaEvla_lay=QHBoxLayout(filaEvla)

            if i!=3:
                if i != 4:
                    etiqueta=QLabel(contenido)
                    filaEvla_lay.addWidget(etiqueta)

                    valor=QLineEdit(content_eval)
                    filaEvla_lay.addWidget(valor)
                    self.elementos_evaluacion[key]=valor
                else:
                    lista=elementos.crear_lista(content_eval, contenido)
                    filaEvla_lay.addWidget(lista)
                    self.elementos_evaluacion[key]=lista
            else:
                etiqueta=QLabel(contenido)
                filaEvla_lay.addWidget(etiqueta)

            grupoFinanciera_layout.addWidget(filaEvla)

        return content_eval

    def contenido_esenario(self):
        content_escenario = QFrame()
        #content_escenario.setStyleSheet(f"background-color: {(240, 240, 240)};")
        content_escenario.setStyleSheet("""
                QFrame {
                    background-color: #f4f6f7;
                }
                QGroupBox {
                    font-weight: bold;
                    font-size: 12px;
                    border: 1px solid #dcdcdc;
                    border-radius: 6px;
                    margin-top: 15px;
                    background-color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 15px;
                    padding: 2px 12px;
                    background-color: #B22222;
                    color: white;
                    border-radius: 4px;
                }
                QLabel {
                    color: #4b5563;
                    font-size: 11px;
                    font-weight: 500;
                }
                QLineEdit {
                    border: none;
                    border-bottom: 2px solid #e5e7eb;
                    background-color: #f9fafb;
                    padding: 4px;
                    color: #1f2937;
                    font-family: 'Consolas', monospace; /* Fuente técnica */
                    font-size: 12px;
                }
            """)
        contenteval_layout = QGridLayout(content_escenario)

        self.grupos={}
        self.grupos_layouts={}


        #Sub Grupos
        etiquetas_grupos={
                            "descripcion":("Descripción", 0,0,"descripcion_lay"),
                            "EstReser":("Estimación de reservas", 0,1,"EstReser_lay"),
                            "PronosPro":("Pronostico de producción", 0,2,"PronosPro_lay"),
                            "SoporPorud":("Soportes de producción", 0,3,"SoporPorud_lay"),
                            "DesProdu":("Destino de la producción", 1,0,"DesProdu_lay"),
                            "EYTProduc":("Envío y separación de la producción", 1,1,"EYTProduc_lay"),
                            "DuctosRe":("Ductos requeridos", 1,2,"DuctosRe_lay"),
                            "Evaleco":("Evaluación económica", 1,3,"Evaleco_lay"),
                            }

        for key,(nombre, x,y, lay) in etiquetas_grupos.items():
            grupo=QGroupBox(content_escenario)
            grupo.setTitle(nombre)
            layo=QVBoxLayout(grupo)
            self.grupos[key]=grupo
            self.grupos_layouts[lay]=layo
            contenteval_layout.addWidget(grupo, x,y)

        #Contenido
        self.items={}

        etiquetas_items={#descripción
                         "ETfluido":("Tipo de fluido", None),
                         "ETapi": ("° API", None),
                         "ETambiente": ("Ambiente de sedimentación", None),
                         "ETyaci": ("Tipo de yacimiento", None),
                         "ETsimilitud": ("Campo de mayor similitud", None),
                         #Estimacion de reservas
                         "ETvolOriAc": ("Volumen original de aceite (MMbbl)", None),
                         "ETvolOriGa": ("Volumen original de gas (MMMpc)", None),
                         "ETraceite": ("Reservas 2P de acite (MMbbl)",None),
                         "ETrgas": ("Reservas 2P de gas (MMMpc)",None),
                         #Pronosticos de producción
                         "ETnpozos": ("Numero de pozos", None),
                         "ETqomax": ("Qomax (Mbpd)", None),
                         "ETqgmax": ("Qgmax (MMpcd)", None),
                         "ETqwmax": ("Qwmax (Mbpd)", None),
                         #soportes de produccióin
                         "ETunoseis": ("Macropera 16 pozos", None),
                         "ETunodos": ("Macropera 12 pozos", None),
                         "ETseis": ("Macropera 6-4 pozos", None),
                         "ETdos": ("Macropera 3-2 pozos", None),
                         "ETuno": ("Pera 1 pozo", None),
                         #Destino de la produccion
                         "ETproduc": ("Tipo de producción", None),
                         "ETinstarecep": ("Instalación receptora", None),
                         "ETlong": ("Distancia (km)", None),
                         "ETpsalida": ("Presión de salida (kg/cm2)", None),
                         "ETpllegada": ("Presión de llegada (kg/cm2)", None),
                         #Envio y separacion
                         "ETpresion": ("Tipo de bombeo", None),
                         "ETseparadorR": ("Separador remoto", None),
                         "ETBateSepa": ("Batería de separación", None),
                         "ETseparadores": ("Total separadores de 1ra y 2da etapa", None),
                         "ETrectificadores": ("Total rectificadores de 1ra y 2da etapa", None),
                         #evaluacion financiera
                         "ETingreso": ("Ingreso Neto (MMUSD)", None),
                         "ETegreso": ("Egreso Neto (MMUSD)", None),
                         "ETvpn": ("vpn", None),
                         "ETtir": ("TIR", None),

        }

        for i, (key,(etiqueta,_)) in enumerate(etiquetas_items.items(), start=1):
            filaET=QFrame(content_escenario)
            filaET_lat=QHBoxLayout(filaET)

            label=QLabel(etiqueta)
            label.setFixedWidth(200)
            filaET_lat.addWidget(label)

            valor=elementos.crear_lineEditFijo(filaET)
            self.items[key]=valor
            filaET_lat.addWidget(valor)

            if i<6:
                self.grupos_layouts["descripcion_lay"].addWidget(filaET)
            elif 5<i<10:
                self.grupos_layouts["EstReser_lay"].addWidget(filaET)
            elif 9<i<14:
                self.grupos_layouts["PronosPro_lay"].addWidget(filaET)
            elif 13<i<19:
                self.grupos_layouts["SoporPorud_lay"].addWidget(filaET)
            elif 18<i<24:
                self.grupos_layouts["DesProdu_lay"].addWidget(filaET)
            elif 23<i<29:
                self.grupos_layouts["EYTProduc_lay"].addWidget(filaET)
            else:
                self.grupos_layouts["Evaleco_lay"].addWidget(filaET)



        return content_escenario