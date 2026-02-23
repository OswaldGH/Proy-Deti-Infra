from PySide6.QtWidgets import (QPushButton, QGridLayout, QVBoxLayout,
                               QGroupBox, QHBoxLayout, QFrame, QLabel, QButtonGroup,
                               QStackedLayout, QWidget, QLineEdit, QTextEdit)
from PySide6.QtCore import QDate,Qt

from complementos import elementos
from PySide6.QtGui import QPixmap,QFont
from core.CoreUI import (barraNav,UIcoreInsta)
import os


class seccion_instalaciones(elementos):

    def cargar_contenido(self, tab):
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =================BOTONES DE BARRA DE NAVEGACION==================================
        bonotes_barra = ["Manejo de la producción",
                         "Red de transporte",
                         "Separadores",
                         "Analisis hidraulico",
                         "Diagrama de flujo"]

        self.barra_opciones, self.botones_barra = elementos.barra_lateral(tab, bonotes_barra)
        layout.addWidget(self.barra_opciones)

        self.botones_barra["Salir"].clicked.connect(barraNav.cerrar_barra)

        #===================== SECCION MANEJO DE LA PRODUCCIÓN =============================
        self.cont_Menajo = self.contenido_Manejo()
        layout.addWidget(self.cont_Menajo)

        #======================= SECCIÓN RED DE TRANSPORTE =================================
        self.cont_red= self.contenido_red_transporte()
        layout.addWidget(self.cont_red)

        #======================= SECCIÓN SEPARADORES =======================================
        self.cont_separadores = self.contenido_separadores()
        layout.addWidget(self.cont_separadores)

        #======================= SECCIÓN ANÁLISIS HIDRÁULICO ================================
        self.cont_analisis = self.contenido_AH()
        layout.addWidget(self.cont_analisis)

        self.cont_Menajo.show()
        self.cont_red.hide()
        self.cont_separadores.hide()
        self.cont_analisis.hide()

        nav=barraNav()

        for nombre,boton in self.botones_barra.items():
            if nombre !="Salir":
                boton.clicked.connect(lambda _, n=nombre: nav.cambiaPestañaIns(self, n))



    def contenido_Manejo(self):
        content_frame = QFrame()
        content_frame.setStyleSheet(f"background-color: {(240, 240, 240)};")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setSpacing(0)

        #=================== SOPORTES DE PRODUCCIÓN ==========================================
        soportesProduccion_Grupo=QGroupBox(content_frame)
        soportesProduccion_layout = QHBoxLayout(soportesProduccion_Grupo)

        #carga de diagramas
        imagen=QGroupBox(content_frame)
        imagen_layout = QVBoxLayout(imagen)

        imagenEstructura = elementos.crear_imagen_estructura(content_frame)
        imagen_layout.addWidget(imagenEstructura)

        estructuras={"MPdiseis":("Macropera 16 pozos",0,0),
                     "MPdoce":("Macropera 12 pozos",1,0),
                     "MPSeis":("Macropera 6 pozos",0,1),
                     "PunPozo":("Pera un pozo",1,1)
        }

        self.btnsMacroP={}
        areaBotonesPeras=QFrame(content_frame)
        areaBotonesPeras_layout = QGridLayout(areaBotonesPeras)

        for key,(boton,x,y) in estructuras.items():
            btn=QPushButton(boton)
            self.btnsMacroP[key]=btn
            areaBotonesPeras_layout.addWidget(btn,x,y)
        imagen_layout.addWidget(areaBotonesPeras)

        soportesProduccion_layout.addWidget(imagen)

        #estimacion de peras

        soportes_grupo=QGroupBox(content_frame)
        soportes_layout = QVBoxLayout(soportes_grupo)

        textSoprtes=(f'Seleccione una de las tres opciones estimadas por la herrmienta,\n'
                     f'o bien defina su propia configuracion con la opción 4')
        infoSoprtes=QLabel(textSoprtes)
        soportes_layout.addWidget(infoSoprtes)

        self.items_Soportes={}

        estiquetas_items_soportes={"OpOneSopor":("Opción 1",0,0),
                                   "OpDosSopor":("Opción 2",0,1),
                                   "OpTreSopor":("Opción 3",1,0),
                                   "OpCauSopor":("Opcion 4",1,1),
                                   "btnEsitmarSopor":("Estimar",None,None),
                                   "MpOneSix":("Macropera 16 pozos",None,None),
                                   "MpOneTwo":("Macropera 12 pozos",None,None),
                                   "MpSeisCua":("Macropera 6-4 pozos",None,None),
                                   "MptreDos":("Macropera 2-3 pozos",None,None),
                                   "PeraOne":("Pera un pozo",None,None),
                                   "btnRegistrar":("Registrar",None,None)
                                    }

        grupoChek=QFrame(content_frame)
        grupoChek_layout = QGridLayout(grupoChek)
        soportes_layout.addWidget(grupoChek)

        for i,(key,(etiqueta,x,y)) in enumerate(estiquetas_items_soportes.items()):

            if i<4:
                OpRB=elementos.crear_radio(content_frame, etiqueta)
                self.items_Soportes[key]=OpRB
                grupoChek_layout.addWidget(OpRB, x,y)
            elif i==4:
                btn_uno_sopor=QPushButton(etiqueta)
                self.items_Soportes[key]=btn_uno_sopor
                soportes_layout.addWidget(btn_uno_sopor)
            elif 4 < i < 10:
                filaNume=QFrame(content_frame)
                filaNume_layout = QHBoxLayout(filaNume)

                etiquetaSoprtes=elementos.crear_etiqueta(content_frame, etiqueta)
                filaNume_layout.addWidget(etiquetaSoprtes)

                value=elementos.crear_lineEditFijo(content_frame)
                self.items_Soportes[key]=value
                filaNume_layout.addWidget(value)

                soportes_layout.addWidget(filaNume)
            else:
                btn_dos_sopor=QPushButton(etiqueta)
                self.items_Soportes[key]=btn_dos_sopor
                soportes_layout.addWidget(btn_dos_sopor)

        soportesProduccion_layout.addWidget(soportes_grupo)
        #============================ ENVIO DE LA PRODUCCIÓN =================================
        envioProduccion_grupo = QGroupBox(content_frame)
        envioProduccion_layout = QVBoxLayout(envioProduccion_grupo)

        self.items_envio={}
        etiquetas_items_envio={
                                "WSPresNa":("Sin separación a\n presión natural",0,0,None),
                                "WSPump":("Sin separación\n con bombeo",1,0,None),
                                "SepaRemo":("Separación romota",0,1,None),
                                "sepConBat":("Batería de separación", 1,1,None),
                                "typeFlow": ("Tipo de fluido",None,None, ["Mezcla","Liquido","Gas"]),
                                "NameInsR":("Nombre de instalación receptora",None,None,None),
                                "DisInsR":("Distancia a instalación\n receptora (km)",None,None,None),
                                "PresOpInsR":("Presión de operacion\ninstalación receptora (kg/cm²)",None,None,None),
                                "PresSalInsN":("Presión de salida\ninstalación nueva (kg/cm²)",None,None,None),
                                "TempLLegaInsR":("Temperatura de llegada\na instalación receptora (°C)",None,None,None),
                                "ViscoOil":("Viscosidad del aceite (cP)",None,None,None),
                                "ViscoGas":("Viscosidad del gas (cP)",None,None,None)
        }

        separacion_grupo=QGroupBox(envioProduccion_grupo)
        separacion_layout = QGridLayout(separacion_grupo)

        envio_grupo=QGroupBox(content_frame)
        envia_grupo_layout = QVBoxLayout(envio_grupo)

        def etiquetaFun(self, texto):
            et=QLabel(texto)
            et.setFixedSize(190,35)
            return et
        for j,(key,(etiqueta,x,y,list)) in enumerate(etiquetas_items_envio.items()):
            if j<4:
                rboton=elementos.crear_radio(content_frame, etiqueta)
                self.items_envio[key]=rboton
                separacion_layout.addWidget(rboton,x,y)
            else:
                filaEnvio = QFrame(content_frame)
                filaEnvio_layout = QHBoxLayout(filaEnvio)

                if j==4:
                    etilis=etiquetaFun(content_frame, etiqueta)
                    filaEnvio_layout.addWidget(etilis)

                    lista=elementos.crear_lista(content_frame, list)
                    self.items_envio[key]=lista
                    filaEnvio_layout.addWidget(lista)
                elif 4 < j < 12:
                    etiquetaEnvio=etiquetaFun(content_frame, etiqueta)
                    filaEnvio_layout.addWidget(etiquetaEnvio)

                    valorEntrada=elementos.crear_lineEdit(content_frame)
                    self.items_envio[key]=valorEntrada
                    filaEnvio_layout.addWidget(valorEntrada)
                envia_grupo_layout.addWidget(filaEnvio)

        btn_envioR = QPushButton("Registrar")
        self.items_envio[key] = btn_envioR
        envia_grupo_layout.addWidget(btn_envioR)

        envioProduccion_layout.addWidget(separacion_grupo)
        envioProduccion_layout.addWidget(envio_grupo)
        #======================== CARGA DE GRUPOS PRINCIPALES =================================
        content_layout.addWidget(soportesProduccion_Grupo)
        content_layout.addWidget(envioProduccion_grupo)

        return content_frame

    def contenido_red_transporte(self):

        content_red = QFrame()
        content_red.setStyleSheet(f"background-color: {(240, 240, 240)};")
        content_layout = QHBoxLayout(content_red)
        content_layout.setSpacing(3)

        controlador=QGroupBox(content_red)
        controlador_layout = QVBoxLayout(controlador)

        self.grupo_componente=QButtonGroup(content_red)
        self.grupo_componente.setExclusive(True)

        self.opciones_componentes_items={}
        self.opciones_componentes_etiquetas={
                                            "Viewcabezal":"Cabezales",
                                            "Viewbajante":"Linea de descarga",
                                            "Viewducto":"Ducto"
        }

        for key, etiquetaOP in self.opciones_componentes_etiquetas.items():
            radio=elementos.crear_radio(content_red, etiquetaOP)
            self.opciones_componentes_items[key]=radio
            self.grupo_componente.addButton(radio)
            controlador_layout.addWidget(radio)

        self.opciones_componentes_items["Viewcabezal"].setChecked(True)


        label_fondo = QLabel()
        pixmap = QPixmap(r"../imagenes/Cabezal.png")
        label_fondo.setPixmap(pixmap)
        label_fondo.setScaledContents(True)
        label_fondo.setFixedHeight(350)
        label_fondo.setFixedWidth(300)


        label_bajante = QLabel()
        pixmapBaja = QPixmap(r"../imagenes/Bajantepozo.png")
        label_bajante.setPixmap(pixmapBaja)
        label_bajante.setScaledContents(True)
        label_bajante.setFixedHeight(350)
        label_bajante.setFixedWidth(300)


        label_ducto = QLabel()
        pixmapDuc = QPixmap(r"../imagenes/ducto.png")
        label_ducto.setPixmap(pixmapDuc)
        label_ducto.setScaledContents(True)
        label_ducto.setFixedHeight(350)
        label_ducto.setFixedWidth(300)


        contenido=QWidget()
        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setSpacing(1)
        contenido_layout.setContentsMargins(0,0,0,0)

        #======================== BAJANTE DE POZOS ===========================================
        bajante_grupo=QGroupBox("BAJANTE DE POZO",content_red)
        bajante_layout = QVBoxLayout(bajante_grupo)

        self.item_bajante={}

        etiquetas_items_bajante={
                                 "presBaj":"Presión (kg/cm² man)",
                                 "tempBaj":"Temperatura (°C)",
                                 "WeiMolLiqBaj":"Peso molecular del liquido",
                                 "WeiMolGasBaj":"Peso molecular del gas",
                                 "QlBaj":"Gasto de liquido (bpd)",
                                 "QoBaj":"Gasto de aceite (bpd)",
                                 "QgBaj":"Gasto de gas (MMpcd)",
                                 "DiaBajCal":"Diámetro calculado (in)",
                                 "DiaBajCon":"Diámetro comercial (in)",
                                 "VeloFlowBaj":"Velocidad del flujo (ft/s)",
                                 "VeloEroBaj":"Velocidad de erosión (ft/s)",
                                 "btnCalBaj":"Calcular"
                                }

        baja_datos=QGroupBox(content_red)
        baja_datos_layout = QVBoxLayout(baja_datos)
        baja_datos_layout.setSpacing(0)

        baja_resul=QGroupBox(content_red)
        baja_result_layout = QVBoxLayout(baja_resul)
        baja_result_layout.setSpacing(0)

        for i,(key,etiqueta) in enumerate(etiquetas_items_bajante.items()):
            if i<11:
                filaBaja=QFrame(content_red)
                filaBaja_layout = QHBoxLayout(filaBaja)
                filaBaja_layout.setSpacing(0)
                filaBaja_layout.setContentsMargins(0,0,0,0)

                eti = elementos.crear_etiqueta(content_red, etiqueta)
                filaBaja_layout.addWidget(eti)

                if i<7:
                    edit=elementos.crear_lineEdit(content_red)
                    self.item_bajante[key]=edit
                    filaBaja_layout.addWidget(edit)
                    baja_datos_layout.addWidget(filaBaja)

                elif 6<i<11:
                    edit=elementos.crear_lineEditFijo(content_red)
                    self.item_bajante[key]=edit
                    filaBaja_layout.addWidget(edit)
                    baja_result_layout.addWidget(filaBaja)
            else:
                btn=QPushButton(etiqueta)
                self.item_bajante[key]=btn
                baja_result_layout.addWidget(btn)

        bajante_layout.addWidget(baja_datos)
        bajante_layout.addWidget(baja_resul)
        #============================== TIPO DE CABEZAL ======================================

        cabezal_grupo=QGroupBox("CABEZALES DE PRODUCCIÓN",content_red)
        cabezal_layout = QVBoxLayout(cabezal_grupo)

        #  CONTROL TIPO DE CABEZAL
        controlCabezal = QGroupBox()
        controlCabezal.setFixedHeight(50)
        controlCabezal_layout = QHBoxLayout(controlCabezal)
        controlCabezal_layout.setSpacing(15)
        controlCabezal_layout.setContentsMargins(0, 0, 0, 0)

        opciones_cabezal = [
            ("Producción", "check_Produ", "ViewProdu"),
            ("Prueba", "check_Prueba", "Viewprueba"),
        ]

        for texto, check_attr, radio_attr in opciones_cabezal:
            layout_opcion = QHBoxLayout()
            layout_opcion.setSpacing(0)
            layout_opcion.setContentsMargins(0, 0, 0, 0)

            check = elementos.crear_check(content_red)
            radio = elementos.crear_radio(content_red, texto)

            setattr(self, check_attr, check)
            setattr(self, radio_attr, radio)

            layout_opcion.addWidget(check)
            layout_opcion.addWidget(radio)
            layout_opcion.addStretch()

            controlCabezal_layout.addLayout(layout_opcion)

        cabezal_layout.addWidget(controlCabezal)

        self.items_cabezal={}

        etiquetas_items_cabezal={
                                 "presCab": "Presión (kg/cm² man)",
                                 "tempCab": "Temperatura (°C)",
                                 "WeiMolLiqCab": "Peso molecular del liquido",
                                 "WeiMolGasCab": "Peso molecular del gas",
                                 "QlCab": "Gasto de liquido (bpd)",
                                 "QoCab": "Gasto de aceite (bpd)",
                                 "QgCab": "Gasto de gas (MMpcd)",
                                 "DiaCabCal": "Diámetro calculado (in)",
                                 "DiaCabCon": "Diámetro comercial (in)",
                                 "VeloFlowCab": "Velocidad del flujo (ft/s)",
                                 "VeloEroCab": "Velocidad de erosión (ft/s)",
                                 "btnCalCab": "Calcular"
                                }

        cabezal_datos = QGroupBox(content_red)
        cabezal_datos_layout = QVBoxLayout(cabezal_datos)
        cabezal_datos_layout.setSpacing(0)

        cabezal_resul = QGroupBox(content_red)
        cabezal_result_layout = QVBoxLayout(cabezal_resul)
        cabezal_result_layout.setSpacing(0)

        for i,(key,etiqueta) in enumerate(etiquetas_items_cabezal.items(),start=0):

            if i<11:
                filaCabe=QFrame(content_red)
                filaCabe_layout = QHBoxLayout(filaCabe)
                filaCabe_layout.setSpacing(0)
                filaCabe_layout.setContentsMargins(0,0,0,0)

                eti = elementos.crear_etiqueta(content_red, etiqueta)
                filaCabe_layout.addWidget(eti)

                if i<7:
                    edit=elementos.crear_lineEdit(content_red)
                    self.items_cabezal[key]=edit
                    filaCabe_layout.addWidget(edit)
                    cabezal_datos_layout.addWidget(filaCabe)

                elif 6<i<11:
                    edit=elementos.crear_lineEditFijo(content_red)
                    self.items_cabezal[key]=edit
                    filaCabe_layout.addWidget(edit)
                    cabezal_result_layout.addWidget(filaCabe)
            else:
                btn=QPushButton(etiqueta)
                self.items_cabezal[key]=btn
                cabezal_result_layout.addWidget(btn)

        #print(self.item_bajante)
        #print(self.items_cabezal)
        cabezal_layout.addWidget(cabezal_datos)
        cabezal_layout.addWidget(cabezal_resul)

        #================================= SERVICIO DE DUCTO =================================
        servicio_grupo=QGroupBox("DUCTO",content_red)
        servicio_layout = QVBoxLayout(servicio_grupo)

        controlServico = QGroupBox()
        controlServico.setFixedHeight(50)
        controlServico_layout = QHBoxLayout(controlServico)
        controlServico_layout.setSpacing(15)
        controlServico_layout.setContentsMargins(0, 0, 0, 0)

        self.grupo_servicio = QButtonGroup(content_red)
        self.grupo_servicio.setExclusive(True)

        self.opciones_servicio_items={}
        opciones_servicio_etiqueta={
                           "ViewOleogaso":"Oleogasoducto",
                           "ViewOleo":"Oleoducto",
                           "ViewGas":"Gasoducto"
                            }
        for key,etiqueta in opciones_servicio_etiqueta.items():
            RB=elementos.crear_radio(content_red,etiqueta)
            self.opciones_servicio_items[key]=RB
            self.grupo_servicio.addButton(RB)
            controlServico_layout.addWidget(RB)

        self.opciones_servicio_items["ViewOleogaso"].setChecked(True)

        #OLEGASODUCTO
        self.oleo_Items={}

        oleo_etiquetas={"apiServi":"°API",
                        "presServi": "Presión (kg/cm² man)",
                        "TemServi": "Temperatura (°C)",
                        "WmolLiqServi": "Peso molecular del líquido",
                        "WmolGasServi": "Peso molecular del gas",
                        "flowLiqServi": "Flujo de líquidos (bpd)",
                        "flowoilServi": "Flujo de aceite (bpd)",
                        "flowGasServi": "Flujo de gas (MMpcd)",
                        "diamCalServi":"Diámetro calculado (pulg)",
                        "diamComServi": "Diámetro comercial (pulg)",
                        "velCalServi": "Velocidad calculada (ft/s)",
                        "velEroServi": "Velocidad de erosión (ft/s)",
                        "PresEntServi": "Presión de entrada (kg/cm²)",
                        "PresSalServi": "Presión de salida (kg/cm²)",
                        "dpServi": "DP (kg/cm²)",
                        "btnCalServi": "Calcular"
                        }

        oleo_datos = QGroupBox(content_red)
        oleo_datos_layout = QVBoxLayout(oleo_datos)
        oleo_datos_layout.setSpacing(0)
        oleo_datos_layout.setContentsMargins(5,0,5,0)

        oleo_resul = QGroupBox(content_red)
        oleo_resul_layout = QVBoxLayout(oleo_resul)
        oleo_resul_layout.setSpacing(0)
        oleo_resul_layout.setContentsMargins(5,0,5,0)

        for i,(key,etiqueta) in enumerate(oleo_etiquetas.items()):
            filaoleo=QFrame(content_red)
            filaoleo_layout = QHBoxLayout(filaoleo)
            filaoleo_layout.setContentsMargins(0,0,0,0)
            filaoleo_layout.setSpacing(0)

            etiquetaOleo=elementos.crear_etiqueta(content_red,etiqueta)
            valorOleo=elementos.crear_lineEdit(content_red)
            self.oleo_Items[key]=valorOleo

            filaoleo_layout.addWidget(etiquetaOleo)
            filaoleo_layout.addWidget(valorOleo)

            if i<8:
                oleo_datos_layout.addWidget(filaoleo)
            else:
                oleo_resul_layout.addWidget(filaoleo)


            if i==15:
                btn=QPushButton(etiqueta)
                self.oleo_Items[key]=btn
                oleo_resul_layout.addWidget(btn)

        #oilducto
        self.oil_Items = {}

        oil_etiquetas = {"apiServio": "°API",
                          "flowoilServio": "Flujo de aceite (bpd)",
                          "diamCalServio": "Diámetro calculado (pulg)",
                          "diamComServio": "Diámetro comercial (pulg)",
                          "velCalServio": "Velocidad calculada (ft/s)",
                          "PresEntServio": "Presión de entrada (kg/cm²)",
                          "PresSalServio": "Presión de salida (kg/cm²)",
                          "dpServio": "DP (kg/cm²)",
                          "btnCalServiOilo": "Calcular"
                          }

        oil_datos = QGroupBox(content_red)
        oil_datos_layout = QVBoxLayout(oil_datos)

        oil_resul = QGroupBox(content_red)
        oil_resul_layout = QVBoxLayout(oil_resul)


        for i,(key,etiqueta) in enumerate(oil_etiquetas.items()):
            filaoil = QFrame(content_red)
            filaoil_layout = QHBoxLayout(filaoil)

            etiquetaoil = elementos.crear_etiqueta(content_red, etiqueta)
            valoroil = elementos.crear_lineEdit(content_red)
            self.oil_Items[key] = valoroil

            filaoil_layout.addWidget(etiquetaoil)
            filaoil_layout.addWidget(valoroil)

            if i<4:
                oil_datos_layout.addWidget(filaoil)
            else:
                oil_resul_layout.addWidget(filaoil)
                if i==8:
                    btnoil = QPushButton(etiqueta)
                    self.oil_Items[key]=btnoil
                    oil_resul_layout.addWidget(btnoil)


        #GASODUCTO
        self.gas_Items = {}

        gas_etiquetas = {
                         "flowgasServig": "Flujo de gas (MMcpd)",
                         "TempgasServig": "Temperatura (°C)",
                         "WmolGasServiG": "Peso molecular del gas",
                         "diamCalServig": "Diámetro calculado (pulg)",
                         "diamComServig": "Diámetro comercial (pulg)",
                         "velCalServig": "Velocidad calculada (ft/s)",
                         "PresEntServig": "Presión de entrada (kg/cm²)",
                         "PresSalServig": "Presión de salida (kg/cm²)",
                         "dpServig": "DP (kg/cm²)",
                         "btnCalServiOilg": "Calcular"
                         }

        gas_datos = QGroupBox(content_red)
        gas_datos_layout = QVBoxLayout(gas_datos)

        gas_resul = QGroupBox(content_red)
        gas_resul_layout = QVBoxLayout(gas_resul)
        for i, (key, etiqueta) in enumerate(gas_etiquetas.items()):
            filaGas = QFrame(content_red)
            filaGas_layout = QHBoxLayout(filaGas)

            etiquetaGas = elementos.crear_etiqueta(content_red, etiqueta)
            valorGas = elementos.crear_lineEdit(content_red)
            self.gas_Items[key] = valorGas
            filaGas_layout.addWidget(etiquetaGas)
            filaGas_layout.addWidget(valorGas)

            if i<3:
                gas_datos_layout.addWidget(filaGas)
            else:
                gas_resul_layout.addWidget(filaGas)
                if i==9:
                    btnoGas = QPushButton(etiqueta)
                    self.gas_Items[key]=btnoGas
                    gas_resul_layout.addWidget(btnoGas)


        #Cargas de layout
        self.oleo_datos = oleo_datos
        self.oleo_resul = oleo_resul
        self.oil_datos = oil_datos
        self.oil_resul = oil_resul
        self.gas_datos = gas_datos
        self.gas_resul = gas_resul

        servicio_layout.addWidget(controlServico)
        servicio_layout.addWidget(self.oleo_datos)
        servicio_layout.addWidget(self.oleo_resul)
        servicio_layout.addWidget(self.oil_datos)
        servicio_layout.addWidget(self.oil_resul)
        servicio_layout.addWidget(self.gas_datos)
        servicio_layout.addWidget(self.gas_resul)

        oleo_datos.show()
        oleo_resul.show()
        oil_datos.hide()
        oil_resul.hide()
        gas_datos.hide()
        gas_resul.hide()

        funt = UIcoreInsta()

        for nombre, rb in self.opciones_servicio_items.items():
            rb.toggled.connect(
                lambda estado, n=nombre: estado and funt.cambiar_servicio(self, n)
            )
        #========================= AGREGAR GRUPOS PRINCIPALES =================================
        content_layout.addWidget(controlador)
        content_layout.addWidget(contenido)

        self.cabezal_grupo=cabezal_grupo
        self.bajante_grupo=bajante_grupo
        self.servicio_grupo=servicio_grupo



        contenido_layout.addWidget(self.cabezal_grupo)
        contenido_layout.addWidget(self.bajante_grupo)
        contenido_layout.addWidget(self.servicio_grupo)

        cabezal_grupo.show()
        bajante_grupo.hide()
        servicio_grupo.hide()

        self.label_fondo = label_fondo
        self.label_bajante = label_bajante
        self.label_ducto = label_ducto

        controlador_layout.addWidget(self.label_fondo)
        controlador_layout.addWidget(self.label_bajante)
        controlador_layout.addWidget(self.label_ducto)

        label_fondo.show()
        label_bajante.hide()
        label_ducto.hide()

        def cambiar_imagen():
            if self.opciones_componentes_items["Viewcabezal"].isChecked():
                label_fondo.show()
                label_bajante.hide()
                label_ducto.hide()

            elif self.opciones_componentes_items["Viewbajante"].isChecked():
                label_fondo.hide()
                label_bajante.show()
                label_ducto.hide()

            elif self.opciones_componentes_items["Viewducto"].isChecked():
                label_fondo.hide()
                label_bajante.hide()
                label_ducto.show()

        for rb in self.opciones_componentes_items.values():
            rb.toggled.connect(cambiar_imagen)

        for nombre, rb in self.opciones_componentes_items.items():
            rb.toggled.connect(
                lambda estado, n=nombre: estado and funt.cambiar_componente(self, n)
            )




        return content_red

    def contenido_separadores(self):
        content_sep = QFrame()
        content_sep.setStyleSheet(f"background-color: {(240, 240, 240)};")
        contentsep_layout = QHBoxLayout(content_sep)
        contentsep_layout.setSpacing(3)

        #========================= CONTROLADOR DE SEPARADORES ===============================
        botonesSeparadores = QGroupBox(content_sep)
        botonesSeparadores.setFixedWidth(400)
        botonesSeparadoresLay=QHBoxLayout(botonesSeparadores)

        controlSeparadores = QGroupBox()
        controlSeparadores_lay = QVBoxLayout(controlSeparadores)


        self.grupo_sepa = QButtonGroup(content_sep)
        self.grupo_sepa.setExclusive(True)

        self.opciones_separadores_items = {}
        opciones_separadores_etiqueta = {
            "ViewSepPrueba": "Separador de prueba",
            "ViewSepRemo": "Separador remoto",
            "ViewSepFirsStep": "Separador de primera etapa",
            "ViewSepSecStep":"Separador de segunda etapa",
            "ViewRetFirStep": "Rectificador de primera etapa",
            "ViewRetSecStep": "Rectificador de segunda etapa",
        }
        for key, etiqueta in opciones_separadores_etiqueta.items():
            RB = elementos.crear_radio(content_sep, etiqueta)
            self.opciones_separadores_items[key] = RB
            self.grupo_sepa.addButton(RB)
            controlSeparadores_lay.addWidget(RB)

        self.opciones_separadores_items["ViewSepPrueba"].setChecked(True)

        label_fondo = QLabel()
        pixmap = QPixmap(r"../imagenes/separador.png")
        label_fondo.setPixmap(pixmap)
        label_fondo.setScaledContents(True)
        label_fondo.setFixedHeight(250)
        label_fondo.setFixedWidth(360)

        controlSeparadores_lay.addWidget(label_fondo)
        botonesSeparadoresLay.addWidget(controlSeparadores)
        # ========================= CONTENIDO DE SEPARADORES ================================
        contenidoSeparadores = QGroupBox(content_sep)
        contenidoSeparadores_lay = QVBoxLayout(contenidoSeparadores)

        #Gurpo superior
        partSup=QFrame(content_sep)
        partSup_lay = QHBoxLayout(partSup)

        gruSupDat=QGroupBox("Datos",content_sep)
        gruSupDat_lay = QVBoxLayout(gruSupDat)

        grupoSupCal=QGroupBox("Dimencionamiento", content_sep)
        grupoSupCal_lay = QVBoxLayout(grupoSupCal)

        #Componentes inferiores
        grupResInf=QGroupBox("Resultados",content_sep)
        grupResInf_lay = QHBoxLayout(grupResInf)

        frameResul=QFrame(content_sep)
        FrameResul_lay = QVBoxLayout(frameResul)

        self.separadores_Items={}

        separadores_Etiquetas={"SepApi":"°API",
                               "SepPres": "Presión (Kg/cm² man)",
                               "SepTemp": "Temperatura (°C)",
                               "SepWmoliq": "Peso molecular de líquido",
                               "SepWmoGas": "Peso molecular de gas",
                               "SepZ": "Factor de compresbilidad",
                               "SepLiqFlow": "Flujo de líquido (bpd)",
                               "SepOilFlow": "Flujo de aceite (bpd)",
                               "SepGasFlow": "Flujo de gas (MMpcd)",
                               "SepDiam": "Diámetro (ft)",
                               "SepLong": "Longitud (Ft)",
                               "SepLD": "L/d",
                               "SepLiqFlowR": "Flujo de líquido (bpd)",
                               "SepAreaDisp": "Area disponible (ft²)",
                               "SepAreaReq": "Area requerida (ft²)",
                               "SepBtnCal": "Calcular",
                               "SepBtnReg": "Registrar"
                              }

        for i,(key, etiqueta) in enumerate(separadores_Etiquetas.items()):
            if i<15:
                filaSep = QFrame(content_sep)
                filaSep_lay = QHBoxLayout(filaSep)

                etiquetas = elementos.crear_etiqueta(content_sep, etiqueta)
                filaSep_lay.addWidget(etiquetas)
                val = elementos.crear_lineEdit(content_sep)
                self.separadores_Items[key] = val
                filaSep_lay.addWidget(val)

                if i<6:
                    gruSupDat_lay.addWidget(filaSep)
                elif 5<i<12:
                    grupoSupCal_lay.addWidget(filaSep)
                else:
                    FrameResul_lay.addWidget(filaSep)
            else:
                btnS=QPushButton(etiqueta)
                self.separadores_Items[key]=btnS
                FrameResul_lay.addWidget(btnS)



        partSup_lay.addWidget(gruSupDat)
        partSup_lay.addWidget(grupoSupCal)
        grupResInf_lay.addWidget(frameResul)
        contenidoSeparadores_lay.addWidget(partSup)
        contenidoSeparadores_lay.addWidget(grupResInf)
        # ========================= CARGA DE VENTANAS PRINCIPALES ===========================
        contentsep_layout.addWidget(botonesSeparadores)
        contentsep_layout.addWidget(contenidoSeparadores)

        return content_sep

    def contenido_AH(self):
        content_AH = QFrame()
        content_AH.setStyleSheet(f"background-color: {(240, 240, 240)};")
        contentAH_layout = QVBoxLayout(content_AH)
        contentAH_layout.setSpacing(0)

        #contenido diagrama
        espacio_diagrama = QFrame(content_AH)
        espacio_lay = QVBoxLayout(espacio_diagrama)

        #nombre de las instalaciones
        nombres=QFrame(content_AH)
        nombres_lay = QHBoxLayout(nombres)
        nombres_lay.setSpacing(0)
        nombres_lay.setContentsMargins(0, 0, 0, 0)

        fuenteN = QFont()
        fuenteN.setPointSize(15)
        fuenteN.setBold(True)
         #Instalación Nueva
        nueva=QFrame(content_AH)
        nueva_lay = QVBoxLayout(nueva)
        nueva_lay.setSpacing(0)


        textoN=QLabel("Instalación nueva:")
        textoN.setFont(fuenteN)
        #textoN.setAlignment(Qt.AlignCenter)
        nueva_lay.addWidget(textoN)

        nombres_Instalacion_N=QLabel("Prueba")
        nombres_Instalacion_N.setFont(fuenteN)
        nueva_lay.addWidget(nombres_Instalacion_N)

         #Instalacion receptora
        receptora=QFrame(content_AH)
        receptora_lay = QVBoxLayout(receptora)
        receptora_lay.setSpacing(0)

        texr=QLabel("Instalación receptora:")
        texr.setFont(fuenteN)

        receptora_lay.addWidget(texr)
        nombres_Instalacion_R = QLabel("Prueba")
        nombres_Instalacion_R.setFont(fuenteN)
        receptora_lay.addWidget(nombres_Instalacion_R)

        nombres_lay.addWidget(nueva)
        nombres_lay.addWidget(receptora)

        espacio_lay.addWidget(nombres)

        #diagrama de las intalaciones
        imagens=QFrame(content_AH)
        imagens.setMaximumHeight(380)

        stack = QStackedLayout(imagens)
        stack.setStackingMode(QStackedLayout.StackAll)
        # ================== FONDO ==================
        label_fondo = QLabel()
        pixmap = QPixmap(r"../imagenes/Diagrama_AH.png")
        label_fondo.setPixmap(pixmap)
        label_fondo.setScaledContents(True)
        label_fondo.setAlignment(Qt.AlignCenter)
        label_fondo.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # ================== CAPA SUPERIOR ==================
        overlay = QWidget()
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        # Ejemplo de item encima
        diametro=0
        lon=0
        texto =f'{diametro} Ø x {lon} Km'
        tex = QLabel(texto,overlay)
        fuente = QFont()
        fuente.setPointSize(20)
        fuente.setBold(True)

        tex.setFont(fuente)
        tex.setAlignment(Qt.AlignCenter)

        tex.move(280, 230)
        tex.setFixedSize(250, 25)

        # ================== ENSAMBLE ==================
        stack.addWidget(label_fondo)  # fondo
        stack.addWidget(overlay)

        espacio_lay.addWidget(imagens)

        #carga de grupos secuandrios
        contentAH_layout.addWidget(espacio_diagrama)

        #Contenido resultados
        self.itemsAH={}

        etiquetas={
                    #datos nueva
                    "AHpresN":"Presión (kg/cm2man.",
                    "AHtemN":"Temperatura (°C)",
                    "AHqliN":"Gasto de liquido (Mbpd)",
                    "AHqgasN":"Gasto de gas (MMpcd)",
                    #Datos receptoes
                    "AHpresR": "Presión (kg/cm2man.",
                    "AHtemR": "Temperatura (°C)",
                    "AHqliR": "Gasto de liquido (Mbpd)",
                    "AHqgasR": "Gasto de gas (MMpcd)",

        }

        espacio_resultados=QFrame(content_AH)
        espacio_resultados_lay=QHBoxLayout(espacio_resultados)

        #resultados nuevo
        r_nueva=QGroupBox(content_AH)
        r_nueva_lay=QVBoxLayout(r_nueva)
        r_nueva_lay.setSpacing(1)

        #resultados receptores
        r_recep = QGroupBox(content_AH)
        r_rece_lay = QVBoxLayout(r_recep)
        r_rece_lay.setSpacing(1)



        for i,(key,etiqueta) in enumerate(etiquetas.items()):
            fila=QFrame(content_AH)
            fila_lay=QHBoxLayout(fila)

            etiquetas=elementos.crear_etiqueta(content_AH,etiqueta)
            etiquetas.setFixedWidth(219)
            fila_lay.addWidget(etiquetas)

            valor=elementos.crear_lineEditFijo(content_AH)
            self.itemsAH[key]=valor
            fila_lay.addWidget(valor)

            if i<4:
                r_nueva_lay.addWidget(fila)
            else:
                r_rece_lay.addWidget(fila)

        espacio_resultados_lay.addWidget(r_nueva)
        espacio_resultados_lay.addWidget(r_recep)

        contentAH_layout.addWidget(espacio_resultados)


        return content_AH