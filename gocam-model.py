import networkx as nx
from enum import Enum

import datetime


class EntityType(Enum):
    BASIC = "basic"
    EVIDENCE = "evidence"
    TERM = "term"
    GENE_PRODUCT = "gene_product"
    TAXON = "taxon"
    RELATIONSHIP = "relationship"
    CONTEXT = "context"
    ACTIVITY = "activity"
    CONTRIBUTOR = "contributor"
    GROUP = "group"



class NamedEntity:
    """
    The (id, label) are to be used to define the entity itself, and only uuid should be used to define the instance of that class
    For instance, the uuid could be a URI of a subject in the triple store
    """

    def __init__(self, id, label):
        self.uuid = None
        self.id = id
        self.label = label

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_id(self, id):
        self.id = id

    def set_label(self, label : str):
        self.label = label
    
    def get_id(self):
        return self.id

    def get_label(self) -> str:
        return self.label

    def same(self, entity : NamedEntity) -> bool:
        if self.id != entity.id or self.label != entity.label:
            return False
        return True

    def equals(self, entity : NamedEntity) -> bool:
        return self == entity

    def __str__(self) -> str:
        return self.label + " [" + self.id + "]"


class TypedNamedEntity (NamedEntity):
    """
    Basic Unit to describe any entity
    """

    def __init__(self, id, label, type : EntityType):
        super().__init__(id, label)
        self.type = type

    def set_type(self, type : EntityType):
        self.type = type

    def get_type(self) -> EntityType:
        return self.type

    def is_type(self, type : EntityType) -> bool:
        return self.type == type

    def same(self, entity : TypedNamedEntity) -> bool:
        if self.id != entity.id or self.label != entity.label or self.type != entity.type:
            return False
        return True

    def equals(self, entity : TypedNamedEntity) -> bool:
        return self == entity

    def __str__(self) -> str:
        return self.type + ":" + self.label + " [" + self.id + "]"


class Term (TypedNamedEntity):

    def __init__(self, term_id, term_label : str):
        super().__init__(term_id, term_label, EntityType.TERM)
        self.aspect = None

    def set_aspect(self, aspect : Term):
        self.aspect = aspect

    def get_aspect(self) -> Term:
        return self.aspect

    def is_mf(self):
        return self.aspect.get_id() == "GO:0003674"

    def is_bp(self):
        return self.aspect.get_id() == "GO:0008150"

    def is_cc(self):
        return self.aspect.get_id() == "GO:0005575"

    def same(self, term : Term) -> bool:
        if self.id != term.id or self.label != term.label or self.type != term.type:
            return False
        return self.aspect == term.aspect

    def equals(self, entity : TypedNamedEntity) -> bool:
        return self == entity

    def __str__(self) -> str:
        return self.type + ":" + self.label + " [" + self.id + "]"


class Taxon (TypedNamedEntity):

    def __init__(self, taxon_id, taxon_label):
        super().__init__(taxon_id, taxon_label, EntityType.TAXON)


class GeneProduct (TypedNamedEntity):

    def __init__(self, gene_product_id, gene_product_label, taxon : Taxon):
        super().__init__(gene_product_id, gene_product_label, EntityType.GENE_PRODUCT)
        self.taxon = taxon

    def set_taxon(self, taxon : Taxon):
        self.taxon = taxon
    
    def get_taxon(self) -> Taxon:
        return self.taxon

    def same(self, gene_product : GeneProduct) -> bool:
        if self.id != gene_product.id or self.label != gene_product.label or self.type != gene_product.type:
            return False
        return self.taxon.same(gene_product.taxon)

    def equals(self, gene_product : TypedNamedEntity):
        return self == gene_product

    def __str__(self):
        return self.type + ":" + self.label + ":" + self.taxon.label + " [" + self.id + "]"


class Group (TypedNamedEntity):

    def __init__(self, orcid, name):
        super().__init__(orcid, name)
    

class Contributor (TypedNamedEntity):

    def __init__(self, orcid, name, groups : [Group]):
        super().__init__(orcid, name, EntityType.CONTRIBUTOR)
        if groups is None:
            groups = { }
        else:
            self.groups = groups

    def set_groups(self, groups : [Group]):
        self.groups = groups

    def has_group(self, group : Group) -> bool:
        for gp in self.groups:
            if gp == group:
                return True
        return False

    def add_group(self, group : Group) -> bool:
        if self.has_group(group):
            return False
        self.groups[group.id] = group
        return True

    def remove_group(self, group : Group) -> bool:
        if not self.has_group(group):
            return False
        self.groups.pop(group.id)
        return True


