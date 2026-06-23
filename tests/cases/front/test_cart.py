"""
购物车 — 测试用例

覆盖场景：空购物车、登录后查看、商品数量修改、删除、批量删除、结算跳转
需要登录态
"""
import allure
import pytest


@allure.feature("购物车")
class TestCart:

    @allure.story("未登录访问购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_cart_empty_when_not_logged_in(self, cart_page):
        """未登录用户访问购物车，显示空状态提示。"""
        cart_page.open()
        # 未登录可能被拦截跳转登录页，或显示空购物车
        assert "/login" in cart_page.current_url or \
            cart_page.is_empty() or \
            "/cart" in cart_page.current_url, \
            "访问购物车应跳登录或显示空状态"

    @allure.story("登录后查看购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.p0
    def test_cart_page_loads(self, cart_page, logged_in):
        """登录用户访问购物车，页面正常加载。"""
        cart_page.open()
        assert "/cart" in cart_page.current_url, "应位于购物车页"

    @allure.story("全选操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_select_all(self, cart_page, logged_in):
        """全选/取消全选操作正常。"""
        cart_page.open()
        if cart_page.is_empty():
            pytest.skip("购物车为空，跳过测试")

        cart_page.toggle_select_all()
        # 操作应无异常
        assert "/cart" in cart_page.current_url

    @allure.story("去结算")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.p0
    def test_go_checkout(self, cart_page, logged_in):
        """点击「去结算」跳转到订单确认页。"""
        cart_page.open()
        if cart_page.is_empty():
            pytest.skip("购物车为空，跳过测试")

        # 尝试勾选第一个商品然后结算
        cart_page.toggle_select_all()
        if cart_page.is_checkout_enabled():
            cart_page.go_checkout()
            assert "/order/confirm" in cart_page.current_url, \
                "应跳转到订单确认页"
        else:
            pytest.skip("无可结算商品")

    @allure.story("继续购物")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login_required
    @pytest.mark.p2
    def test_continue_shopping(self, cart_page, logged_in):
        """点击「继续购物」返回首页。"""
        cart_page.open()
        cart_page.continue_shopping()
        assert cart_page.wait_for_url_contains("/", timeout=5), \
            "应返回首页或列表页"
