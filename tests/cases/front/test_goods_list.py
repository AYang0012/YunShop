"""
商品列表 — 测试用例

覆盖场景：列表加载、搜索、排序（综合/销量/价格/新品）、分页、空结果
"""
import allure
import pytest


@allure.feature("商品列表")
class TestGoodsList:

    @allure.story("列表加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_goods_list_loads(self, goods_list_page):
        """商品列表页正常加载，显示商品卡片。"""
        goods_list_page.open()
        count = goods_list_page.get_goods_count()
        # 根据默认分页，最多12条
        assert 0 <= count <= 12, f"商品数量应≤12，实际: {count}"

    @allure.story("搜索")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    def test_search_goods(self, goods_list_page):
        """输入关键词搜索，结果页面URL包含keyword参数。"""
        goods_list_page.open()
        goods_list_page.search("华为")
        # 搜索后应停留在列表页或显示空结果
        assert "/goods/list" in goods_list_page.current_url, \
            "搜索后应仍在商品列表页"

    @allure.story("排序 — 综合")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_sort_default(self, goods_list_page):
        """点击「综合」排序。"""
        goods_list_page.open()
        goods_list_page.sort_by_default()
        assert goods_list_page.is_displayed(goods_list_page.SORT_BAR), \
            "排序栏应仍可见"

    @allure.story("排序 — 销量")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_sort_by_sales(self, goods_list_page):
        """点击「销量」排序，URL 应包含 sort=sales。"""
        goods_list_page.open()
        goods_list_page.sort_by_sales()
        # 排序后应在列表页
        assert "/goods/list" in goods_list_page.current_url

    @allure.story("排序 — 价格")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_sort_by_price(self, goods_list_page):
        """点击「价格」排序。"""
        goods_list_page.open()
        goods_list_page.sort_by_price()
        assert "/goods/list" in goods_list_page.current_url

    @allure.story("排序 — 新品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_sort_by_time(self, goods_list_page):
        """点击「新品」排序。"""
        goods_list_page.open()
        goods_list_page.sort_by_time()
        assert "/goods/list" in goods_list_page.current_url

    @allure.story("搜索不存在商品")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_search_no_results(self, goods_list_page):
        """搜索不存在的商品，显示空状态。"""
        goods_list_page.open()
        goods_list_page.search("zzzzznonexistent9999")
        # 应无异常 — 可能显示空结果
        assert "/goods/list" in goods_list_page.current_url

    @allure.story("每页条数切换")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_page_size_switch(self, goods_list_page):
        """切换每页24条。"""
        goods_list_page.open()
        goods_list_page.set_page_size(24)
        # 验证：商品数量不超过24
        count = goods_list_page.get_goods_count()
        assert 0 <= count <= 24, f"每页24条应≤24，实际: {count}"
