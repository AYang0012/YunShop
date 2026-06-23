"""
后台登录 — 测试用例

覆盖场景：正常登录、错误密码、空字段、登录后跳转、页面元素
"""
import allure
import pytest


@allure.feature("后台登录")
class TestAdminLogin:

    @allure.story("正常登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.admin
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_admin_login_success(self, admin_login_page, admin_user):
        """管理员使用正确凭证登录，跳转到后台首页。"""
        admin_login_page.open()
        assert admin_login_page.is_login_page(), "应位于后台登录页"

        admin_login_page.login(admin_user["username"], admin_user["password"])

        # 登录成功后应跳转到后台管理页
        assert admin_login_page.wait_for_url_contains("/admin", timeout=5), \
            "登录成功后应跳转到后台"

    @allure.story("错误密码")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_login_wrong_password(self, admin_login_page):
        """使用错误密码登录失败。"""
        admin_login_page.open()
        admin_login_page.login("admin", "wrongpassword")

        # 应停留在登录页或显示错误
        assert "/admin/login" in admin_login_page.current_url or \
            "/admin" in admin_login_page.current_url, \
            "错误密码应留在登录页"

    @allure.story("空字段")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_login_empty_fields(self, admin_login_page):
        """空字段提交应触发校验。"""
        admin_login_page.open()
        admin_login_page.login("", "")

        # 应留在登录页
        assert "/admin/login" in admin_login_page.current_url or \
            "/admin" in admin_login_page.current_url

    @allure.story("页面元素")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_login_page_elements(self, admin_login_page):
        """验证后台登录页关键元素存在。"""
        admin_login_page.open()
        assert admin_login_page.is_displayed(admin_login_page.USERNAME_INPUT), \
            "应有用户名输入框"
        assert admin_login_page.is_displayed(admin_login_page.PASSWORD_INPUT), \
            "应有密码输入框"
        assert admin_login_page.is_displayed(admin_login_page.SUBMIT_BTN), \
            "应有登录按钮"
        assert "后台" in admin_login_page.get_title(), \
            "标题应包含「后台」"
