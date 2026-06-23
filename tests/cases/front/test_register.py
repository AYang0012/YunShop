"""
会员注册 — 测试用例

覆盖场景：手机号注册、邮箱注册、密码复杂度校验、协议勾选、跳转
"""
import allure
import pytest

from data.constants import TITLE_REGISTER_PAGE, URL_REGISTER, URL_HOME
from data.test_data import new_mobile, new_email, valid_password, weak_password


@allure.feature("会员注册")
class TestRegister:

    @allure.story("手机号注册")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_register_by_mobile(self, register_page):
        """使用新手机号注册，注册成功后跳转到首页。"""
        register_page.open()
        assert register_page.is_register_page()
        assert register_page.get_title_text() == TITLE_REGISTER_PAGE

        register_page.register(
            account=new_mobile(),
            password=valid_password(),
            register_type="mobile",
            agree_protocol=True,
        )

        # 注册成功 → 跳转首页
        assert register_page.wait_for_url_contains(URL_HOME, timeout=5), \
            "注册成功后应跳转到首页"

    @allure.story("邮箱注册")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    def test_register_by_email(self, register_page):
        """使用新邮箱注册，切换邮箱标签后注册成功。"""
        register_page.open()
        register_page.switch_to_email()

        register_page.register(
            account=new_email(),
            password=valid_password(),
            register_type="email",
            agree_protocol=True,
        )

        # 注册成功 → 跳转首页
        assert register_page.wait_for_url_contains(URL_HOME, timeout=5), \
            "注册成功后应跳转到首页"

    @allure.story("密码复杂度校验")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_register_password_too_short(self, register_page):
        """密码长度不足6位时应触发前端校验。"""
        register_page.open()
        register_page.register(
            account=new_mobile(),
            password="Abc1",
            agree_protocol=True,
        )

        # 应停留在注册页（前端校验阻止提交）
        errors = register_page.get_form_errors()
        assert any("6" in e for e in errors) or register_page.wait_for_url_contains(
            URL_REGISTER, timeout=3
        ), "密码不足6位应阻止注册"

    @allure.story("确认密码不一致")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_register_password_mismatch(self, register_page):
        """两次密码输入不一致时应触发校验。"""
        register_page.open()
        register_page.register(
            account=new_mobile(),
            password=valid_password(),
            confirm_password="Mismatch@999",
            agree_protocol=True,
        )

        errors = register_page.get_form_errors()
        assert any("不一致" in e for e in errors) or register_page.wait_for_url_contains(
            URL_REGISTER, timeout=3
        ), "两次密码不一致应阻止注册"

    @allure.story("协议未勾选")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_register_without_protocol(self, register_page):
        """未勾选协议时应触发校验。"""
        register_page.open()
        register_page.register(
            account=new_mobile(),
            password=valid_password(),
            agree_protocol=False,
        )

        errors = register_page.get_form_errors()
        assert any("协议" in e for e in errors) or register_page.wait_for_url_contains(
            URL_REGISTER, timeout=3
        ), "未勾选协议应阻止注册"

    @allure.story("页面跳转")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_go_to_login_from_register(self, register_page):
        """从注册页点击「已有账号？立即登录」跳转到登录页。"""
        register_page.open()
        register_page.go_login()
        assert register_page.wait_for_url_contains("/login", timeout=5), \
            "应跳转到登录页"
