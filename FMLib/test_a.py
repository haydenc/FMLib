first_user = all_users[0]
first_ten_users = all_users[0:10]

user_by_name = user_manager.get(First_Name='Christine')
assert(user_by_name._data['First_Name']=='Christine')

user_to_change = all_users[5]
user_to_change.update_value('First_Name', 'Eugienie')

user_to_change.save()

changed_user = user_manager.get(**{'-recid' : user_to_change.record_id})
assert(changed_user._data['First_Name']=='Eugienie')
