from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password = valid_password):
    """Проверяем что данные email и пароля корректные и мы можем получить ключ"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что список животных не пустой"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Vasya', animal_type='cat',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Baskov", "dog", "4", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Tuzik', animal_type='Bird', age='3'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 1 позитивный
def test_add_new_pet_with_valid_data_without_photo(name='Barsik', animal_type='goat',
                                     age='5'):
    """Проверяем что можно добавить питомца с корректными данными без фотографии"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест 2 позитивный
def test_add_photo_of_pet(pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить фотографию питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем добавить фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и значение pet_photo не пустое (фото добавлено)
        assert status == 200
        assert result['pet_photo'] != ""
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 3 негативный
def test_get_api_key_for_invalid_user_email(email="invalidemail@mail.ru", password = valid_password):
    """Проверяем что тест провалится с некорректными данными email"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

# Тест 4 негативный
def test_get_api_key_for_invalid_user_password(email=valid_email, password = "invalidpassword"):
    """Проверяем что тест провалится с некорректными данными пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 200

# Тест 5 негативный
def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем что тест провалится с некорректными данными api ключа"""
    auth_key = "123456789qwerty"
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Тест 6 негативный
def test_add_new_pet_with_invalid_age(name='Vasya', animal_type='cat',
                                     age='-22', pet_photo='images/cat1.jpg'):
    """Проверяем что тест провалится при добавлении питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    if status == 200:
        print('Тест не пройден. Ошибка в API сайта PetFriends. Возраст не может быть отрицательным')

# Тест 7 негативный
def test_add_new_pet_with_invalid_animal_type(name='Vasya', animal_type='123',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что тест провалится при добавлении питомца с цифровым наименованием типа животного """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    if status == 200:
        print('Тест не пройден. Ошибка в API сайта PetFriends. Тип животного не может состоять из цифр')

# Тест 8 негативный
def test_get_all_pets_with_invalid_filter(filter='ivalid_filter'):
    """Проверяем что тест провалится с некорректными данными фильтра"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Тест 9 негативный
def test_add_new_pet_with_invalid_animal_name(name='', animal_type='dog',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что тест провалится при добавлении питомца с без имени """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    if status == 200:
        print('Тест не пройден. Ошибка в API сайта PetFriends. Поле для имени питомца не может быть пустым')

# Тест 10 негативный
def test_add_invalid_photo_of_pet(pet_photo=''):
    """Проверяем что тест провалится если не прикрепить фотографию питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем добавить фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и значение pet_photo не пустое (фото добавлено)
        assert status == 200
        assert result['pet_photo'] != ""
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
