import settings
from lxml import etree
import six

class FileMakerRecord(object):
    _xml_string, _xml_node, _string_data, _data, record_id = (None,) * 5
    def __init__(self, xml_string=None, xml_node=None, string_data=None, data=None, manager=None, record_id=None, mod_id=None):
        # TODO: Raise an exception if zero or more than one of the constructor kwargs has been provided
        # TODO: This init method is messy
        # Keep a reference to the manager in case we decide to update this record
        self.manager = manager
        record_node = None
        if xml_string:
            xml_node = etree.XML(xml_string)
        if xml_node is not None:
            self._tag = xml_node
            self._tag_dict = dict(self._tag.items())
            # TODO: Is this an appropriate place to retrieve the record and mod ids? Meh
            self.record_id = self._tag_dict['record-id']
            self.mod_id = self._tag_dict['mod-id']
            string_data = self._process_tag()
        if string_data:
            self._string_data = string_data
            self._parse_values()
        if data:
            self.data = data
            self._serialize_values()

    def update_value(self, key, value=None):
        """ Method to update the data for this record """
        if isinstance(key, six.string_types):
            values_dict = { key : value }
        else:
            values_dict = key
        self._data.update(values_dict)
        self._serialize_values()

    def update_string_value(self, key, value=None):
        # TODO: Consider abstracting these two functions to match each other
        """ Method to update the data for this record with the provided string values """
        if isinstance(key, six.string_types):
            values_dict = { key : value }
        else:
            values_dict = key
        self._string_data.update(values_dict)
        self._parse_values()

    def delete(self):
        manager = self._get_manager()
        manager.delete(self)

    def save(self):
        manager = self._get_manager()
        manager.save(self)

    def _get_manager(self):
        if hasattr(self, 'manager'):
            return self.manager
        else:
            # Will throw an error if the global config does not provide everything we need
            return FileMakerObjectManager.create_from_config()

    def _process_tag(self):
        _string_data = self._extract_set_data(self._tag)
        related_set_tags = self._tag.findall(settings._RELATED_SET_TAG)
        for related_set_tag in related_set_tags:
            related_set_name = dict(related_set_tag.items())['table']
            _string_data[related_set_name] = [self._extract_set_data(record) for record in related_set_tag.findall(settings._RECORD_TAG)]
        return _string_data

    def _extract_set_data(self, set_tag):
        _string_data = {}
        field_tags = set_tag.findall(settings._FIELD_TAG)
        for f_tag in field_tags:
            items_dict = dict(f_tag.items())
            field_name = items_dict['name']
            field_value = f_tag.find(settings._DATA_TAG).text
            _string_data[field_name] = field_value
        return _string_data

    def _parse_values(self):
        # If we don't have a manager we can't get the metadata and we don't know the types without the metadata.
        manager = self._get_manager()
        self._data = manager.convert_strings_to_data(self._string_data)

    def _serialize_values(self):
        # If we don't have a manager we can't get the metadata.
        manager = self._get_manager()
        self._string_data = manager.convert_data_to_strings(self._data)
