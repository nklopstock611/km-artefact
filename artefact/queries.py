from rdflib import Graph, URIRef

g = Graph()

g.parse("./ontology/km_ontology.ttl", format="ttl")

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
    return str(value).startswith("http://example.org")

def has_instances(properties):
    for prop, value in properties:
        if is_instance_uri(value):
            return True
            
    return False
