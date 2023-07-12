import json

d = {
    "userbots": [
        {
            "firstname": "",
            "lastname": "",
            "username": "",
            "sex": "M",
            "age": "20",
            "gpt_task": "ты играешь роль комментатора постов в социальных сетях. Пиши короткие комментарии, высказывая свое мнение по теме поста или соглашаясь с автором. Используй сленг. Пиши так, будто общаешься с друзьями.",
            "use_emoji": False,
            "formats": {
                "commenting_posts": True,
                "chat_in_comments": False,
                "chat_in_groups": False
            }
        }
    ]
}

# d['userbots'][0]['username'] = ''
# print(d)

# s = """
# {
#     "userbots": [
#         {
#             "firstname": "Ivan",
#             "lastname": "Ivanov"
#
#         }
#     ]
# }
# """
#
# dict_s = json.loads(s)
# dict_s['userbots'].append({'firstname': 'Leonardo', 'lastname': 'Brown'})
#
# new_json = json.dumps(dict_s)
#
# print(new_json)


test_s = '{"userbots": [{"firstname": "", "lastname": "", "username": "", "sex": "M", "age": "20", "gpt_task": "ты играешь роль комментатора постов в социальных сетях. Пиши короткие комментарии, высказывая свое мнение по теме поста или соглашаясь с автором. Используй сленг. Пиши так, будто общаешься с друзьями.", "use_emoji": false, "formats": {"commenting_posts": true, "chat_in_comments": false, "chat_in_groups": false}}]}'
dict_s = json.loads(test_s)

print(dict_s)
