from rest_framework import status

from ..models import Work
from .base import BaseConstructionObjectTestCase


class BaseWorkTestCase(BaseConstructionObjectTestCase):

    def test_base_work_retrieve(self):
        """
        Тест, получение объекта по id
        """

        response = self.client_1.get(
            self.get_url(
                "pk_work",
                pk_work=self.base_work_1.pk,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_work_retrieve_left_user(self):
        """
        Тест, получение объекта по id пользователем не состоящем в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_3.get(
            self.get_url(
                "pk_work",
                pk_work=self.base_work_1.pk,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_work_list(self):
        """
        Тест, получение списка объектов
        """

        response = self.client_1.get(
            self.get_url(
                "work_list/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_work_list_left_user(self):
        """
        Тест, получение списка объектов пользователем из другой компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_3.get(
            self.get_url(
                "work_list/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_base_work(self):
        """
        Тест, создание объекта владельцем компании
        """

        data = {
            "guidebook": self.base_guidebook_1.pk,
            "title": "Оклейка стен",
            "price_by_unit": 3000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_1.post(
            self.get_url("work_create"),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Work.objects.count(), 3)

    def test_create_base_work_error(self):
        """
        Тест, создание объекта мастером
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "guidebook": self.base_guidebook_1.pk,
            "title": "Оклейка стен",
            "price_by_unit": 3000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_2.post(
            self.get_url("work_create"),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Work.objects.count(), 2)

    def test_create_base_work_left_user(self):
        """
        Тест, создание объекта пользователем не работающим в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "guidebook": self.base_guidebook_1.pk,
            "title": "Оклейка стен",
            "price_by_unit": 3000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_3.post(
            self.get_url("work_create"),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Work.objects.count(), 2)

    def test_base_work_update(self):
        """
        Тест, изменение объекта по id владельцем компании
        """

        data = {
            "title": "Перекрытие крыши",
            "guidebook": self.base_guidebook_1.pk,
            "price_by_unit": 10000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_1.put(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk),
            data,
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Перекрытие крыши")

    def test_base_work_update_error(self):
        """
        Тест, изменение объекта по id мастером
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Перекрытие крыши",
            "guidebook": self.base_guidebook_1.pk,
            "price_by_unit": 10000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_2.put(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_work_update_left_user(self):
        """
        Тест, изменение объекта по id пользователем не работающим в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Перекрытие крыши",
            "guidebook": self.base_guidebook_1.pk,
            "price_by_unit": 10000,
            "unit_of_measurement": Work.UnitType.SQUARE_METER,
            "currency": Work.CurrencyType.RUB,
            "is_delete": False,
        }

        response = self.client_3.put(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_work_delete(self):
        """
        Тест, удаление объекта по id деректором
        """

        response = self.client_1.delete(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_base_work_delete_error(self):
        """
        Тест, удаление объекта по id мостером

        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_2.delete(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_work_delete_left_user(self):
        """
        Тест, удаление объекта по id пользователем не работающим в компании

        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_2.delete(
            self.get_url("change_work/pk_work", pk_work=self.base_work_1.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