class Evidence (TypedNamedEntity):

    def __init__(self, evidence_id, evidence_label : str, contributor : Contributor):
        super().__init__(evidence_id, evidence_label, EntityType.EVIDENCE)
        self.set_contributor(contributor)
        self.date = datetime.datetime.now()
        
    def set_contributor(self, contributor : Contributor):
        self.contributors = { }
        self.contributors[contributor.id] = contributor

    def add_contributor(self, contributor : Contributor) -> bool:
        if contributor.id in self.contributors:
            return False
        self.contributors[contributor.id] = contributor
        return True
    
    def get_contributors(self) -> [Contributor]:
        return self.contributors

    def set_date(self, date):
        self.date = date

    def get_date(self):
        return self.date

    def same(self, evidence : evidence) -> bool:
        if not super().same(evidence):
            return False
        if len(self.contributors) != len(evidence.contributors):
            return False
        for contributor_id in evidence.contributors:
            if contributor_id not in self.contributors:
                return False
        return True





class BasicRelationship (TypedNamedEntity):
    """
    This defines the basic property of any relationship: it's a TypedNamedEntity
    """

    def __init__(self, id, label : str):
        super().__init__(id, label, EntityType.RELATIONSHIP)


class EvidencedRelationship (BasicRelationship):
    """
    This defines a relationship between a subject and object and supported by 0+ evidences
    """

    def __init__(self, subject : TypedNamedEntity, object : TypedNamedEntity, relation_id, relation_label : str):
        super().__init__(relation_id, relation_label)
        self.subject = subject
        self.object = object
        self.evidences = { }

    def set_evidences(self, evidences : [Evidence]):
        self.evidences = evidences

    def add_evidence(self, evidence : Evidence):
        self.evidences[evidence.get_id()] = evidence

    def remove_evidence(self, evidence_id):
        self.evidences.pop(evidence_id)

    def get_evidences(self) -> [Evidence]:
        return self.evidences

    def same(self, relation : EvidencedRelationship) -> bool:
        if not super().same(relation):
            return False
        if len(self.evidences) != len(relation.evidences):
            return False
        for key,val in self.evidences:
            if key not in relation.evidences:
                return False
            if not val.same(relation.evidences[key]):
                return False


class TypedNamedEntityAssociation (EvidencedRelationship):
    """
    General purpose association for entities
    """

    def __init__(self, subject : TypedNamedEntity, object : TypedNamedEntity, relation_id, relation_label : str):
        super().__init__(relation_id, relation_label)
        self.subject = subject
        self.object = object

    def get_subject(self) -> TypedNamedEntity:
        return self.subject

    def get_object(self) -> TypedNamedEntity:
        return self.object


class ActivityAssociation (TypedNamedEntityAssociation):
    """
    Wrapper class to really understand what we are getting / asking for in an Activity Association (MF enabled by GPs)
    """

    def __init__(self, activity : Term, gene_product : GeneProduct, relation_id, relation_label):
        super().__init__(activity, gene_product, relation_id, relation_label)

    def get_activity(self) -> Term:
        return self.subject

    def get_gene_product(self) -> GeneProduct:
        return self.object
        


class Context (Term):
    """
    A Context is a Term that is not an Activity
    """

    def __init__(self, term : Term):
        super().__init__(term.id, term.label)
        self.type = EntityType.CONTEXT

        if self.is_mf():
            raise Exception("Context Terms can not be an activity, you probably want to create an Activity ?")



class TypedNamedEntityTargetAssociation (EvidencedRelationship):
    """
    General purpose association for entities (we only keep the targets/objects, not the subject)
    """

    def __init__(self, object : TypedNamedEntity, relation_id, relation_label : str):
        super().__init__(relation_id, relation_label)
        self.object = object

    def get_object(self) -> TypedNamedEntity:
        return self.object


class ContextTargetAssociation (TypedNamedEntityAssociation):
    """
    Specific Activity associations (e.g. part_of object or occurs_in object)
    Wrapper class to really understand what we are getting / asking for in a Context Association (Activity part_of, occurs_in, etc)
    """

    def __init__(self, context : Context, relation_id, relation_label):
        super().__init__(context, relation_id, relation_label)

    def get_context(self) -> Context:
        return self.object


