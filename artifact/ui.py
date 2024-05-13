import streamlit as st
import pandas as pd
import queries as qs

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

# ============ #
# Streamlit UI #
# ============ #

if 'prev_instance_uri' not in st.session_state:
    st.session_state.prev_instance_uri = ['']

st.title('APEX - Documentación')

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