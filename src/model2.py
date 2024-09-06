import os
from dotenv import load_dotenv
from neomodel import (
    config,
    StructuredNode,
    StringProperty,
    DateProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty
)


load_dotenv()
neo4j_url = os.getenv('NEO4J_URI_0')
config.DATABASE_URL = neo4j_url


class Court(StructuredNode):
    name = StringProperty(required=True)
    abbreviation = StringProperty()

    # Relationships
    case = RelationshipTo('Case', 'Is_case')
    applealed_case = RelationshipTo('AppealedCase', 'Is_case')


class Case(StructuredNode):
    case_name = StringProperty(required=True)
    case_no = StringProperty()
    dated = DateProperty()
    result = StringProperty()
    overruled = StringProperty()
    overruled_by = StringProperty()

    # Relationships
    is_appealed = RelationshipFrom('ApplealedCase', 'Appeal_from')
    case_appealed_to = RelationshipTo('ApplealedCase', 'Appeal_to')
    court = RelationshipFrom('Court', 'Is_case')
    case_data = RelationshipTo('CourtData', 'Has_data')
    case_summary = RelationshipTo('SummaryData', 'Has_data')
    case_citations = RelationshipTo('CitationsData', 'Has_data')


class ApplealedCase(StructuredNode):
    case_name = StringProperty(required=True)
    case_no = StringProperty()
    dated = DateProperty()
    result = StringProperty()
    overruled = StringProperty()
    overruled_by = StringProperty()

    # Relationships
    is_appealed = RelationshipTo('Case', 'Appeal_from')
    case_appealed_to = RelationshipFrom('Case', 'Appeal_to')
    court = RelationshipFrom('Court', 'Is_case')


class CourtData(StructuredNode):
    case_no = StringProperty(required=True)
    case_type = StringProperty()
    petetioner = StringProperty()
    respondent = StringProperty()
    coram = StringProperty()
    petetioner_counsel = StringProperty()
    respondent_counsel = StringProperty()
    act = StringProperty()
    bench = StringProperty()
    dated = DateProperty()
    reportable = StringProperty()

    # Relationships
    case = RelationshipFrom('Case', 'Has_data')
    summary_of = RelationshipFrom('SummaryData', 'Neighbouring_data')
    summary_from = RelationshipTo('SummaryData', 'Neighbouring_data')
    citation_of = RelationshipFrom('CitationsData', 'Neighbouring_data')
    cited_from = RelationshipTo('CitationsData', 'Neighbouring_data')


class SummaryData(StructuredNode):
    case_no = StringProperty(required=True)
    evidence = StringProperty()
    conclusion = StringProperty()
    courts_reasoning = StringProperty()
    precedent_analysis = StringProperty()
    legal_analysis = StringProperty()
    respondents_arguments = StringProperty()
    petitioners_arguments = StringProperty()
    issues = StringProperty()
    facts = StringProperty()
    summary = StringProperty()

    # Relationships
    case = RelationshipFrom('Case', 'Has_data')
    summary_of = RelationshipFrom('SummaryData', 'Neighbouring_data')
    summary_from = RelationshipTo('SummaryData', 'Neighbouring_data')
    citation_of = RelationshipFrom('CitationsData', 'Neighbouring_data')
    cited_from = RelationshipTo('CitationsData', 'Neighbouring_data')

Node = ['Case', 'Court', 'ApplealedCase', 'CourtData', 'SummaryData', 'CitationsData']
Relationships = ['Appeal_from', 'Appeal_to', 'Is_case', 'Has_data', 'Neighbouring_data']
class CitationsData(StructuredNode):
    reference = StringProperty(unique_index=True, required=True)
    cases = RelationshipFrom('Case', 'CITED_BY')


class Counsel(StructuredNode):
    name = StringProperty(required=True)

    # Relationships
    cases = RelationshipFrom('Case', 'ARGUED_BY')
