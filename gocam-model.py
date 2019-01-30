import networkx as nx
from enum import Enum


class EntityType(Enum):
    BASIC = "basic"
    EVIDENCE = "evidence"
    TERM = "term"
    GENE_PRODUCT = "gene_product"
    RELATIONSHIP = "relationship"
    CONTEXT = "context"
    ACTIVITY = "activity"



class BasicEntity:
    """
    Basic Unit to describe any entity
    """

    def set_id(self, evidence_label):
        self.id = evidence_label

    def set_type(self, type):
        self.type = type

    def set_label(self, evidence_label):
        self.label = evidence_label
    
    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_label(self):
        return self.label


class BasicRelationship:
    """
    This is similar to BasicEntity but separated in order to let Entities and Relations evolve separately
    """

    def set_id(self, evidence_label):
        self.id = evidence_label

    def set_type(self, type):
        self.type = type

    def set_label(self, evidence_label):
        self.label = evidence_label
    
    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_label(self):
        return self.label


class Evidence (BasicEntity):

    def __init__(self, evidence_id, evidence_type):
        self.id = evidence_id
        self.type = EntityType.EVIDENCE
        
    def set_contributor(self, contributor):
        self.contributor = contributor
    
    def get_contributor(self):
        return self.contributor

    def set_date(self, date):
        self.date = date

    def get_date(self):
        return self.date


class GeneProduct (BasicEntity):

    def __init__(self, gene_product_id):
        self.id = gene_product_id
        self.type = EntityType.GENE_PRODUCT

    def set_taxon(self, taxon_id):
        self.taxon_id = taxon_id
    
    def get_taxon(self):
        return self.taxon_id


class Term (BasicEntity):

    def __init__(self, term_id):
        self.id = term_id
        self.type = EntityType.TERM

    def set_aspect(self, aspect):
        self.aspect = aspect

    def get_aspect(self):
        return self.aspect


class Relationship (BasicRelationship):

    def __init__(self, relation_id, relation_type):
        self.id = relation_id
        self.type = EntityType.RELATIONSHIP
        self.relation_type = relation_type
        self.evidences = { }

    def set_relation_type(self, relation_type):
        self.relation_type = relation_type

    def get_relation_type(self):
        return self.relation_type

    def add_evidence(self, evidence : Evidence):
        self.evidences[evidence.get_id()] = evidence

    def remove_evidence(self, evidence_id):
        self.evidences.pop(evidence_id)

    def get_evidences(self):
        return self.evidences


class EntityAssociation (Relationship):
    """
    General purpose association for entities
    """

    def __init__(self, subject : BasicEntity, relation_id, relation_type, object : BasicEntity):
        super().__init__(relation_id, relation_type)
        self.subject = subject
        self.object = object

    def get_relationship(self):
        return self

    def get_evidences(self):
        return self.get_evidences()

    def get_subject(self):
        return self.subject    

    def get_object(self):
        return self.object


class ActivityAssociation (EntityAssociation):
    """
    Wrapper class to really understand what we are getting / asking for
    """

    def __init__(self, gene_product : GeneProduct, relation_id, relation_type, term : Term):
        super().__init__(gene_product, relation_id, relation_type, term)

    def get_gene_product(self):
        return self.get_subject()    

    def get_term(self):
        return self.get_object()


class Context (BasicEntity):

    def __init__(self, relationship : Relationship, term : Term):
        self.type = EntityType.CONTEXT
        self.relationship = relationship
        self.term = term


class Activity (BasicEntity):

    def __init__(self, activity_id):
        self.id = activity_id
        self.type = EntityType.ACTIVITY
        self.contexts = { }

    def set_activity_association(self, activity_association : ActivityAssociation):
        self.activity_association = activity_association

    def get_activity_association(self):
        return self.activity_association

    def add_context(self, context : Context):
        self.contexts[context.id] = context

    def remove_context(self, context_id):
        self.contexts.pop(context_id)

    def get_contexts(self):
        return self.contexts


class GOCam:

    def __init__(self, model_id):
        self.id = model_id        
        self.graph = nx.MultiDiGraph(name=model_id)

    def has_activity(self, activity_id):
        return self.graph.has_node(activity_id)

    def get_activity(self, activity_id):
        return self.graph.nodes(activity_id)

    def add_activity(self, activity_id):
        if self.has_activity(activity_id):
            return False
        
        activity = Activity(activity_id)
        self.graph.add_node(activity_id, data = activity)
        return True

    def remove_activity(self, activity_id):
        if not self.has_activity(activity_id):
            return False
        self.graph.remove_node(activity_id)
        return True
    
    def has_causal_relationship(self, activity_id1, activity_id2, relation_type):
        edges = self.graph.get_edge_data(activity_id1, activity_id2)
        for edge in edges:
            if edges[edge]['type'] == relation_type:
                return True
        return False

    def add_causal_relationship(self, activity_id1, activity_id2, relation_type):
        if not self.has_activity(activity_id1) or not self.has_activity(activity_id2):
            return False
        self.graph.add_edge(activity_id1, activity_id2, **{ "type": relation_type })


class GOCamExport:

    def __init__(self, gocam : GOCam):
        self.gocam = gocam

    def to_json(self):
        pass

    def to_yaml(self):
        pass

    def to_ttl(self):
        pass

    