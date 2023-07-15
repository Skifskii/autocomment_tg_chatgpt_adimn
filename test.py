import json

d = {
    "userbots": [
        {
            "api_data": {
                "phone": "+79094009878",
                "password": "56e5414d9bdF",
                "telegram_id": "5592822561",
                "api_id": 28579817,
                "api_hash": "6c4a628de1b7b5a4461248d2683d45d4"
            },
            "firstname": "Азнаур",
            "lastname": "Хизкияев",
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

# test_s = '{"userbots": [{"firstname": "", "lastname": "", "username": "", "sex": "M", "age": "20", "gpt_task": "ты играешь роль комментатора постов в социальных сетях. Пиши короткие комментарии, высказывая свое мнение по теме поста или соглашаясь с автором. Используй сленг. Пиши так, будто общаешься с друзьями.", "use_emoji": false, "formats": {"commenting_posts": true, "chat_in_comments": false, "chat_in_groups": false}}]}'
json_s = json.dumps(d)

print(json_s)
