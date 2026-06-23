"""
用例层 fixtures — 页面对象实例化

每个 fixture 接收 driver fixture，返回对应的 Page Object 实例。
测试用例中直接使用: def test_xxx(login_page): ...
"""

import pytest

from pages.front.home_page import HomePage
from pages.front.login_page import LoginPage
from pages.front.register_page import RegisterPage
from pages.front.goods_list_page import GoodsListPage
from pages.front.goods_detail_page import GoodsDetailPage
from pages.front.cart_page import CartPage
from pages.front.order_confirm_page import OrderConfirmPage
from pages.front.user_center_page import UserCenterPage
from pages.front.user_orders_page import UserOrdersPage
from pages.front.user_address_page import UserAddressPage
from pages.front.user_profile_page import UserProfilePage
from pages.front.user_password_page import UserPasswordPage

from pages.admin.admin_login_page import AdminLoginPage
from pages.admin.admin_index_page import AdminIndexPage
from pages.admin.admin_goods_list_page import AdminGoodsListPage
from pages.admin.admin_goods_edit_page import AdminGoodsEditPage
from pages.admin.admin_category_page import AdminCategoryPage
from pages.admin.admin_order_page import AdminOrderPage
from pages.admin.admin_user_page import AdminUserPage


# ================================================================
# 前台 Page Object fixtures
# ================================================================

@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def register_page(driver):
    return RegisterPage(driver)


@pytest.fixture
def goods_list_page(driver):
    return GoodsListPage(driver)


@pytest.fixture
def goods_detail_page(driver):
    return GoodsDetailPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def order_confirm_page(driver):
    return OrderConfirmPage(driver)


@pytest.fixture
def user_center_page(driver):
    return UserCenterPage(driver)


@pytest.fixture
def user_orders_page(driver):
    return UserOrdersPage(driver)


@pytest.fixture
def user_address_page(driver):
    return UserAddressPage(driver)


@pytest.fixture
def user_profile_page(driver):
    return UserProfilePage(driver)


@pytest.fixture
def user_password_page(driver):
    return UserPasswordPage(driver)


# ================================================================
# 后台 Page Object fixtures
# ================================================================

@pytest.fixture
def admin_login_page(driver):
    return AdminLoginPage(driver)


@pytest.fixture
def admin_index_page(driver):
    return AdminIndexPage(driver)


@pytest.fixture
def admin_goods_list_page(driver):
    return AdminGoodsListPage(driver)


@pytest.fixture
def admin_goods_edit_page(driver):
    return AdminGoodsEditPage(driver)


@pytest.fixture
def admin_category_page(driver):
    return AdminCategoryPage(driver)


@pytest.fixture
def admin_order_page(driver):
    return AdminOrderPage(driver)


@pytest.fixture
def admin_user_page(driver):
    return AdminUserPage(driver)


# ================================================================
# 复合 fixtures（登录状态）
# ================================================================

@pytest.fixture
def logged_in(driver, login_page, test_user):
    """
    前台已登录状态 fixture。

    用法:
        def test_cart(cart_page, logged_in):
            cart_page.open()
            ...
    """
    login_page.open()
    login_page.login(test_user["mobile"], test_user["password"])
    return test_user


@pytest.fixture
def admin_logged_in(driver, admin_login_page, admin_user):
    """
    后台已登录状态 fixture。

    用法:
        def test_admin_goods(admin_goods_list_page, admin_logged_in):
            admin_goods_list_page.open()
            ...
    """
    admin_login_page.open()
    admin_login_page.login(admin_user["username"], admin_user["password"])
    return admin_user
