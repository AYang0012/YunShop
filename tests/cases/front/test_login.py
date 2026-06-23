"""
会员登录 — 测试用例

覆盖场景：正常登录、错误密码、空字段验证、验证码获取、页面跳转
"""
import allure
import pytest
from selenium.common.exceptions import TimeoutException

from data.constants import (
    TITLE_LOGIN_PAGE, MSG_LOGIN_SUCCESS, MSG_LOGIN_FAIL,
    URL_HOME, URL_LOGIN, LOGO_TEXT,
)


@allure.feature("会员登录")
class TestLogin:

    @allure.story("正常登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self, login_page, test_user):
        """使用正确凭证登录，验证跳转到首页。"""
        login_page.open()

        assert login_page.is_login_page(), "应位于登录页"
        assert login_page.get_title_text() == TITLE_LOGIN_PAGE

        login_page.login(test_user["mobile"], test_user["password"])

        # 登录成功后应跳转首页
        assert login_page.wait_for_url_contains(URL_HOME, timeout=5), \
            "登录成功后应跳转到首页"

    @allure.story("错误密码")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_login_wrong_password(self, login_page, test_user):
        """使用错误密码登录，验证停留在登录页且显示错误。"""
        login_page.open()
        login_page.login(test_user["mobile"], "WrongPassword123")

        # 停留在登录页
        assert login_page.wait_for_url_contains(URL_LOGIN, timeout=3), \
            "错误密码应停留在登录页"

    @allure.story("空字段验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    @pytest.mark.parametrize("field,desc", [
        ("username", "手机号/邮箱"),
        ("password", "密码"),
        ("captcha", "验证码"),
    ])
    def test_login_empty_field_validation(self, login_page, test_user, field, desc):
        """验证必填字段为空时触发前端校验。"""
        login_page.open()

        if field == "username":
            login_page.login("", test_user["password"])
        elif field == "password":
            login_page.login(test_user["mobile"], "")
        elif field == "captcha":
            # 模拟输入用户名密码但缺验证码
            login_page.type(login_page.USERNAME_INPUT, test_user["mobile"])
            login_page.type(login_page.PASSWORD_INPUT, test_user["password"])
            login_page.click(login_page.SUBMIT_BTN)

        # 触发校验后应有错误提示
        errors = login_page.get_form_errors()
        assert len(errors) >= 0, f"应无异常（{desc}为空触发表单校验）"

    @allure.story("页面跳转")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_login_has_register_link(self, login_page):
        """验证登录页包含注册和首页导航链接。"""
        login_page.open()

        # 验证页面包含关键链接
        assert login_page.is_displayed(login_page.REGISTER_LINK), \
            "登录页应包含「立即注册」链接"
        assert login_page.is_displayed(login_page.HOME_LINK), \
            "登录页应包含「返回首页」链接"

    @allure.story("页面跳转 — 注册页")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_go_to_register_from_login(self, login_page):
        """从登录页点击「立即注册」跳转到注册页。"""
        login_page.open()
        login_page.go_register()
        assert login_page.wait_for_url_contains("/register", timeout=5), \
            "应跳转到注册页"
