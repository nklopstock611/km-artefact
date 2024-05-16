from rdflib import Graph, URIRef


g = Graph()

g.parse("./ontology/km_ontology_instances.ttl", format="ttl")


def get_properties_and_values_of_instance(instance_uri: str):
    """
    Returns the properties and values of a given instance URI.
    Example: get_properties_and_values_of_instance(g, "http://example.org/Usuario1")
    """
    instance_uri_ref = URIRef(instance_uri)

    query = """
    SELECT ?property ?value
    WHERE {
        ?instance_uri ?property ?value .
        FILTER(?property != rdf:type)
    }
    """

    results = g.query(query, initBindings={'instance_uri': instance_uri_ref})

    return results


def get_class_of_instance(instance_uri: str):
    """
    Returns the class of a given instance.
    Example: get_properties_and_values_of_instance(g, "http://example.org/Usuario1")
    """
    instance_uri_ref = URIRef(instance_uri)

    query = """
    SELECT ?property ?value
    WHERE {
        ?instance_uri ?property ?value .
        FILTER(?property = rdf:type)
    }
    """

    results = g.query(query, initBindings={'instance_uri': instance_uri_ref})

    return results


def get_models_fundamental_concept_and_description(model_uri: str):
    """
    Returns the fundamental concept and description of
    the given model.
    """
    model_uri_ref = URIRef(model_uri)

    query = """
    SELECT ?conceptoFundamental ?descripcionConcepto 
    WHERE { 
        ?model_uri a :Modelo . 
        ?conceptoFundamental a :Concepto_Fundamental . 
        ?model_uri :tieneConceptoFundamental ?conceptoFundamental . 
        ?conceptoFundamental :descripcion ?descripcionConcepto . 
    }
    """

    results = g.query(query, initBindings={'model_uri': model_uri_ref})

    return results


def get_models_modeling_hypothesis_and_description(model_uri: str):
    """
    Returns the modeling hypothesis and description of
    the given model.
    """
    model_uri_ref = URIRef(model_uri)

    query = """
    SELECT ?hipotesisModelado ?descripcionHipotesis 
    WHERE {
        ?model_uri rdf:type :Modelo . 
        ?hipotesisModelado rdf:type :Hipotesis_de_Modelado . 
        ?model_uri :tieneHipotesisDeModelado ?hipotesisModelado .
        ?hipotesisModelado :descripcion ?descripcionHipotesis .
    }
    """

    results = g.query(query, initBindings={'model_uri': model_uri_ref})

    return results


def get_restrictions_by_model(model_uri: str):
    """
    Returns the restrictions asociated to the given model.
    """
    model_uri_ref = URIRef(model_uri)

    query = """
    SELECT DISTINCT ?restriccion ?descripcionRestriccion
    WHERE {
        ?model_uri rdf:type :Modelo .
        ?model_uri :tieneRestriccion ?restriccion .
        ?restriccion rdf:type :Restriccion .
        ?restriccion :descripcion ?descripcionRestriccion .
    }
    """

    results = g.query(query, initBindings={'model_uri': model_uri_ref})

    return results


def get_use_cases_models_fundamental_concept_and_descriptions(use_case_uri: str):
    """
    Returns the models, fundamental concept and description of
    the given use case.
    """
    use_case_uri_ref = URIRef(use_case_uri)

    query = """
    SELECT ?modelo ?conceptoFundamental ?descripcionConcepto
    WHERE {
        ?use_case_uri rdf:type :Caso_de_Uso .
        ?modelo rdf:type :Modelo .
        ?conceptoFundamental rdf:type :Concepto_Fundamental .
        ?use_case_uri :tieneModelo ?modelo .
        ?conceptoFundamental :descripcion ?descripcionConcepto .
        ?modelo :tieneConceptoFundamental ?conceptoFundamental .
    }
    """

    results = g.query(query, initBindings={'use_case_uri': use_case_uri_ref})

    return results


def is_instance_uri(value):
    if '<ul><li>' in value: # If it is a list of URIs
        preprocessed_value = value.replace('<ul><li>', '').replace('</ul>', '').replace('<li>', '').split('</li>')
        return all(item.startswith('http://www.apex.com') for item in preprocessed_value[:-1])
    else:
        return str(value).startswith('http://www.apex.com')

def has_instances(properties):
    for prop, value in properties:
        if is_instance_uri(value):
            return True

    return False
