from exceptions import FMActionException
import settings
from metadata import FileMakerMetadata
from record import FileMakerRecord
from error_codes import FMErrorLookup


class FileMakerResultSet(object):

    def __init__(self, root_node, manager=None):
        self.tag = root_node
        self.check_errors()
        self.parse_metadata()
        self.position = 0
        self.results = self.tag.find(settings.RESULT_SET_TAG).findall(settings.RECORD_TAG)
        self.manager = manager
        self.metadata = None

    def check_errors(self):
        error_tag = self.tag.find(settings.ERROR_TAG)
        error_dict = dict(error_tag.items())
        error_code = int(error_dict['code'])
        if error_code != 0:
            # TODO: Custom exception type including type
            raise FMActionException(FMErrorLookup[error_code])

    def parse_metadata(self):
        metadata_tag = self.tag.find(settings.METADATA_TAG)
        datasource_tag = self.tag.find(settings.DATASOURCE_TAG)
        self.metadata = FileMakerMetadata(metadata_tag, datasource_tag)

    def parse_record(self, record_node):
        return FileMakerRecord(xml_node=record_node, manager=self.manager)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.results)

    def __getitem__(self, key):
        # TODO: Caching parsed records
        if isinstance(key, int):
            return self.parse_record(self.results[key])
        else:
            return [self.parse_record(rec) for rec in self.results[key]]

    def next(self):
        try:
            # TODO: Refactor this, could accidentally catch index error within FileMakerRecord or subclass parse_record
            # TODO: Introduce result-set caching - we don't want to re-read the XML every time.
            record = self.parse_record(self.results[self.position])
            self.position += 1
            return record
        except IndexError:
            raise StopIteration
