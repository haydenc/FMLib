from FMLib.exceptions import ZeroObjectsReturned, MultipleObjectsReturned
import settings
import requests
from result_set import FileMakerResultSet
from lxml import etree


class FileMakerObjectManager(object):
    def __init__(self, schema=None, host=None, port=None, user=None, password=None, db=None, layout=None):
        self._schema = schema or settings.schema
        self._host = host or settings.host
        self._port = port or settings.port
        self._user = user or settings.user
        self._password = password or settings.password
        self._db = db or settings.db
        self._layout = layout or settings.layout

    def get_schema(self):
        """ Returns the schema - (http/https) """
        return self._schema

    def get_host(self):
        """ Returns the host address """
        return self._host

    def get_port(self):
        """ Returns the host port """
        return self._port

    def get_user(self):
        """ Returns the username to be used for http authentication """
        return self._user

    def get_password(self):
        """ Returns the username to be used for http authentication """
        return self._password

    def get_db(self):
        """ Returns the username to be used for http authentication """
        return self._db

    def get_layout(self):
        """ Returns the username to be used for http authentication """
        return self._layout

    def _get_connection_string(self):
        """ Returns a basic connection string - schema, host, port and http basic auth credentials"""
        return '%s://%s:%s@%s:%s' % \
               (self.get_schema(), self.get_user(), self.get_password(), self.get_host(), self.get_port())

    def _get_request_address(self, action):
        """ Returns a fully prepared URI, including the action parameter """
        return '%s/fmi/xml/fmresultset.xml?-db=%s&-lay=%s&-%s' % (
            self._get_connection_string(), self.get_db(), self.get_layout(), action)

    #####################
    # # Begin Actions # #
    #####################

    def list_db_names(self):
        """ Returns a list of database names """
        return self._perform_request('dbnames')

    def list_layout_names(self):
        """ Returns a list of layout names """
        return self._perform_request('layoutnames')

    def view(self):
        return self._perform_request('view')

    def get(self, **kwargs):
        results = self._perform_request('find', kwargs)
        if len(results) > 1:
            raise MultipleObjectsReturned('Get method returned more than one result')
        if len(results) == 0:
            raise ZeroObjectsReturned('Get method returned no result')
        return results[0]

    def all(self, order_by=None):
        order_by = order_by or {}
        return self.filter(order_by=order_by)

    def filter(self, order_by=None, **kwargs):
        order_by = order_by or {}
        return self._perform_request('findall', kwargs, order_by=order_by)

    @staticmethod
    def _flatten(string_data):
        flattened_dict = {}
        for (key, value) in string_data.items():
            if isinstance(value, list):
                pass
            else:
                flattened_dict[key] = value
        return flattened_dict

    def save(self, record):
        save_kwargs = self._flatten(record.get_string_data())
        if record.record_id:
            action = 'edit'
            save_kwargs.update({'-recid': record.record_id})
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
        self._perform_request(action, {'-recid': record_id})

    def _perform_request(self, action, parameters=None, order_by=None):
        order_by = order_by or {}
        parameters = parameters or {}
        # TODO: Construct order by params
        url = self._get_request_address(action)
        response = requests.get(url, params=parameters)
        print 'Request made to', response.url
        results = FileMakerResultSet(etree.XML(response.text.encode('UTF-8')), manager=self)
        if settings.cache_layout_metadata:
            self.metadata = results.metadata
        return results

    def _get_metadata(self):
        if hasattr(self, 'metadata'):
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