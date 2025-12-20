from capaLogica.lPersona import LPersona
import streamlit as st
from datetime import date

class PPersona:

    def __init__(self):
        self.__lPersona = LPersona()
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey= 0
        if 'persona_seleccionada' not in st.session_state:
            st.session_state.persona_seleccionada = ''
        if 'docIdentidad_sesion' not in st.session_state:
            st.session_state.docIdentidad_sesion = ''
        if 'nombres_sesion' not in st.session_state:
            st.session_state.nombres_sesion = ''
        if 'apellidoPaterno_sesion' not in st.session_state:
            st.session_state.apellidoPaterno_sesion = ''
        if 'apellidoMaterno_sesion' not in st.session_state:
            st.session_state.apellidoMaterno_sesion = ''
        # CORREGIDO: Inicializar fechaNacimiento_sesion
        if 'fechaNacimiento_sesion' not in st.session_state:
            st.session_state.fechaNacimiento_sesion = date.today()
        if 'correoEscuela_sesion' not in st.session_state:
            st.session_state.correoEscuela_sesion = ''
        if 'contraseniaEscuela_sesion' not in st.session_state:
            st.session_state.contraseniaEscuela_sesion = ''                          
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title("Registro de Estudiantes")
        # CORREGIDO: Solo acceder si es diccionario y tiene datos
        if st.session_state.persona_seleccionada != '' and isinstance(st.session_state.persona_seleccionada, dict):
            st.session_state.docIdentidad_sesion = st.session_state.persona_seleccionada['dni']
            st.session_state.nombres_sesion = st.session_state.persona_seleccionada['nombres']
            st.session_state.apellidoPaterno_sesion = st.session_state.persona_seleccionada['apellidopaterno']
            st.session_state.apellidoMaterno_sesion = st.session_state.persona_seleccionada['apellidomaterno']
            # CORREGIDO: Manejar conversión de fecha
            fecha_str = st.session_state.persona_seleccionada['fecha_nacimiento']
            if isinstance(fecha_str, str):
                st.session_state.fechaNacimiento_sesion = date.fromisoformat(fecha_str)
            st.session_state.correoEscuela_sesion = st.session_state.persona_seleccionada['correo_escuela']
            st.session_state.contraseniaEscuela_sesion = st.session_state.persona_seleccionada['contrasenia_escuela']
        
        with st.form(f"Formulario de Estudiantes {st.session_state.formularioKey}"):
            docIdentidad = st.text_input("Documento de Identidad", value=st.session_state.docIdentidad_sesion, disabled=st.session_state.persona_seleccionada != '', max_chars=8, help="Ingrese su DNI sin puntos ni guiones, Solo números.", placeholder="Ejem: 12345678")
            nombres = st.text_input("Nombres", value=st.session_state.nombres_sesion, max_chars=70, help="Ingrese sus nombres completos, separados por espacios y nada de números.", placeholder="Ejem: Juan Carlos")
            apellidoPaterno = st.text_input("Apellido Paterno", value=st.session_state.apellidoPaterno_sesion, max_chars=50, help="Ingrese su apellido paterno, nada de números.", placeholder="Ejem: Pérez")
            apellidoMaterno = st.text_input("Apellido Materno", value=st.session_state.apellidoMaterno_sesion, max_chars=50, help="Ingrese su apellido materno, nada de números.", placeholder="Ejem: Gómez")
            fechaNacimiento = st.date_input("Fecha de Nacimiento", value=st.session_state.fechaNacimiento_sesion, help="Seleccione su fecha de nacimiento.", max_value=date.today())
            correoEscuela = st.text_input("Correo de la Escuela", value=st.session_state.correoEscuela_sesion, help="Ingrese su correo institucional.", placeholder="Ejem: 12345678@davidhouse.edu.pe", max_chars=110)
            contraseniaEscuela = st.text_input("Contraseña de la Escuela", value=st.session_state.contraseniaEscuela_sesion, type="password", help="Ingrese su contraseña institucional.", max_chars=50)
            if st.session_state.persona_seleccionada != '':
                btnActualizar = st.form_submit_button("Actualizar Estudiante", type="primary")
                if btnActualizar:
                    persona = {
                        "dni": docIdentidad,
                        "nombres": nombres,
                        "apellidopaterno": apellidoPaterno,
                        "apellidomaterno": apellidoMaterno,
                        "fecha_nacimiento": fechaNacimiento.isoformat(),
                        "correo_escuela": correoEscuela,
                        "contrasenia_escuela": contraseniaEscuela
                    }
                    self.actualizarPersona(persona, docIdentidad)


            else:
                btnRegistrar = st.form_submit_button("Registrar Estudiante", type="primary")

                if btnRegistrar:
                    persona = {
                        "dni": docIdentidad,
                        "nombres": nombres,
                        "apellidopaterno": apellidoPaterno,
                        "apellidomaterno": apellidoMaterno,
                        "fecha_nacimiento": fechaNacimiento.isoformat(),
                        "correo_escuela": correoEscuela,
                        "contrasenia_escuela": contraseniaEscuela
                    }
                    self.nuevaPersona(persona)
        self.mostrarPersona()

    def mostrarPersona(self):
        listaPersonas = self.__lPersona.mostrarPersona()
        col1, col2 = st.columns([10, 2])
        with col1:
            personaSeleccionada = st.dataframe(listaPersonas, selection_mode="single-row", on_select="rerun")
        with col2:
            if personaSeleccionada.selection.rows:
                indice_persona = personaSeleccionada.selection.rows[0]
                personaSeleccionadaIndice = listaPersonas[indice_persona]
                btnEditar = st.button('Editar Estudiante')

                btnEliminar = st.button('Eliminar Estudiante')

                if btnEditar:
                    # CORREGIDO: Guardar el diccionario completo, no solo el DNI
                    st.session_state.persona_seleccionada = personaSeleccionadaIndice
                    st.rerun() 

                if btnEliminar:
                    self.eliminarPersona(personaSeleccionadaIndice['dni'])
                    st.rerun()
    def nuevaPersona(self, persona: dict):
        try:
            self.__lPersona.nuevaPersona(persona)
            st.toast("Estudiante registrado exitosamente.", duration='short')            
            self.limpiar()

        except Exception as e:    
            st.error(e)
            st.toast('Registro fallido')

    def actualizarPersona(self, persona: dict, docIdentidad: str):
        try:
            self.__lPersona.actualizarPersona(persona, docIdentidad)
            st.toast("Estudiante actualizado exitosamente.", duration='short')
            self.limpiar()

        except Exception as e:    
            st.error(e)
            st.toast('Actualización fallida')

    def eliminarPersona(self, docIdentidad: str):
        try:
            self.__lPersona.eliminarPersona(docIdentidad)
            st.toast("Registro eliminado exitosamente.", duration='short')


        except Exception as e:    
            st.error(e)
            st.toast('Eliminación fallida')
        self.__lPersona.eliminarPersona(docIdentidad)


    def limpiar(self):
       st.session_state.formularioKey += 1
       st.session_state.persona_seleccionada = ''
       st.session_state.docIdentidad_sesion = ''
       st.session_state.nombres_sesion = ''
       st.session_state.apellidoPaterno_sesion = ''
       st.session_state.apellidoMaterno_sesion = ''
       st.session_state.fechaNacimiento_sesion = date.today()
       st.session_state.correoEscuela_sesion = ''
       st.session_state.contraseniaEscuela_sesion = ''        
       st.rerun()