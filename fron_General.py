from PySide6.QtWidgets import (QPushButton, QGridLayout, QVBoxLayout,
                               QGroupBox, QDateEdit, QHBoxLayout, QFrame)
from PySide6.QtCore import QDate

import tabulate as tb

from core.info_gene import extractor

#librerias propias
from complementos import elementos
from core.CoreUI import barraNav

class seccion_informacion(elementos, extractor):

    def cargar_contenido(self,tab):

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # =================BOTONES DE BARRA DE NAVEGACION==================================
        bonotes_barra=["Información General",
                        "Analogías",
                       "Reservas",
                       "Pronosticos"]

        self.barra_opciones,self.botones_barra= elementos.barra_lateral(tab,bonotes_barra)
        layout.addWidget(self.barra_opciones)

        self.botones_barra["Salir"].clicked.connect(barraNav.cerrar_barra)

        #==================SECCIÓN DE INFORMACIÓN GENERAL==================================
        self.contenido=self.contenido_general()
        layout.addWidget(self.contenido)

        # ===========================SECCIÓN ANALOGIAS=====================================
        self.contenidoAnalogias = self.contenido_analogias()
        layout.addWidget(self.contenidoAnalogias)

        #=========================== SECCIÓN RESERVAS =====================================
        self.contenidoReservas = self.contenido_reservas()
        layout.addWidget(self.contenidoReservas)

        #=========================== SECCIÓN PRONOSTICOS ==================================
        self.contenidoPronosticos = self.contenido_pronostico()
        layout.addWidget(self.contenidoPronosticos)

        #navegacion de pestañas
        self.contenido.show()
        self.contenidoAnalogias.hide()
        self.contenidoReservas.hide()
        self.contenidoPronosticos.hide()

        nav=barraNav()

        for nombre,boton in self.botones_barra.items():
            if nombre !="Salir":
                boton.clicked.connect(lambda _, n=nombre: nav.cambiaPestaña(self, n))



    def contenido_general(self):
        content_frame = QFrame()
        content_frame.setStyleSheet(f"background-color: {(240, 240, 240)};")

        content_layout = QGridLayout(content_frame)
        #content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)

        #=============== INFORMACIÓN DEL POZO==================================
        workspace_area = QGroupBox(content_frame)
        workspace_area.setFixedHeight(450)
        workspace_layout = QVBoxLayout(workspace_area)
        workspace_layout.setSpacing(0)

        self.items_general={}
        etiqueas_info_campo={"name":("Nombre del campo",None),
                             "year":("Año de descubrimiento", [str(año) for año in range(2020, 2050)]),
                             "ubi":("Ubicación", ["Terrestre", "Marino"]),
                             "region":("Región",["Norte", "Sur", "Marina Suroeste", "Marina Noroeste"]),
                             "activo_extra":("Activo de extracción", [
                                              "Ku-Maloob-Zaap", "Cantarell", "Abkatun-Pol-Chuc", "Litoral de Tabasco",
                                              "Macuspana-Muspac", "Samaria-Luna", "Bellota-Jujo", "Cinco Presidentes",
                                              "Poza Rica-Altamira", "Veracruz", "Reynosa", "Campos Estrategicos"
                                                   ]),
                             "estatus":("Estatus", ["Desarrollo", "Evaluación", "Exploración"]),
                             "inicio_perfo":("Inicio de perforación", None)
                            }


        for i,(key,(texto,opciones)) in enumerate(etiqueas_info_campo.items()):
            fila_area = QFrame(content_frame)
            fila_layout = QHBoxLayout(fila_area)

            self.etiqueta=elementos.crear_etiqueta(content_frame, texto)
            fila_layout.addWidget(self.etiqueta)

            if i==0:
                line_edit = elementos.crear_lineEdit(content_frame)
                self.items_general[key]=line_edit
                fila_layout.addWidget(line_edit)
            elif 0<i<6:
                lista=elementos.crear_lista(content_frame,opciones)
                self.items_general[key]=lista
                fila_layout.addWidget(lista)
            else:
                inicioPerfo = QDateEdit()
                self.items_general[key]=inicioPerfo
                inicioPerfo.setFixedSize(160,30)
                inicioPerfo.setDisplayFormat("dd-MM-yyyy")
                inicioPerfo.setCalendarPopup(True)
                inicioPerfo.setMinimumDate(QDate(2010, 1, 1))
                inicioPerfo.setMaximumDate(QDate(2100, 12, 31))
                inicioPerfo.setDate(QDate.currentDate())
                fila_layout.addWidget(inicioPerfo)

            fila_layout.addStretch(1)
            fila_layout.setSpacing(1)

            workspace_layout.addWidget(fila_area)

        r=tb.tabulate(self.items_general.items())
        print(r)




        #=============== INFORMACIÓN DEL YACIMIENTO ============================
        workspace2_area = QGroupBox(content_frame)
        workspace2_area.setFixedHeight(450)
        workspace2_layout = QVBoxLayout(workspace2_area)

        elementos_yacimiento={
                              "ambiente":("Ambiente de sedimentación", ["Clástica", "Carbonatada"]),
                              "yacimiento":("Yacimiento", ["Jurásico", "Cretácico", "Terciario", "Cuaternario"]),
                              "play":("Play geológico", [
                                    "Jurásico (JSK)", "Jurásico (JSK)",
                                    "Cretacico(BKS)", "Cretacico(KS)", "Cretacico(BM)", "Cretacico(BI)",
                                    "Terciario(Plioceo)", "Terciario(Mioceno)", "Terciario(Oligoceno)",
                                    "Terciario(Eoceno)", "Terciario(Paleoceno)"
                                                  ]),
                                    "porosidad":("Porosidad (%)",None),
                                    "permeabilidad":("Permeabilidad (md)",None),
                                    "fluido":("Tipo de fluido",["Aceite negro", "Aceite Volátil", "Gas y condensado"]),
                                    "api":("° API",None),
                                    "rga":("RGA (m³/m³)",None),
                                    "rgc":("RGC (m³/m³)",None),
                                    "voo":("Volumen original de aceite (MMbbl)",None),
                                    "vog":("Volumen original de gas (MMMpcd)", None)

                             }

        for j, (key,(textoYaci, opcionesYaci)) in enumerate(elementos_yacimiento.items()):
            filaYaci_area = QFrame(content_frame)
            filaYaci_layout = QHBoxLayout(filaYaci_area)

            self.etiquetaYaci = elementos.crear_etiqueta(content_frame, textoYaci)
            filaYaci_layout.addWidget(self.etiquetaYaci)

            if opcionesYaci==None:
                line_editYaci = elementos.crear_lineEdit(content_frame)
                self.items_general[key]=line_editYaci
                filaYaci_layout.addWidget(line_editYaci)
            else:
                listaYaci = elementos.crear_lista(content_frame, opcionesYaci)
                self.items_general[key]=listaYaci
                filaYaci_layout.addWidget(listaYaci)

            filaYaci_layout.addStretch(1)
            filaYaci_layout.setSpacing(1)
            workspace2_layout.addWidget(filaYaci_area)


        workspace2_layout.setSpacing(0)
        r2=tb.tabulate(self.items_general.items())
        print(r2)

        # =============== UBICACIÓN DEL POZO EXPLORATORIO ======================
        workspace3_area = QGroupBox(content_frame)
        workspace3_area.setFixedHeight(450)
        workspace3_layout = QVBoxLayout(workspace3_area)

        elementos_ubicacion={
                             "well_name":("Nombre del pozo",None),
                             "latitud":("Latitud",None),
                             "longitud":("Longitud",None),
                            }
        for k,(key,(textoUbi,estado)) in enumerate(elementos_ubicacion.items()):
            filaUbi_area = QFrame(content_frame)
            filaUbi_layout = QHBoxLayout(filaUbi_area)

            self.etiquetaUbi=elementos.crear_etiqueta(content_frame, textoUbi)
            filaUbi_layout.addWidget(self.etiquetaUbi)

            line_editUbi = elementos.crear_lineEdit(content_frame)
            self.items_general[key]=line_editUbi
            filaUbi_layout.addWidget(line_editUbi)

            filaUbi_layout.addStretch(1)
            filaUbi_layout.setSpacing(1)
            workspace3_layout.addWidget(filaUbi_area)

        self.mapa_ubi = elementos.crear_mapa(content_frame)
        workspace3_layout.addWidget(self.mapa_ubi)

        workspace3_layout.setSpacing(0)

        print(tb.tabulate(self.items_general.items()))

        # ===================== REGISTRO DE ESCENARIOS =========================
        workspace4_area = QGroupBox(content_frame)
        workspace4_layout = QVBoxLayout(workspace4_area)

        self.tablaEscenarios=elementos.crear_tabla(content_frame)
        workspace4_layout.addWidget(self.tablaEscenarios)

        btn_Area_resgistro=QGroupBox(content_frame)
        btn_Area_resgistro_layout = QHBoxLayout(btn_Area_resgistro)

        btn_guardar_registro = QPushButton("Guardar")
        btn_editar_registro=QPushButton("Editar")
        btn_eliminar_registro=QPushButton("Eliminar")

        btn_Area_resgistro_layout.addWidget(btn_guardar_registro)
        btn_Area_resgistro_layout.addWidget(btn_editar_registro)
        btn_Area_resgistro_layout.addWidget(btn_eliminar_registro)

        workspace4_layout.addWidget(btn_Area_resgistro)

        #=============== CARGA DE GRUPOS =======================================
        content_layout.setRowStretch(0,6)
        content_layout.setColumnStretch(1,4)
        content_layout.setSpacing(0)
        content_layout.addWidget(workspace_area,0,0)
        content_layout.addWidget(workspace2_area,0,1)
        content_layout.addWidget(workspace3_area, 0, 2)
        content_layout.addWidget(workspace4_area, 1,0,1,3)



        self.extractor=extractor(self.items_general)
        return content_frame

    def contenido_analogias(self):
        content_analogias = QFrame()
        content_analogias.setStyleSheet(f"background-color: {(240, 240, 240)};")
        contentAnalogias_layout = QVBoxLayout(content_analogias)
        # content_layout.setContentsMargins(20, 20, 20, 20)
        contentAnalogias_layout.setSpacing(10)

        #=====================BUSCADOR DE CAMPOS ANALOGOS===========================
        grupoSuperior_area=QGroupBox(content_analogias)
        grupoSuperior_layout = QVBoxLayout(grupoSuperior_area)

        #AREA PARA VISUALIZACIÓN DE ESCENARIO
        areaEscenario = QFrame(content_analogias)
        areaEscenario_layout = QHBoxLayout(areaEscenario)

        etiquetasAnalogias={
                            "Escenario": None,
                            "Campo": None
                            }

        for texto,estado in etiquetasAnalogias.items():

            filaSimilitud_area=QFrame(content_analogias)
            filaSimilitud_Layoy=QHBoxLayout(filaSimilitud_area)

            self.etiquetaSimi=elementos.crear_etiqueta(content_analogias,texto)
            self.resulAnalo=elementos.crear_lineEditFijo(content_analogias)

            filaSimilitud_Layoy.addWidget(self.etiquetaSimi)
            filaSimilitud_Layoy.addWidget(self.resulAnalo)

            areaEscenario_layout.addWidget(filaSimilitud_area)

        self.btn_buscar=QPushButton("Buscar")
        areaEscenario_layout.addWidget(self.btn_buscar)

        #TABLA DE SIMILUD
        self.tablaSimilitud=elementos.crear_tabla(content_analogias)


        #ITEMS DE CAMPOS ANALOGOS
        grupoSuperior_layout.addWidget(areaEscenario)
        grupoSuperior_layout.addWidget(self.tablaSimilitud)

        #=========================BASE DE CAMPOS ANALOGOS============================
        grupo_inferior=QGroupBox(content_analogias)
        grupoinferior_layout=QVBoxLayout(grupo_inferior)

        #CREACIÓN DE BUSCADOR
        buscador_area=QFrame(content_analogias)
        buscador_layout = QHBoxLayout(buscador_area)

        #barra de busqueda
        self.buscador=elementos.crear_buscador(content_analogias)
        buscador_layout.addWidget(self.buscador)

        #botones de base de datos
        gropoBontones_base=QFrame(content_analogias)
        gropoBontones_baseLayout=QGridLayout(gropoBontones_base)

        botonesbase = {
                        "buscar": ("Buscar campo", 0, 0),
                        "editar": ("Editar campo", 1, 0),
                        "mostrar": ("Base de campo", 0, 1),
                        "agregar": ("Agregar campo", 1, 1)
                      }

        self.botones_base={}

        for key,(etiqueta,fila,columna) in botonesbase.items():
            btn=elementos.crear_boton(content_analogias,etiqueta)
            self.botones_base[key] = btn
            gropoBontones_baseLayout.addWidget(btn,fila,columna)

        gropoBontones_baseLayout.setSpacing(10)
        #llamar botnones
        #self.botones_base["buscar"].setEnabled(False)

        buscador_layout.setSpacing(0)
        buscador_layout.addWidget(gropoBontones_base)

        #CREACION DE TABLA
        self.base_campos=elementos.crear_tabla(content_analogias)

        grupoinferior_layout.setSpacing(0)
        grupoinferior_layout.addWidget(buscador_area)
        grupoinferior_layout.addWidget(self.base_campos)

        #===========================CARGA DE GRUPOS===================================
        contentAnalogias_layout.setSpacing(0)
        contentAnalogias_layout.addWidget(grupoSuperior_area)
        contentAnalogias_layout.addWidget(grupo_inferior)

        return content_analogias

    def contenido_reservas(self):
        content_reservas = QFrame()
        content_reservas.setStyleSheet(f"background-color: {(240, 240, 240)};")
        content_reservas_layout = QGridLayout(content_reservas)

        #======================AREA DE CALCULOS=======================================
        infoReservas_grupo = QGroupBox(content_reservas)
        infoReservas_layout = QVBoxLayout(infoReservas_grupo)

        #volumenes originales
        volumenes_reservas = QGroupBox(content_reservas)
        volumenes_reservas_layout = QVBoxLayout(volumenes_reservas)

        #factores de recuperación
        factoresR_reservas = QGroupBox(content_reservas)
        factoresR_reservas_layout = QVBoxLayout(factoresR_reservas)

        etiquetas_reservas = {
                                "VooR":"Volumen original de condensado (MMbbl)",
                                "VogR":"Volumen original de gas (MMMpc)",
                                "FrcR":"Factor de recuperación condensado (%)",
                                "FrgR":"Factor de recuperación gas (%)",
                                #botnoes
                                "estiFac":"Estimas factores",
                                "estiRes": "Estimas Reservas"
                            }

        self.editLinesRes={}
        self.botonesRes={}

        reservas_botones_area = None

        for i,(key,(etiqueta)) in enumerate(etiquetas_reservas.items()):
            reservas_areas=QFrame(content_reservas)
            reservas_areas_layout = QHBoxLayout(reservas_areas)

            if i<4:
                #etiquetas
                self.etiqueta=elementos.crear_etiqueta(content_reservas,etiqueta)
                reservas_areas_layout.addWidget(self.etiqueta)

                #lineas editables
                lineEditsR=elementos.crear_lineEdit(content_reservas)
                self.editLinesRes[key]=lineEditsR
                reservas_areas_layout.addWidget(lineEditsR)

                if i < 2:

                    volumenes_reservas_layout.addWidget(reservas_areas)

                else:
                    factoresR_reservas_layout.addWidget(reservas_areas)
            else:
                if reservas_botones_area is None:

                    reservas_botones_area = QFrame(content_reservas)
                    reservas_botones_layout = QHBoxLayout(reservas_botones_area)

                btn = elementos.crear_boton(content_reservas, etiqueta)
                self.botonesRes[key] = btn
                reservas_botones_layout.addWidget(btn)

        if reservas_botones_area:
            factoresR_reservas_layout.addWidget(reservas_botones_area)

        #estimación de reservas
        EstimacionR_reservas = QGroupBox(content_reservas)
        EstimacionR_reservas_layout = QGridLayout(EstimacionR_reservas)

        self.elementos_reservas = {}
        etiquetas_reservas={
                            "t1":("Reservas condensados (MMbbl)",1,0),
                            "t2":("Reservas gas (MMMpc)",2,0),

                            "t3": ("1P",0,1),
                            "t4": ("2P",0,2),
                            "t5": ("3P",0,3),

                            "t6": ("P90",3,1),
                            "t7": ("P50",3,2),
                            "t8": ("P10",3,3),
                            "conunoP":(None,1,1),
                            "gasunoP": (None,2,1),
                            "condosP": (None,1,2),
                            "gasdosP": (None,2,2),
                            "contreP": (None,1,3),
                            "gastreP": (None,2,3),
        }

        for i,(key,(etiqueta,x,y)) in enumerate(etiquetas_reservas.items(), start=1):
            if i<9:
                etiquetas=elementos.crear_etiqueta(content_reservas, etiqueta)
                EstimacionR_reservas_layout.addWidget(etiquetas,x,y)
            else:
                lineEditsR=elementos.crear_lineEditFijo(content_reservas)
                self.elementos_reservas[key]=lineEditsR
                EstimacionR_reservas_layout.addWidget(lineEditsR,x,y)

        nota_label = elementos.crear_etiqueta(content_reservas,"Nota: *2P: Valor usado para el desarrollo tipo de los campos estratégicos (P50)")
        nota_label.setStyleSheet("font-size: 10px; color: #333;")
        EstimacionR_reservas_layout.addWidget(nota_label, 4, 0, 1, 4)

        #carga de items del grupo datos
        infoReservas_layout.addWidget(volumenes_reservas)
        infoReservas_layout.addWidget(factoresR_reservas)
        infoReservas_layout.addWidget(EstimacionR_reservas)

        # ======================AREA GRAFICOS=======================================
        graficosReservas_grupo = QGroupBox(content_reservas)
        graficosReservas_layout = QVBoxLayout(graficosReservas_grupo)


        self.categorias = ["Volumen", "Reservas"]
        self.valoresCondensado = [
                    [800, 1500],#bruto,
                    [600, 1200]#neto
                ]
        self.graficoCondensado = elementos.crear_grafica_barras_h(content_reservas,"Condensados",
                                                                self.categorias,self.valoresCondensado)
        self.valoresGas= [
                        [80, 150],
                        [65, 100],
                        [0, 80],
                        ]
        self.graficoGas=elementos.crear_grafica_barras_h(content_reservas,"Gas",
                                                         self.categorias,self.valoresGas)

        graficosReservas_layout.addWidget(self.graficoCondensado)
        graficosReservas_layout.addWidget(self.graficoGas)

        #========================= CARGAR GRAFICOS ===================================
        content_reservas_layout.setColumnStretch(0, 6)
        content_reservas_layout.setColumnStretch(1, 4)
        content_reservas_layout.addWidget(infoReservas_grupo,0,0)
        content_reservas_layout.addWidget(graficosReservas_grupo,0,1)

        return content_reservas

    def contenido_pronostico(self):
        content_pronosticos = QFrame()
        content_pronosticos.setStyleSheet(f"background-color: {(240, 240, 240)};")
        content_pronosticos_layout = QVBoxLayout(content_pronosticos)

        #============================= GRUPO DE INFORMACIÓN ============================
        grupo_info = QGroupBox(content_pronosticos)
        grupo_info_layout = QVBoxLayout(grupo_info)

        eituqtasInfo={
                      "DecliAnula":"Declinación anual",
                      "rgcPronos":"RGC (m³/m³)",
                      "WaterCutPronos":"Corte de agua (%)",
                      "qcPronos":"Gasto de condensado inical (Mbpd)",
                      "qgPronos":"Gasto de gas inicial (MMpcd)",
                      "qwPronos":"Gasto de  agua inicial (Mbpd)",
                      "RC2pPronos":"Reserva de condensado 2p (MMbbl)",
                      "RG2pPronos":"Reserva de gas 2p (MMMpcd)",
                      "econolim":"Limite economico",
                      "estPro":"Estimar pronóstico",
                      "savePro": "Guardar resultado",
                      "dowloPro": "Descargar informe fase 01"
                       }

        self.resulEtiqueasInfro = {}
        self.botosPros={}

        area_textos=QFrame(content_pronosticos)
        area_textos_layout = QHBoxLayout(area_textos)

        area1=QFrame(content_pronosticos)
        area1_layout = QVBoxLayout(area1)

        area2=QFrame(content_pronosticos)
        area2_layout = QVBoxLayout(area2)

        area3=QFrame(content_pronosticos)
        area3_layout = QVBoxLayout(area3)

        area4=QFrame(content_pronosticos)
        area4_layout = QHBoxLayout(area4)

        for i, (key,etiqueta) in enumerate(eituqtasInfo.items()):
            filaDato=QFrame(content_pronosticos)
            filaDato_layout = QHBoxLayout(filaDato)

            if i <9:
                self.etiInfoPro = elementos.crear_etiqueta(content_pronosticos, etiqueta)
                filaDato_layout.addWidget(self.etiInfoPro)

                cuadroRes=elementos.crear_lineEditFijo(content_pronosticos)
                self.resulEtiqueasInfro[key]=cuadroRes
                filaDato_layout.addWidget(cuadroRes)

                if i<3:
                    area1_layout.addWidget(filaDato)
                elif 2<i<6:
                    area2_layout.addWidget(filaDato)
                elif 5<i:
                    area3_layout.addWidget(filaDato)
            else:
                btn=QPushButton(etiqueta)
                self.botosPros[key]=btn
                area4_layout.addWidget(btn)

        area_textos_layout.addWidget(area1)
        area_textos_layout.addWidget(area2)
        area_textos_layout.addWidget(area3)
        grupo_info_layout.addWidget(area_textos)
        grupo_info_layout.addWidget(area4)

        #==================================== RESULTADOS ================================
        resultados_grupo = QGroupBox(content_pronosticos)
        resultados_grupo_layout = QVBoxLayout(resultados_grupo)

        #area de pozo
        areaPozos_grupo = QFrame(content_pronosticos)
        areaPozos_layout = QHBoxLayout(areaPozos_grupo)

        etiquetasPozos={
                        "Nwells":"Numero de pozos productores",
                        "QcondeMax":"Qcmax (Mbpd",
                        "QgasMax": "Qgmax(MMpcd)"
                        }


        self.PronosLineEdid={}

        for key,dato in etiquetasPozos.items():
            filaPozo = QFrame(content_pronosticos)
            filaPozo_layout = QHBoxLayout(filaPozo)

            self.etiquetaProRes=elementos.crear_etiqueta(content_pronosticos,dato)
            filaPozo_layout.addWidget(self.etiquetaProRes)

            etiqueta= elementos.crear_lineEditFijo(content_pronosticos)
            self.PronosLineEdid[key] = etiqueta
            filaPozo_layout.addWidget(etiqueta)

            areaPozos_layout.addWidget(filaPozo)

        resultados_grupo_layout.addWidget(areaPozos_grupo)

        #Tabla de pronosticos
        self.tablaPronosticos = elementos.crear_tabla(content_pronosticos)
        resultados_grupo_layout.addWidget(self.tablaPronosticos)

        #graficos
        area_graficos=QFrame()
        area_graficos_layout = QHBoxLayout(area_graficos)

        graficos={"Condensado",
                  "Gas",
                  "Agua"
                    }
        x,y=0,0
        for nombre in graficos:
            self.graficoPronostico=elementos.crear_grafica(content_pronosticos,nombre,x,y)
            area_graficos_layout.addWidget(self.graficoPronostico)

        resultados_grupo_layout.addWidget(area_graficos)


        #============================= AGREGAR LAYOUTS ===================================
        content_pronosticos_layout.addWidget(grupo_info)
        content_pronosticos_layout.addWidget(resultados_grupo)

        return content_pronosticos
