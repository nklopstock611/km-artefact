import streamlit as st
import pandas as pd
import queries as qs

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'

if 'prev_instance_uri' not in st.session_state:
    st.session_state.prev_instance_uri = ['']

def set_view(view_name):
    st.session_state.current_view = view_name

def consolidate_properties(results):
    prop_dict = {}
    for prop, val in results:
        val_str = str(val)
        if prop in prop_dict:
            prop_dict[prop].append(val_str)
        else:
            prop_dict[prop] = [val_str]

    # Converts lists of values into HTML lists if there are more than one value of a property
    for prop in prop_dict:
        if len(prop_dict[prop]) > 1:
            prop_dict[prop] = '<ul>' + ''.join(f'<li>{value}</li>' for value in prop_dict[prop]) + '</ul>'
        else:
            prop_dict[prop] = prop_dict[prop][0]

    return prop_dict

def get_class_name(results):
    for prop, value in results:
        if str(prop) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            return str(value).split('/')[-1].replace('voca#', '')

    return None

def handle_click(instance_name, prev_instance_name):
    st.session_state.prev_instance_uri.append(prev_instance_name)
    st.session_state.instance_uri = instance_name

def go_back():
    if st.session_state.prev_instance_uri != []:
        st.session_state.instance_uri = st.session_state.prev_instance_uri.pop()

def load_data(instance_uri):
    prop_dict = {}
    results = qs.get_properties_and_values_of_instance(f"http://www.apex.com/{instance_uri}")
    if results:
        prop_dict = consolidate_properties(results)
        data = [{"Propiedad": prop.replace('http://www.apex.com/voca#', ''), "Valor": values.replace('http://www.apex.com/voca#', '')} for prop, values in prop_dict.items()]
        df = pd.DataFrame(data)

        # Render HTML in dataframe cells without index
        class_of_instance = qs.get_class_of_instance(f"http://www.apex.com/{instance_uri}")
        class_of_instance = get_class_name(class_of_instance)
        st.subheader(f"Tipo: {class_of_instance}")

        html = df.to_html(escape=False, index=False)
        html = html.replace('<th>', '<th style="text-align: left;">')
        html = html.replace('<table border="1" class="dataframe">', '<table style="width: 100%;">')
        st.markdown(html, unsafe_allow_html=True)                      

    else:
        st.write("No hay resultados para el concepto ingresado.")

    return prop_dict, results

def load_ontology_search_view():
    instance_uri = st.text_input('Ingresa el nombre de un concepto:', key='instance_uri')
    st.markdown("---")

    if instance_uri:
        st.session_state['current_uri'] = instance_uri
        prop_dict, results = load_data(instance_uri)

        if qs.has_instances(results):
            st.markdown("---")
            st.subheader("Instancias en las propiedades:")
            for prop, value in prop_dict.items():
                if qs.is_instance_uri(value):
                    if '<ul><li>' in value:
                        instances = value.replace('<ul><li>', '').replace('</ul>', '').replace('<li>', '').split('</li>')[:-1]
                        for instance in instances:
                            instance_name = instance.split('/')[-1]
                            st.text(f"{prop}: ")
                            col1, col2, col3 = st.columns([4, 1, 1])
                            col1.button(instance_name, on_click=handle_click, args=(instance_name, instance_uri))
                    else:
                        st.text(f"{prop.replace('http://www.apex.com/voca#', '')}: ")
                        instance = value.split('/')[-1]
                        col1, col2, col3 = st.columns([4, 1, 1])
                        col1.button(instance, on_click=handle_click, args=(instance, instance_uri)) 
    else:
        st.write("Por favor, ingrese un concepto.")

    st.markdown("---")
    st.button("Atrás", on_click=go_back)

def load_queries_view():
    st.subheader('Consultas comunes')
    query_param = st.text_input('Ingresa el nombre de un parámetro:')
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    query = None
    with col1:
        if st.button("Conceptos Fundamentales de un Modelo"):
            query = "Q1"
    with col2:
        if st.button("Hipótesis de Modelado de un Modelo"):
            query = "Q2"
    with col3:
        if st.button("Modelos y Conceptos Fundamentales asociados a un Caso de Uso"):
            query = "Q3"
    with col4:
        if st.button("Restricciones por Modelo"):
            query = "Q4"

    if query_param:
        if query:
            results = []
            query_param_uri = f"http://www.apex.com/{query_param}"
            if query == "Q1":
                results = qs.get_models_fundamental_concept_and_description(query_param_uri)
            elif query == "Q2":
                results = qs.get_models_modeling_hypothesis_and_description(query_param_uri)
            elif query == "Q3":
                results = qs.get_use_cases_models_fundamental_concept_and_descriptions(query_param_uri)
            elif query == "Q4":
                results = qs.get_restrictions_by_model(query_param_uri)
            else:
                st.write('Botón no encontrado.')

            if len(results) > 0:
                for result in results:
                    if len(result) == 1:
                        st.write()
                        st.write(result[0].replace('http://www.apex.com/', '').replace('_', ' '))
                    elif len(result) == 2:
                        concept, desc = result
                        st.subheader(concept.replace('http://www.apex.com/', '').replace('_', ' '))
                        st.write(desc)
                    elif len(result) == 3:
                        model, conc, conc_desc = result
                        st.subheader(f"Modelo: {model.replace('http://www.apex.com/', '').replace('_', ' ')} - Concepto Fundamental: {conc.replace('http://www.apex.com/', '').replace('_', ' ')}")
                        # st.write(f"Descripción del Concepto Fundamental: {conc_desc}")
                        st.markdown(f"**Descripción del Concepto Fundamental:** {conc_desc}")
            else:
                st.write('')
                st.write('No se retornó información con el parámetro dado.')
        else:
            st.write('')
            st.write('Selecciona una consulta.')
    else:
        st.write('')
        st.write('Ingresa un parámetro de consulta y presiona la tecla Enter.')

# ============ #
# Streamlit UI #
# ============ #

st.title('Apex in a Nutshell')

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Ontología"):
        set_view('ontology')

with col2:
    if st.button("Consultas"):
        set_view('queries')

if st.session_state['current_view'] == 'ontology':
    load_ontology_search_view()
elif st.session_state['current_view'] == 'queries':
    load_queries_view()
