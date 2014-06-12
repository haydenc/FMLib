import settings
import requests
from result_set import FileMakerResultSet
from lxml import etree

class FileMakerObjectManager(object):

    def __init__(self, schema=None, host=None, port=None, user=None, password=None, db=None, layout=None):
        self.schema = schema or settings.schema
        self.host = host or settings.host
        self.port = port or settings.port
        self.user = user or settings.user
        self.password = password or settings.password
        self.db = db or settings.db
        self.layout = layout or settings.layout

    @classmethod
    def create_from_config(cls):
        pass

    def get(self, **kwargs):
        action = 'find'
        results = self._perform_request(action, kwargs)
        if len(results) > 1:
            raise Exception('Get method returned more than one result')
        if len(results) == 0:
            raise Exception('Get method returned no result')
        return results[0]

    def all(self, order_by={}):
        return self.filter(order_by=order_by)

    def filter(self, order_by={}, **kwargs):
        action = 'findall'
        return self._perform_request(action, kwargs, order_by=order_by)

    def _flatten(self, string_data):
        flattened_dict = {}
        for (key, value) in string_data.items():
            if isinstance(value, list):
                pass
            else:
                flattened_dict[key] = value
        return flattened_dict

    def save(self, record):
        save_kwargs = self._flatten(record._string_data)
        if record.record_id:
            action = 'edit'
            save_kwargs.update({'-recid' : record.record_id})
        else:
            action = 'new'
        return self._perform_request(action, save_kwargs)

    def delete(self, record):
        """ Deletes the supplied record or record id """
        action = "delete"
        if isinstance(record, int):
            record_id = record
        else:
            record_id = record.record_id
        self._perform_request(action, {'-recid' : record_id})

    def _perform_request(self, action, parameters, order_by={}):
        # TODO: Construct order by params
        url = self._get_request_address(action)
        response = requests.get(url, params=parameters)
        print 'Request made to', response.url
        results = FileMakerResultSet(etree.XML(response.text.encode('UTF-8')), manager=self)
        if settings.cache_layout_metadata:
            self.metadata = results.metadata
        return results

    def _get_request_address(self, action):
        return '%s/fmi/xml/fmresultset.xml?-db=%s&-lay=%s&-%s' % (self._get_connection_string(), self.db, self.layout, action)

    def _get_connection_string(self):
        return '%s://%s:%s@%s:%s' % (self.schema, self.user, self.password, self.host, self.port)

    def _get_metadata(self):
        if getattr(self, 'metadata'):
            return self.metadata
        else:
            view_results = self.view()
            return view_results.metadata

    def convert_data_to_strings(self, typed_data):
        metadata = self._get_metadata()
        return metadata.convert_to_strings(typed_data)

    def convert_strings_to_data(self, string_data):
        metadata = self._get_metadata()
        return metadata.convert_from_strings(string_data)
