import settings
from datetime import datetime
import re

class FileMakerField(object):
    def __init__(self, field_node):
        self.tag = field_node
        self.tag_dict = dict(self.tag.items())
        self.type = self.tag_dict['result']
        self.name = self.tag_dict['name']

class BaseResultSet(object):
    fields = []
    fields_dict = {}

    def __init__(self, metadata_node):
        self.metadata_tag = metadata_node
        self.process_field_definitions()

    def process_field_definitions(self):
        tags = self.metadata_tag.findall(settings._FIELD_DEFINITION_TAG)
        for tag in tags:
            field = FileMakerField(tag)
            self.append_field(field.name, field)

    def append_field(self, field_name, field):
        self.fields.append(field)
        self.fields_dict[field_name] = field

    def get_field_type_by_name(self, field_name):
        return self.fields_dict[field_name].type

class FileMakerRelatedSetMetadata(BaseResultSet):
    def __init__(self, metadata_node):
        # We use the table name as the reference 
        self.table_name = dict(metadata_node.items())['table']
        super(FileMakerRelatedSetMetadata, self).__init__(metadata_node)

class FileMakerMetadata(BaseResultSet):
    related_sets = []
    related_sets_dict = {}

    def __init__(self, metadata_node, datasource_tag):
        super(FileMakerMetadata, self).__init__(metadata_node)
        self.process_related_sets()
        self.datasource_tag = datasource_tag
        self.datasource_items = dict(datasource_tag.items())

    def get_field_type_by_name(self, field_name, related_set_name=None):
        if related_set_name:
            return self.related_sets_dict[related_set_name].get_field_type_by_name(field_name)
        else:
            return super(FileMakerMetadata, self).get_field_type_by_name(field_name)

    def process_related_sets(self):
        tags = self.metadata_tag.findall(settings._RELATED_SET_DEFINITION_TAG)
        for tag in tags:
            related_set = FileMakerRelatedSetMetadata(tag)
            self.related_sets.append(related_set)
            self.related_sets_dict[related_set.table_name] = related_set

    def convert_to_strings(self, string_dict):
        converted_data = {}
        for (key, value) in string_dict.items():
            if isinstance(value, list):
                # value is a list of related records
                converted_data_list = []
                for item in value:
                    # item is an individual related record
                    iconverted_data = {}
                    for (ikey, ivalue) in item.items():
                        field_type = self.get_field_type_by_name(ikey, key)
                        iconverted_data[ikey] = self._convert(field_type, ivalue, True)
                    converted_data_list.append(iconverted_data)
                converted_data[key] = converted_data_list
            else:
                field_type = self.get_field_type_by_name(key)
                converted_data[key] = self._convert(field_type, value, True)
        return converted_data

    def convert_from_strings(self, typed_dict):
        converted_data = {}
        for (key, value) in typed_dict.items():
            if isinstance(value, list):
                # value is a list of related records
                converted_data_list = []
                for item in value:
                    # item is an individual related record
                    iconverted_data = {}
                    for (ikey, ivalue) in item.items():
                        field_type = self.get_field_type_by_name(ikey, key)
                        iconverted_data[ikey] = self._convert(field_type, ivalue)
                    converted_data_list.append(iconverted_data)
                converted_data[key] = converted_data_list
            else:
                field_type = self.get_field_type_by_name(key)
                converted_data[key] = self._convert(field_type, value)
        return converted_data

    def _convert(self, field_type, value, to_string=False):
        direction = 'from' if to_string else 'to'
        try:
            conversion_method = getattr(self, '_convert_%s_%s' % (direction, field_type))
            return conversion_method(value)
        except AttributeError:
            # TODO: Custom exceptions
            raise Exception('Conversions for type "%s" not available. Extend the FileMakerMetadata class with a "_convert_from_{{type}}" method.' % field_type)

    def _convert_to_text(self, string_value):
        # TODO: Check encoding - should we encode to UTF here?
        return string_value

    def _convert_from_text(self, text_value):
        return text_value

    def _convert_to_date(self, string_value):
        return datetime.strptime(string_value, self._get_date_format())

    def _convert_from_date(self, date_value):
        return date_value.strftime(self._get_date_format())

    def _convert_to_number(self, string_value):
        if string_value == None:
            return None
        if not settings.number_conversion:
            return string_value
        if settings.number_conversion == 'HARSH':
            return float(re.sub("[^0-9.]", "", string_value) or 0)
        if setting.number_conversion == 'ERROR':
            try:
                return float(string_value)
            except:
                # TODO: Custom exceptions
                raise Exception('Unable to parse value as a number')

    def _convert_from_number(self, number_value):
        return str(number_value)

    def _get_date_format(self):
        # TODO: This should come from the datasource node, but we have to convert format string flavours
        return '%m/%d/%Y'

    def _get_time_format(self):
        # TODO: This should come from the datasource node, but we have to convert format string flavours
        return '%m/%d/%Y'

    def _get_datetime_format(self):
        # TODO: This should come from the datasource node, but we have to convert format string flavours
        return '%m/%d/%Y'