# This module acts as a singleton to hold library settings.

_BASE_TAG_STRUCTURE = '{http://www.filemaker.com/xml/fmresultset}%s'
_RESULT_SET_ROOT_TAG = _BASE_TAG_STRUCTURE % 'fmresultset'
_RESULT_SET_TAG = _BASE_TAG_STRUCTURE % 'resultset'
_METADATA_TAG = _BASE_TAG_STRUCTURE % 'metadata'
_FIELD_DEFINITION_TAG = _BASE_TAG_STRUCTURE % 'field-definition'
_RELATED_SET_DEFINITION_TAG = _BASE_TAG_STRUCTURE % 'relatedset-definition'
_RECORD_TAG = _BASE_TAG_STRUCTURE % 'record'
_FIELD_TAG = _BASE_TAG_STRUCTURE % 'field'
_DATA_TAG = _BASE_TAG_STRUCTURE % 'data'
_RELATED_SET_TAG = _BASE_TAG_STRUCTURE % 'relatedset'
_ERROR_TAG = _BASE_TAG_STRUCTURE % 'error'
_DATASOURCE_TAG = _BASE_TAG_STRUCTURE % 'datasource'
_RECORD_TAG = _BASE_TAG_STRUCTURE % 'record'

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
# 'AUTO' will dynamically switch between HARSH and False based on the non-numeric field setting # TODO: Implement 'AUTO'

def update(settings_dict):
    import sys
    thismodule = sys.modules[__name__]
    for (key, value) in settings_dict.items():
        setattr(thismodule, key, value)