class Activity (Term):
    """
    An Activity is a Term that is of aspect Activity (MF)
    The instances of Context terms MUST be created at the GO-CAM level. Only the LINKS are part of the Activities
    """

    def __init__(self, activity_id, activity_label):
        super().__init__(activity_id, activity_label)
        self.type = EntityType.ACTIVITY
        self.context_targets = { }

        if not self.is_mf():
            raise Exception("Activity Terms must be an activity, you probably want to create a Context ?")
        
    def set_activity_association(self, activity_association : ActivityAssociation):
        self.activity_association = activity_association

    def get_activity_association(self) -> ActivityAssociation:
        return self.activity_association

    def has_context(self, context_association : ContextTargetAssociation) -> bool:
        return context_association.id in self.context_targets

    def add_context(self, context_association : ContextTargetAssociation) -> bool:
        if self.has_context(context_association):
            return False
        self.context_targets[context_association.id] = context_association
        return True

    def remove_context(self, context_association : ContextTargetAssociation) -> bool:
        if not self.has_context(context_association):
            return False
        self.context_targets.pop(context_association.id)
        return True

    def get_contexts(self) -> [ContextTargetAssociation]:
        return self.context_targets



class GOCam:
    """
    GO-CAM is currently the largest data wrapper. Both Activity and Context node instances must be created at this level.
    The causal relationships between Activities are stored at this level but the links between any (Activity -> Context(s)) are stored at the Activity level.
    """

    def __init__(self, model_id, model_title):
        self.id = model_id        
        self.title = model_title
        self.creation_date = None
        self.modified_date = None
        self.graph = nx.MultiDiGraph(name=model_id)
        self.contributors = { }
        self.contexts = { }

    def set_title(self, title : str):
        self.title = title

    def set_creation_date(self, date):
        self.creation_date = date

    def set_modified_date(self, date):
        self.modified_date = date

    def set_contributors(self, contributors : [Contributor]):
        self.contributors = contributors

    def add_contributor(self, contributor : Contributor):
        self.contributors[contributor.id] = contributor

    def get_title(self) -> str:
        return self.title

    def get_creation_date(self):
        return self.creation_date

    def get_modified_date(self):
        return self.modified_date

    def has_contributor(self, orcid) -> bool:
        return orcid in self.contributors

    def get_contributors(self) -> [Contributor]:
        return self.contributors

    def has_activity(self, activity_id) -> bool:
        return self.graph.has_node(activity_id)

    def get_activity(self, activity_id):
        return self.graph.nodes(activity_id)

    def add_activity(self, activity : Activity) -> bool:
        if self.has_activity(activity.id):
            return False
        
        self.graph.add_node(activity.id, data = activity)
        return True

    def remove_activity(self, activity_id) -> bool:
        if not self.has_activity(activity_id):
            return False
        self.graph.remove_node(activity_id)
        return True
    
    def has_causal_relationship(self, activity_id1, activity_id2, relation_type) -> bool:
        edges = self.graph.get_edge_data(activity_id1, activity_id2)
        for edge in edges:
            if edges[edge]['type'] == relation_type:
                return True
        return False

    def add_causal_relationship(self, activity_id1, activity_id2, relation_type) -> bool:
        if not self.has_activity(activity_id1) or not self.has_activity(activity_id2):
            return False
        self.graph.add_edge(activity_id1, activity_id2, **{ "type": relation_type })
        return True

    def remove_causal_relationship(self):
        pass

    def add_context(self, context : Context):
        self.contexts[context.id] = context

    def remove_context(self, context_id):
        self.contexts.pop(context_id)

    def has_context(self, context_id):
        return context_id in self.contexts

    def get_contexts(self):
        return self.contexts        




class GOCamHandler:

    def __init__(self, gocam : GOCam):
        self.gocam = gocam

    def from_json(self):
        pass

    def from_yaml(self):
        pass

    def from_ttl(self):
        pass

    def from_gorql(self):
        pass

    def from_golr(self):
        pass

    def to_json(self):
        pass

    def to_yaml(self):
        pass

    def to_ttl(self):
        pass

    def to_golr(self):
        pass

    def to_gorql(self):
        pass