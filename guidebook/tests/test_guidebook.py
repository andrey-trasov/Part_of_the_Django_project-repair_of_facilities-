from rest_framework import status

from ..models import GuideBook
from .base import BaseConstructionObjectTestCase


class GuideBookTestCase(BaseConstructionObjectTestCase):

    def test_base_guide_book_retrieve(self):
        """
        Тест, получение объекта по id
        """

        response = self.client_1.get(
            self.get_url(
                "pk_guidebook",
                pk_guidebook=self.base_guidebook_1.pk,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_guide_book_retrieve_left_user(self):
        """
        Тест, получение объекта по id пользователем не состоящем в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_3.get(
            self.get_url(
                "pk_guidebook",
                pk_guidebook=self.base_guidebook_1.pk,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_guide_book_list(self):
        """
        Тест, получение списка справочников
        """

        response = self.client_1.get(
            self.get_url("guidebook_list/pk_company", pk_company=self.company_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_guide_book_list_left_user(self):
        """
        Тест, получение списка справочников
        """

        response = self.client_3.get(
            self.get_url("guidebook_list/pk_company", pk_company=self.company_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_base_guide_book(self):
        """
        Тест, создание объекта владельцем компании
        """

        data = {
            "title": "Бетонирование пола",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_1.post(
            self.get_url("guidebook_create/pk_company", pk_company=self.company_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GuideBook.objects.count(), 3)

    def test_create_base_guide_book_error(self):
        """
        Тест, создание объекта мастером
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Бетонирование пола",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_2.post(
            self.get_url("guidebook_create/pk_company", pk_company=self.company_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GuideBook.objects.count(), 2)

    def test_create_base_guide_book_left_user(self):
        """
        Тест, создание объекта пользователем не работающим в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Бетонирование пола",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_3.post(
            self.get_url("guidebook_create/pk_company", pk_company=self.company_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GuideBook.objects.count(), 2)

    def test_base_guide_book_update(self):
        """
        Тест, изменение объекта по id владельцем компании
        """

        data = {
            "title": "Перекрытие крыши",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_1.put(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk),
            data,
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Перекрытие крыши")

    def test_base_guide_book_update_error(self):
        """
        Тест, изменение объекта по id мастером
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Перекрытие крыши",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_2.put(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_guide_book_update_left_user(self):
        """
        Тест, изменение объекта по id пользователем не работающим в компании
        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        data = {
            "title": "Перекрытие крыши",
            "company": self.company_1,
            "is_delete": False,
        }

        response = self.client_3.put(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_guide_book_delete(self):
        """
        Тест, удаление объекта по id деректором
        """

        response = self.client_1.delete(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_base_guide_book_delete_error(self):
        """
        Тест, удаление объекта по id мостером

        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_2.delete(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_base_guide_book_delete_left_user(self):
        """
        Тест, удаление объекта по id пользователем не работающим в компании

        должен выдать ошибку HTTP_403_FORBIDDEN
        """

        response = self.client_3.delete(
            self.get_url("change/pk_guidebook", pk_guidebook=self.base_guidebook_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
