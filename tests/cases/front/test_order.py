"""
订单流程 — 测试用例

覆盖场景：订单页面访问、订单状态查看、订单支付、订单取消、确认收货
需要登录态
"""
import allure
import pytest


@allure.feature("订单流程")
class TestOrder:

    @allure.story("我的订单页加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_orders_page_loads(self, user_orders_page, logged_in):
        """登录后「我的订单」页正常加载。"""
        user_orders_page.open()
        assert "/user/orders" in user_orders_page.current_url, \
            "应位于我的订单页"

    @allure.story("订单状态筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    @pytest.mark.parametrize("status,tab_name", [
        ("all", "全部"),
        ("PENDING", "待付款"),
        ("PAID", "待发货"),
        ("SHIPPED", "待收货"),
        ("COMPLETED", "已完成"),
        ("CANCELLED", "已取消"),
    ])
    def test_filter_by_status(self, user_orders_page, logged_in, status, tab_name):
        """切换订单状态 Tab，无异常。"""
        user_orders_page.open()
        user_orders_page.filter_by_status(status)
        # 切换后页面应仍在订单页
        assert "/user/orders" in user_orders_page.current_url, \
            f"筛选 {tab_name} 后应仍在订单页"

    @allure.story("支付订单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login_required
    @pytest.mark.p0
    def test_pay_order(self, user_orders_page, logged_in):
        """对第一个待付款订单执行支付操作。"""
        user_orders_page.open()
        user_orders_page.filter_by_status("PENDING")

        if user_orders_page.is_empty():
            pytest.skip("无待付款订单")

        user_orders_page.pay_order(0)
        assert "/user/orders" in user_orders_page.current_url, \
            "支付后应仍在订单页"

    @allure.story("取消订单")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_cancel_order(self, user_orders_page, logged_in):
        """取消第一个待付款订单。"""
        user_orders_page.open()
        user_orders_page.filter_by_status("PENDING")

        if user_orders_page.is_empty():
            pytest.skip("无待付款订单可取消")

        user_orders_page.cancel_order(0)
        assert "/user/orders" in user_orders_page.current_url, \
            "取消后应仍在订单页"

    @allure.story("确认收货")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_confirm_receive(self, user_orders_page, logged_in):
        """对第一个已发货订单执行确认收货。"""
        user_orders_page.open()
        user_orders_page.filter_by_status("SHIPPED")

        if user_orders_page.is_empty():
            pytest.skip("无已发货订单")

        user_orders_page.confirm_receive(0)
        assert "/user/orders" in user_orders_page.current_url, \
            "确认收货后应仍在订单页"

    @allure.story("订单确认页跳转")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_order_confirm_page(self, order_confirm_page, logged_in):
        """订单确认页访问（登录后）。"""
        order_confirm_page.open()
        # 可能因为购物车无选中商品而停留在确认页或跳转
        assert "/order/confirm" in order_confirm_page.current_url or \
            "/cart" in order_confirm_page.current_url, \
            "应位于订单确认页或跳回购物车"
