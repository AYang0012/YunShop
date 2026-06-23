"""
用户中心 — 测试用例

覆盖场景：个人中心导航、收货地址管理、密码修改、个人信息编辑
需要登录态
"""
import allure
import pytest

from data.test_data import new_address_data, new_mobile


@allure.feature("用户中心")
class TestUserCenter:

    @allure.story("用户中心导航")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_user_center_loads(self, user_center_page, logged_in):
        """登录后用户中心页正常加载。"""
        user_center_page.open()
        assert user_center_page.is_user_center(), "应位于用户中心"

    @allure.story("收货地址 — 列表")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_address_page_loads(self, user_address_page, logged_in):
        """收货地址页正常加载。"""
        user_address_page.open()
        assert "/user/address" in user_address_page.current_url, \
            "应位于收货地址页"

    @allure.story("收货地址 — 新增")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.p0
    def test_add_address(self, user_address_page, logged_in):
        """新增收货地址成功。"""
        user_address_page.open()
        data = new_address_data()
        user_address_page.add_address(**data)

        # 新增后应在地址页
        assert "/user/address" in user_address_page.current_url, \
            "新增地址后应返回地址列表"

    @allure.story("收货地址 — 删除")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_delete_address(self, user_address_page, logged_in):
        """删除一个收货地址。"""
        user_address_page.open()
        if user_address_page.is_empty():
            # 先新增一个再删除
            data = new_address_data()
            user_address_page.add_address(**data)
            user_address_page.open()

        user_address_page.delete_address(0)
        assert "/user/address" in user_address_page.current_url, \
            "删除后应在地址列表页"

    @allure.story("修改密码 — 页面加载")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_password_page_loads(self, user_password_page, logged_in):
        """修改密码页正常加载。"""
        user_password_page.open()
        assert "/user/password" in user_password_page.current_url, \
            "应位于修改密码页"

    @allure.story("个人信息 — 页面加载")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_profile_page_loads(self, user_profile_page, logged_in):
        """个人信息页正常加载。"""
        user_profile_page.open()
        assert "/user/profile" in user_profile_page.current_url, \
            "应位于个人信息页"

    @allure.story("个人信息 — 编辑昵称")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_update_nickname(self, user_profile_page, logged_in):
        """修改昵称成功。"""
        user_profile_page.open()
        user_profile_page.update_nickname("测试用户_自动化")
        # 更新后应在同一页或显示成功提示
        assert "/user/profile" in user_profile_page.current_url, \
            "修改昵称后应仍在个人信息页"

    @allure.story("用户中心 — 导航到订单")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login_required
    @pytest.mark.p2
    def test_navigate_to_orders(self, user_center_page, logged_in):
        """从用户中心导航到我的订单。"""
        user_center_page.open()
        user_center_page.go_orders()
        assert user_center_page.wait_for_url_contains("/user/orders", timeout=5), \
            "应导航到我的订单"

    @allure.story("用户中心 — 导航到地址")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login_required
    @pytest.mark.p2
    def test_navigate_to_address(self, user_center_page, logged_in):
        """从用户中心导航到收货地址。"""
        user_center_page.open()
        user_center_page.go_address()
        assert user_center_page.wait_for_url_contains("/user/address", timeout=5), \
            "应导航到收货地址"
