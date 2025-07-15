from rest_framework.test import APIClient, APITestCase

from company.models import ClientCompany, Company, CompanyRoleUser
from core.base.utils import GetUrlUtils
from guidebook.apps import GuidebookConfig
from guidebook.models import GuideBook, Work
from users.models import User


class BaseConstructionObjectTestCase(APITestCase, GetUrlUtils):
    module_name = GuidebookConfig.name

    def setUp(self):
        """
        создаем бд
        """
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_3 = APIClient()
        self.user_1 = User.objects.create_user(
            email="user_1@gmail.com",
            password="12345678",
            first_name="Ivan_1",
            second_name="Ivanov_1",
            third_name="Ivanov_2",
            phone_number="+70000000001",
        )

        self.user_2 = User.objects.create_user(
            email="user_2@gmail.com",
            password="12345678",
            first_name="Ivan_2",
            second_name="Ivanov_2",
            third_name="Ivanov_2",
            phone_number="+70000000002",
        )

        self.user_3 = User.objects.create_user(
            email="user_3@gmail.com",
            password="12345678",
            first_name="Ivan_2",
            second_name="Ivanov_2",
            third_name="Ivanov_2",
            phone_number="+70000000003",
        )

        self.company_1 = Company.objects.create(
            name="ООО",
            address="улица ленина 1",
            email="company_1@gmail.com",
            inn="0000000010",
            company_type="self_employed",
            is_delete=False,
        )

        self.company_2 = Company.objects.create(
            name="ОАО",
            address="улица ленина 2",
            email="company_2@gmail.com",
            inn="000000000012",
            company_type="limited_liability_company",
            is_delete=False,
        )

        self.company_role_user_1 = CompanyRoleUser.objects.create(
            user=self.user_1,
            company=self.company_1,
            role=CompanyRoleUser.RoleType.DIRECTOR,
        )

        self.company_role_user_2 = CompanyRoleUser.objects.create(
            user=self.user_1,
            company=self.company_1,
            role=CompanyRoleUser.RoleType.AUTHOR,
        )

        self.company_role_user_3 = CompanyRoleUser.objects.create(
            user=self.user_2,
            company=self.company_1,
            role=CompanyRoleUser.RoleType.MASTER,
        )

        self.company_role_user_4 = CompanyRoleUser.objects.create(
            user=self.user_3,
            company=self.company_2,
            role=CompanyRoleUser.RoleType.AUTHOR,
        )

        self.client_user_company = ClientCompany.objects.create(
            company=self.company_1,
            user=self.user_1,
            first_name="Ivan",
            second_name="Ivanov",
            third_name="Ivanov",
            email="ivan.petrov@gmail.com",
            phone="+79001234567",
            invite_token="test_token__invite_client_individual_entrepreneur_1",
        )

        self.client_user_company_2 = ClientCompany.objects.create(
            company=self.company_1,
            user=self.user_1,
            first_name="Ivan_2",
            second_name="Ivanov_2",
            third_name="Ivanov_2",
            email="ivan.petrov_2@gmail.com",
            phone="+79001234563",
            invite_token="test_token__invite_client_individual_entrepreneur_2",
        )

        self.base_guidebook_1 = GuideBook.objects.create(
            title="Внутренняя отделка",
            company=self.company_1,
            is_delete=False,
        )

        self.base_guidebook_2 = GuideBook.objects.create(
            title="Внешняя отделка",
            company=self.company_1,
            is_delete=False,
            parent_guide_book=self.base_guidebook_1,
        )

        self.base_work_1 = Work.objects.create(
            guidebook=self.base_guidebook_1,
            title="Покраска стен",
            price_by_unit=1000,
            unit_of_measurement=Work.UnitType.SQUARE_METER,
            currency=Work.CurrencyType.RUB,
            is_delete=False,
        )

        self.base_work_2 = Work.objects.create(
            guidebook=self.base_guidebook_1,
            title="Покраска потолков",
            price_by_unit=2000,
            unit_of_measurement=Work.UnitType.SQUARE_METER,
            currency=Work.CurrencyType.RUB,
            is_delete=False,
        )

        self.client_1.force_authenticate(user=self.user_1)  # авторизовываемся
        self.client_2.force_authenticate(user=self.user_2)  # авторизовываемся
        self.client_3.force_authenticate(user=self.user_3)  # авторизовываемся
