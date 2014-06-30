from unittest import TestCase
import six

from .. import manager, settings, exceptions
import datetime
from exceptions import FMActionException
from record import FileMakerRecord

from numpy.random.mtrand import RandomState
import binascii
rand = RandomState()

NEW_PROJECT_DATA = {
    'Creation TimeStamp': None,
    'Tasks': None,
    'Status on Screen': None,
    'Description': None,
    'Due Date': None,
    'Project Name': None,
    'Days Elapsed': None,
    'Projects Browser': None,
    'Tag': None,
    'Project Completion Progress Bar': None,
    'Created By': None,
    'Start Date': None,
    'Days Remaining': None
}


class BaseManagerTest(TestCase):

    def setUp(self):
        self.settings = {
            'schema': 'http',
            'user': '',
            'password': '',
            'host': '127.0.0.1',
            'port': '80',
        }
        settings.update(self.settings)
        # We're using the FMServer_Sample database - projects + tasks.
        self.table_details = {
            'db': 'fmserver_sample',
            'layout': 'Projects'
        }
        self.manager = manager.FileMakerObjectManager(**self.table_details)

    # noinspection PyPep8Naming
    def runTest(self):
        return self.run_test()

    def run_test(self):
        pass

    def random_string(self):
        lo = 1000000000000000
        hi = 999999999999999999
        return binascii.b2a_hex(rand.randint(lo, hi, 2).tostring())[:30]


class TestDev(BaseManagerTest):

    def run_test(self):
        self.manager.all()


class TestGetEditSave(BaseManagerTest):

    def run_test(self):
        all_objects = self.manager.all()
        projects_count = len(all_objects)
        assert(isinstance(projects_count, int))
        first_project = all_objects[0]
        self.old_description = first_project.description
        first_project.description = 'My First Project'
        first_project.save()
        retrieved_project = self.manager.get(description='My First Project')
        # Make sure that we're updating when we save the changes to the first student, not creating a new row.
        assert(retrieved_project.record_id == first_project.record_id)
        project_1 = self.manager.get(description='My First Project')
        project_1.description = self.old_description
        project_1.save()


class TestTypeConversions(BaseManagerTest):

    def run_test(self):
        all_objects = self.manager.all()
        project_1 = all_objects[0]
        print project_1._data
        self.assertIsInstance(project_1._data['Due Date'], datetime.date)
        self.assertIsInstance(project_1._data['Description'], six.string_types)
        self.assertIsInstance(project_1._data['Days Elapsed'], float)
        # TODO: Assertions for all other types


class TestGetThrowsErrorOnMultiple(BaseManagerTest):

    def run_test(self):
        params = {'Created By': 'Tim Thomson'}
        self.assertRaises(exceptions.MultipleObjectsReturned, self.manager.get, **params)


class TestGetThrowsErrorOnZeroResults(BaseManagerTest):

    def run_test(self):
        params = {'Created By': 'Tom Turner'}
        self.assertRaises(exceptions.ZeroObjectsReturned, self.manager.get, **params)


class TestCreateNew(BaseManagerTest):

    def run_test(self):
        # TODO: Filter out unreasonable types for us to write to.

        record = FileMakerRecord(data=NEW_PROJECT_DATA)
        # TODO: Test that Rec-id is set when we save the record.
        record.save()
        record2 = self.manager.get(Description=NEW_PROJECT_DATA['Description'])
        for key, value in NEW_PROJECT_DATA.items():
            self.assertEqual(value, record2._data[key])


class TestEdit(BaseManagerTest):

    def run_test(self):
        record = self.manager.all()[0]
        initial_record_id = record.id
        new_description = self.random_string()
        record._data['Description'] = new_description
        record.save()

        # First we confirm that the initial record that we loaded has been updated, by loading it again.
        record2 = self.manager.get(recId=initial_record_id)
        self.assertEqual(record2._data['Description'], new_description)
        # Here we confirm that no new entry was created.
        record3 = self.manager.get(Description=new_description)
        self.assertEqual(record3.record_id, initial_record_id)


class TestEditMissing(BaseManagerTest):

    def edit_missing(self):
        record = self.manager.all()[0]
        # TODO: Lets not rely on this number not being used as an ID - lets generate high numbers and then see.
        record.record_id = 33030303
        record.save()

    def run_test(self):
        self.assertRaises(FMActionException, self.edit_missing)


class TestDelete(BaseManagerTest):

    def run_test(self):
        record = FileMakerRecord(data=NEW_PROJECT_DATA, manager=self.manager)
        record.save()
        rec_id = record.record_id
        self.manager.get(record_id=rec_id)
        self.assertIsNotNone(rec_id)
        record.delete()
        self.assertRaises(FMActionException, self.manager.get, record_id=rec_id)


class TestViewMethod(BaseManagerTest):

    def run_test(self):
        results_set = self.manager.view()
        assert(hasattr(results_set, 'metadata'))