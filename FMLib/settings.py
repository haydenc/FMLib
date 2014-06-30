# This module acts as a singleton to hold library settings.

BASE_TAG_STRUCTURE = '{http://www.filemaker.com/xml/fmresultset}%s'
RESULT_SET_ROOT_TAG = BASE_TAG_STRUCTURE % 'fmresultset'
RESULT_SET_TAG = BASE_TAG_STRUCTURE % 'resultset'
METADATA_TAG = BASE_TAG_STRUCTURE % 'metadata'
FIELD_DEFINITION_TAG = BASE_TAG_STRUCTURE % 'field-definition'
RELATED_SET_DEFINITION_TAG = BASE_TAG_STRUCTURE % 'relatedset-definition'
RECORD_TAG = BASE_TAG_STRUCTURE % 'record'
FIELD_TAG = BASE_TAG_STRUCTURE % 'field'
DATA_TAG = BASE_TAG_STRUCTURE % 'data'
RELATED_SET_TAG = BASE_TAG_STRUCTURE % 'relatedset'
ERROR_TAG = BASE_TAG_STRUCTURE % 'error'
DATASOURCE_TAG = BASE_TAG_STRUCTURE % 'datasource'

schema = 'http'
host = None
port = 80
user = None
password = None
db = None
layout = None
cache_layout_metadata = True
number_conversion = 'HARSH'
# Options: False, 'HARSH', 'ERROR'
# False will leave it as a string
# 'HARSH' will strip non numeric characters
# 'ERROR' will raise an exception
# TODO: Implement 'AUTO'
# 'AUTO' will dynamically switch between HARSH and False based on the non-numeric field setting


def update(settings_dict):
    import sys
    this_module = sys.modules[__name__]
    for (key, value) in settings_dict.items():
        setattr(this_module, key, value)
