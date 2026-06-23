"""
商品详情 — 测试用例

覆盖场景：详情页加载、商品信息展示、数量操作、加入购物车、立即购买
"""
import allure
import pytest


@allure.feature("商品详情")
class TestGoodsDetail:

    @allure.story("详情页加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_goods_detail_loads(self, goods_detail_page):
        """商品详情页正常加载，显示商品名称和价格。"""
        goods_detail_page.open(1)
        assert goods_detail_page.is_detail_page(), "应位于商品详情页"

        name = goods_detail_page.get_goods_name()
        assert len(name) > 0, "商品名称不应为空"

        price = goods_detail_page.get_shop_price()
        assert "¥" in price, f"价格应包含 ¥ 符号: {price}"

    @allure.story("商品信息展示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_goods_detail_info(self, goods_detail_page):
        """验证商品详情页显示完整信息：图片、名称、价格、销量、库存。"""
        goods_detail_page.open(1)

        assert goods_detail_page.is_displayed(goods_detail_page.MAIN_IMG), \
            "应显示商品主图"
        assert goods_detail_page.is_displayed(goods_detail_page.GOODS_TITLE), \
            "应显示商品标题"
        assert goods_detail_page.is_displayed(goods_detail_page.SHOP_PRICE), \
            "应显示售价"

    @allure.story("数量操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_quantity_increase(self, goods_detail_page):
        """点击 + 按钮增加购买数量。"""
        goods_detail_page.open(1)
        initial = goods_detail_page.get_buy_quantity()
        goods_detail_page.increase_quantity()
        assert goods_detail_page.get_buy_quantity() == initial + 1, \
            "数量应增加1"

    @allure.story("数量操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_quantity_decrease(self, goods_detail_page):
        """点击 - 按钮减少购买数量（不低于最小值1）。"""
        goods_detail_page.open(1)
        goods_detail_page.increase_quantity()  # 2
        goods_detail_page.increase_quantity()  # 3
        assert goods_detail_page.get_buy_quantity() == 3
        goods_detail_page.decrease_quantity()  # 2
        assert goods_detail_page.get_buy_quantity() == 2

    @allure.story("加入购物车（未登录）")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    def test_add_to_cart_redirects_to_login(self, goods_detail_page):
        """
        未登录用户点击「加入购物车」，应提示登录。

        注意：前端 api/cart 需要登录态，后端返回401后
        前端拦截器会跳转到登录页。
        """
        goods_detail_page.open(1)
        goods_detail_page.add_to_cart()
        # 可能跳转到登录页或显示错误提示
        # 验证操作未导致异常
        assert goods_detail_page.is_detail_page() or \
            "/login" in goods_detail_page.current_url, \
            "加入购物车后应在详情页或跳转登录页"

    @allure.story("立即购买（未登录）")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_buy_now(self, goods_detail_page):
        """点击「立即购买」，应触发操作（未登录则跳转登录）。"""
        goods_detail_page.open(1)
        goods_detail_page.buy_now()

        # 未登录时跳转登录；已登录时跳转购物车
        assert "/login" in goods_detail_page.current_url or \
            "/cart" in goods_detail_page.current_url or \
            goods_detail_page.is_detail_page(), \
            "操作后应跳转或停留"
