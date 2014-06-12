import requests
from lxml import etree
from manager import FileMakerObjectManager
import settings as fm_settings

glob_settings = {
    'schema' : 'http',
    'user' : 'developer',
    'password' : 'd3v3l0p3r',
    'host' : '127.0.0.1',
    'port' : '80',
}

fm_settings.update(glob_settings)

user_manager_settings = {
    'db' : 'CommunityGrants',
    'layout' : '__USERS'
}

user_manager = FileMakerObjectManager(**user_manager_settings)

all_users = user_manager.all()

users_count = len(all_users)
first_user = all_users[0]
first_ten_users = all_users[0:10]

user_by_name = user_manager.get(First_Name='Christine')
assert(user_by_name._data['First_Name']=='Christine')

user_to_change = all_users[5]
user_to_change.update_value('First_Name', 'Eugienie')

user_to_change.save()

changed_user = user_manager.get(**{'-recid' : user_to_change.record_id})
assert(changed_user._data['First_Name']=='Eugienie')

#####################
### XML TAG NAMES ###
#####################

#connection_string = '%s://%s:%s@%s:%s' % (schema, user, password, host, port)
#resource_string = '%s/fmi/xml/fmresultset.xml?-db=%s&-lay=%s&-%s' % (connection_string, db, layout, action)

#xml_result = requests.get(resource_string)

#root = etree.XML(xml_result.text.encode('UTF-8'))

#results = FileMakerResultSet(root)

#flat_results = [a for a in results]

#metadata = root.find(METADATA_TAG)
#result_set = root.find(RESULT_SET_TAG)

#records = resultset.findall(RECORD_TAG)

import pdb; pdb.set_trace()

