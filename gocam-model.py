import networkx as nx


class BasicEntity:

    def set_id(self, evidence_label):
        self.id = evidence_label

    def set_label(self, evidence_label):
        self.label = evidence_label
    
    def get_id(self):
        return self.id

    def get_label(self):
        return self.label


class Evidence (BasicEntity):

    def __init__(self, evidence_id):
        self.id = evidence_id

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

    def set_taxon(self, taxon_id):
        self.taxon_id = taxon_id
    
    def get_taxon(self):
        return self.taxon_id


class Term (BasicEntity):

    def __init__(self, term_id):
        self.id = term_id

    def set_aspect(self, aspect):
        self.aspect = aspect

    def get_aspect(self):
        return self.aspect


class Relationship (BasicEntity):

    def __init__(self, relation_id, relation_type):
        self.id = relation_id
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


class Association:

    def __init__(self, gene_product : GeneProduct, relationship : Relationship, term : Term):
        self.gene_product = gene_product
        self.relationship = relationship
        self.term = term

    def get_relationship(self):
        return self.relationship

    def get_gene_product(self):
        return self.gene_product    

    def get_term(self):
        return self.term



class ContextualAssociation:

    def __init__(self, relationship : Relationship, term : Term):
        self.relationship = relationship
        self.term = term


class Annoton (BasicEntity):

    def __init__(self, annoton_id):
        self.annoton_id = annoton_id
        self.contextual_associations = { }

    def set_association(self, association : Association):
        self.association = association

    def get_association(self):
        return self.association

    def add_contextual_association(self, contextual_association : ContextualAssociation):
        self.contextual_associations[contextual_association.id] = contextual_association

    def remove_contextual_association(self, contextual_association_id):
        self.contextual_associations.pop(contextual_association_id)

    def get_contextual_associations(self):
        return self.contextual_associations


class GOCam (BasicEntity):

    def __init__(self, model_id):
        self.model_id = model_id        
        self.graph = nx.MultiDiGraph(name=model_id)

    def has_annoton(self, annoton_id):
        return self.graph.has_node(annoton_id)

    def get_annoton(self, annoton_id):
        return self.graph.nodes(annoton_id)

    def create_annoton(self, annoton_id):
        if self.has_annoton(annoton_id):
            return False
        
        annoton = Annoton(annoton_id)
        self.graph.add_node(annoton_id, data = annoton)
        return True

    def remove_annoton(self, annoton_id):
        if not self.has_annoton(annoton_id):
            return False
        self.graph.remove_node(annoton_id)
        return True
    
    def has_relationship(self, annoton_id1, annoton_id2, relation_type):
        edges = self.graph.get_edge_data(annoton_id1, annoton_id2)
        for edge in edges:
            if edges[edge]['type'] == relation_type:
                return True
        return False

    def create_relationship(self, annoton_id1, annoton_id2, relation_type):
        if not self.has_annoton(annoton_id1) or not self.has_annoton(annoton_id2):
            return False
        self.graph.add_edge(annoton_id1, annoton_id2, **{ "type": relation_type })


class GOCamExport:

    def __init__(self, gocam : GOCam):
        self.gocam = gocam

    def to_json(self):
        pass

    def to_yaml(self):
        pass

    