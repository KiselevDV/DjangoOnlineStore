from decimal import Decimal
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Notebook, CartProduct, Cart, Customer
from .utils import recalc_cart
from .views import AddToCartView, BaseView

User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        """
        Объект болванка, для тестирования: создания нового
        продукта, пользователя, корзины и продукта_для_корзины
        """
        self.user = User.objects.create(
            username='TestUser', password='password')
        self.category = Category.objects.create(
            name='Ноутбуки', slug='notebooks')
        # image = SimpleUploadedFile(
        #     'honor_magic_book.jpg', content=b'', content_type='image/jpg')
        self.notebook = Notebook.objects.create(
            category=self.category, title='HONOR MagicBook 15 2021',
            slug='honor_magic_book_15_2021', price=Decimal('2166.00'),
            diagonal='15.6"', display_type='IPS', processor_freq='2 300 МГц',
            ram='16 ГБ', video='встроенная',
            time_without_charge='6 часов 18 минут'
        )
        self.customer = Customer.objects.create(
            user=self.user, phone='+7 495 123-45-67',
            address='st. Lva Tolstogo 16'
        )
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer, cart=self.cart, content_object=self.notebook)

    def test_add_to_cart(self):
        """Сами тесты - ф-ии с префиксом 'test_' """
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)

        # Тест 1: Вхождение чего-то, в каком-то контейнере (массиве)
        self.assertIn(self.cart_product, self.cart.products.all())
        # Тест 2: Количество вхождений объекта в массив
        self.assertEqual(self.cart.products.count(), 1)
        # Тест 3: Проверка корректности ф-ии пересчёта 'recalc_cart'
        self.assertEqual(self.cart.final_price, Decimal('2166.00'))

    def test_response_from_add_to_cart_view(self):
        # client = Client()
        # response = client.get(
        # '/add-to-card/notebook/honor_magic_book_15_2021/')
        # self.assertEqual(response.status_code, 200)

        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = AddToCartView.as_view()(
            request, ct_model='notebook', slug='honor_magic_book_15_2021')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)
            print(mock_data_.called)
