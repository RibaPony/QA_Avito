import requests
import pytest
import re

class Test_API:
    
    @pytest.mark.parametrize(
            "uuid, status",
            [
                ("c66f214f-e103-441c-b9bf-474d3fd028ea", 200), #созданное объявление
                ("!", 404), #негативно проверяем, спец символ, пробел, отрицательные и не uuid значения
                ("ca1-123-cc", 404),
                (" ", 404),
                (-1, 404),
            ]
    )
    def test_take_card(self, uuid, status):
        data = requests.get(f"https://qa-internship.avito.com/api/1/item/{uuid}")
        assert data.status_code == status


    @pytest.mark.parametrize(
            "seller_id, status",
            [
                (953800, 200), #первые 2 значения в интервале, у одного продавца 0 объявлений, у другого есть созданные
                (953891, 200),
                (123, 404), #диапазон ID от 111 111 до 999 999, проверяем значения меньше, больше, отрицательные и спец символы. 
                            #На данные запросы должен возвращаться 404/400 статус код, в методе получения объявления возвращается 404, ставлю ее
                (12345678, 404), 
                (-1, 404), 
                ("!", 404),
                (" ", 404),
            ]
    )
    def test_take_cards(self, seller_id, status):
        data = requests.get(f"https://qa-internship.avito.com/api/1/{seller_id}/item")
        assert data.status_code == status

    @pytest.mark.parametrize(
            "name, price, sellerId, contacts, likes, viewCount, status",
            [
                #не считаю, что полям статистики необходимо тестирование, так как в реальных задачах такие данные не указываются, а подсчитываются системой
                ("Ноутбук", 50999, 953891, 0, 0, 0, 200), #проверяем положительную ситуацию

                ("Ноутбук", 50000, "", 0, 0, 0, 500), #можно ли оставить поле sellerID пустым, фактически токен, сервер вернул 500, ставлю ее
                (-1, 50000, 953891, 0, 0, 0, 500), #можно ли передать в текстовое поле число
                ("Ноутбук", "50000", 953891, 0, 0, 0, 500), #можно ли передавать в числовое поле текст
                ("Ноутбук", 50000, "953891", 0, 0, 0, 500),
                ("Ноутбук", 50000.5, 953891, 0, 0, 0, 500), #можно ли установить цену с копейками


                (None, 50000, 953891, 0, 0, 0, 400), #можно ли оставить обязатльные поля пустыми
                ("Ноутбук", None, 953891, 0, 0, 0, 400),
                ("Ноутбук", 50000, None, 0, 0, 0, 400),
                ("Ноутбук", -100, 953891, 0, 0, 0, 400), #можно ли установить отрицательную цену
                ("Ноутбук", 0, 953891, 0, 0, 0, 400), #можно ли установить нулевую цену
                
            ]
    )
    def test_create_card(self, name, price, sellerId, contacts, likes, viewCount, status):
        body = {
            "statistics": {
                "contacts": contacts,
                "likes": likes,
                "viewCount": viewCount
        }
        }
        #можно ли отправить тело запроса без обязательных параметров: цены, названия и продавца
        if price is not None:
            body["price"] = price

        if name is not None:
            body["name"] = name

        if sellerId is not None:
            body["sellerId"] = sellerId

        
        print(body)
        data = requests.post("https://qa-internship.avito.com/api/1/item", json = body)

        assert data.status_code == status
