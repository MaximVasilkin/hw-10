import csv
import re


def fix_contacts(file_name):
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)

    pattern_name = r'([А-Я]\w+).([А-Я]\w+).([А-Я]\w+)?'
    pattern_phone = '(\+7|8)([ \(]+|)(\d{3})([\)\- ]+|)(\d{3})([- ]+|)(\d{2})([- ]+|)(\d{2})([ \(]+(доб.).(\d+)(\)|))?'

    counter = 1
    names = {}

    for contact in contacts_list[1:]:
        text = ' '.join(contact[:3])
        name_list = re.findall(pattern_name, text)[0]
        phone = re.sub(pattern_phone, '+7(\\3)\\5-\\7-\\9 \\11\\12', contact[-2])
        phone = phone if 'доб' in phone else phone[:-1]
        contact[-2] = phone
        contact[0], contact[1], contact[2] = name_list
        contacts_list[counter] = contact
        counter += 1
        last_and_firstname = ' '.join(name_list[:-1])
        if last_and_firstname not in names:
            names[last_and_firstname] = dict.fromkeys(contacts_list[0][2:], '')
        for key, value in zip(contacts_list[0][2:], contact[2:]):
            names[last_and_firstname][key] = value if value else names[last_and_firstname].get(key, '')

    new_file = [contacts_list[0], *[name.split(' ') + list(info.values()) for name, info in names.items()]]

    with open(f'fixed_{file_name}', 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_file)


if __name__ == '__main__':
    fix_contacts('phonebook_raw.csv')
