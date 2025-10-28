

def get_form_text(username: str | None, kwargs: dict) -> str:
    male = kwargs.get('male')
    name = kwargs.get('name')
    age = kwargs.get('age')
    city = kwargs.get('city')
    origin = kwargs.get('origin')
    children = kwargs.get("children")
    about = kwargs.get('about')
    contact = kwargs.get('contact')
    married = kwargs.get('married')
    text = (f'<b>{"Мужская анкета" if male == "men" else "Женская анкета"}</b> от пользователя: {username}\n\nЗовут: {name}\nВозраст: {age}\n'
            f'Город: {city}\nСемейное положение: {married}\nНациональность: {origin}\nНаличие детей: {children}\n'
            f'О себе: <blockquote expandable>{about}</blockquote>\n\nКонтактные данные: {contact}\n')
    return text
