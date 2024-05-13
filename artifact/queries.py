from rdflib import Graph, URIRef

g = Graph()

g.parse("./ontology/km_ontology_instances.ttl", format="ttl")

def get_properties_and_values_of_instance(instance_uri):
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

def get_class_of_instance(instance_uri):
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
