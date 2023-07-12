unknown_error_answer = """
🤖🚫
Что-то пошло не так :("""

invalid_channel_number_answer = """
🤖🚫
Ошибка! Сообщение должно содержать только одно число - номер группы.
Например: "1" """

invalid_channel_info_answer = """
🤖🚫
Ошибка в формате ввода. Попробуйте еще раз.

Вводите название группы и ссылку на нее в одном сообщении!"""

bad_link_error_answer = """
🤖🚫
Указана неверная ссылка. Проверьте корректность написания ссылки и повторите еще раз!"""

invalid_email_value_type = """
🤖🚫
Некорректный e-mail, попробуйте еще раз"""

RateLimitError_answer = """
🤖🚫
Слишком много запросов. Попробуйте повторить запрос позже"""

InvalidRequestError_answer = """
🤖🚫
Произошла ошибка. Пожалуйста, повторите запрос"""

start_answer = """
Привет, {first_name} 👋
[ текст ]

/my_channels 'Мои каналы'
/my_userbots 'Мои юзерботы'
/start_userbots 'Начать автокомментинг"""

help_answer = """
🤖
Команды:

/about - обо мне.
/profile - профиль пользователя.
/forget - очистить память нейросети.
/image - сгенерировать изображение по текстовому запросу.

Все остальные сообщения будут восприниматься как запрос к ChatGPT.

❗️Прежде чем сменить тему общения с ботом или перейти на другой язык, нажмите /forget."""

about_answer = """
🤖
ChatGPT — чат-бот с искусственным интеллектом, способный работать в диалоговом режиме, поддерживающий запросы на естественных языках.
ChatGPT может вести диалог, отвечать на вопросы любой сложности, писать код на разных языках программирования, искать ошибки в коде, сочинять стихи, писать сценарии и многое другое.
ChatGPT может использовать в общении разные языки, но мы рекомендуем вести общение на английском. Так бот будет работать более корректно, а вы сможете сэкономить свои токены (1000 токенов ~ 700 английских слов или 150 слов другого языка)."""

forget_answer = """
🤖
Вы успешно очистили память бота!"""

profile_answer = """
👤 {user_name}
Подписка: {user_subscription}"""

channels_list_is_empty_message = """
У вас нет подключенных каналов"""

userbots_list_is_empty_message = """
У вас нет подключенных юзерботов"""

channels_list_message = """
Список каналов:

{channels_list}

Стр. {page_number}/{total_number_of_pages}"""

userbots_list_message = """
<b>Ваши юзерботы:</b>

- Имя: <b><i>{firstname}</i></b>
- Фамилия: <b><i>{lastname}</i></b>
- Username: <i>{username}</i>

- Пол: <i>{sex}</i>
- Возраст: <i>{age}</i>
- Использование эмодзи: <i>{use_emoji}</i>
- Задача GPT: 
<code>{gpt_task}</code>

- Поддерживаемые форматы:
    - Комментирование постов: <i>{commenting_posts}</i>
    - Общение в комментариях: <i>{chat_in_comments}</i>
    - Общение в группах: <i>{chat_in_groups}</i>

<b>№ {page_number}/{total_number_of_pages}</b>"""

buy_no_email_answer = """
🤖
Введите адрес электронной почты для получения чеков"""

add_channel_message = """
Введите ссылки на каналы (не больше 100) в следующем формате:

@канал_1
@канал_2
@канал_3
...

ВАЖНО! Каждая ссылка должна быть на новой строке."""

channel_added_message = """
Каналы успешно добавлены!"""

channel_deleted_message = """
Группа успешно удалена!"""

input_channel_to_delete_number_message = """
Введите одно число - номер группы, которую хотите удалить из списка"""

select_subscription_message = """
🤖
<b>GPT</b> - <i>100 руб.</i> - месяц безлимитного доступа к нейросети ChatGPT!   

<b>VIP</b> - <i>250 руб.</i> - месяц безлимитного доступа к нейросетям ChatGPT и DALL-E (для генерации изображений). Все запросы обрабатываются отдельно. Это повышает скорость ответа и снижает ограничение на частоту запросов!
"""

choose_subscription_type_answer = """
🤖
Поздравляю! Вы оформили подписку {subscription_type}"""

while_answer_is_generating_answer = """
🤖 Генерирую ответ..."""

telegram_logs_permission_symbols = ['❌', '✅']

ask_gpt_without_subscribe_answer = """
🤖🚫
Вы не можете отправлять запросы без подписки. Если вы хотите оформить подписку, перейдите в свой профиль, нажав /profile"""

ban_answer = """
🤖🚫
Вы были забанены администратором."""

ask_dalle_without_subscribe_answer = """
🤖🚫
Вы не можете генерировать изображения без подписки VIP. Если вы хотите оформить подписку, перейдите в свой профиль, нажав /profile"""

image_command_answer = """
🤖
Введите текст запроса"""

choose_image_size_message = """
🤖
Выберите качество изображения"""

generating_image_message = """
🤖 Генерирую изображение..."""

openai_dalle_error_message = """
🤖🚫
Произошла ошибка на сервере DALL-E :(\nПопробуйте повторить запрос"""

openai_dalle_bad_request_error_message = """
🤖🚫
Ошибка! Введенный вами запрос является некорректным с точки зрения DALL-E.\nПопробуйте повторить запрос, изменив формулировку"""

select_user_answer = """
🤖
Введите id пользователя"""

select_new_status_answer = """
🤖
Статус пользователя {user_id} изменен на {new_status}"""

stat_answer = """
🤖
Статистика, собранная в период
От   {date_start}
До   {today}

- Новых пользователей: {num_of_new_users}
- Запросов отправлено: {num_of_new_requests}
- Ответов получено: {num_of_new_answers}
- Токенов потрачено: {num_of_tokens}

Общая статистика:
- Пользователи: {total_num_of_users}
- Количество запросов: {total_number_of_messages}
- Сгенерированные изображения: {total_number_of_images}"""

admin_funcs_info_answer = """
⚙ admin panel ⚙

/stat - статистика
/select_user - данные пользователя
/setup_telegram_logs - настройка логов
/send_to_users (message) - рассылка
"""

payment_link_message = """
🤖
Ссылка на оплату: {payment_link}"""

subscription_finished_message = """
🤖🚫
Срок вашей подписки истек. Если вы хотите обновить подписку, перейдите в свой профиль"""

message_to_user_message = """
🤖
Введите текст сообщения"""

message_to_user_sent_message = """
🤖
Сообщение отправлено!"""
