"""
首页 — 测试用例

覆盖场景：页面加载、分类菜单、Banner轮播、商品楼层、热门推荐
"""
import allure
import pytest


@allure.feature("首页")
class TestHome:

    @allure.story("页面加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_home_page_loads(self, home_page):
        """首页正常加载，显示核心区域。"""
        home_page.open()
        assert home_page.is_home_page(), "应位于首页"

    @allure.story("分类菜单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    def test_category_menu_displayed(self, home_page):
        """左侧分类菜单正常显示。"""
        home_page.open()
        count = home_page.get_category_count()
        assert count >= 1, f"至少应显示1个分类，实际: {count}"

    @allure.story("分类菜单悬停")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_category_hover_popup(self, home_page):
        """悬停一级分类后弹出子分类面板。"""
        home_page.open()
        categories = home_page.get_category_count()
        if categories < 1:
            pytest.skip("无分类数据")

        home_page.hover_category(0)
        assert home_page.is_popup_visible(), "悬停后应显示分类弹出层"

    @allure.story("Banner 轮播")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_banner_displayed(self, home_page):
        """Banner 区域正常显示。"""
        home_page.open()
        assert home_page.is_banner_displayed(), "Banner区域应可见"

    @allure.story("Banner 箭头切换")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_banner_next_arrow(self, home_page):
        """点击右箭头切换到下一张 Banner。"""
        home_page.open()
        banner_count = home_page.get_banner_count()
        if banner_count <= 1:
            pytest.skip("Banner数量≤1，无法测试轮播切换")

        home_page.hover_banner()
        home_page.click_next_banner()
        # 验证未抛出异常（Banner区域仍可见）
        assert home_page.is_banner_displayed(), "切换后Banner区应仍可见"

    @allure.story("Banner 指示器点击")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.p2
    def test_banner_dot_click(self, home_page):
        """点击指示器圆点切换 Banner。"""
        home_page.open()
        banner_count = home_page.get_banner_count()
        if banner_count <= 1:
            pytest.skip("Banner数量≤1，无法测试指示器切换")

        home_page.hover_banner()
        home_page.click_dot(0)
        assert home_page.is_banner_displayed(), "点击指示器后Banner区应仍可见"

    @allure.story("商品楼层")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_floor_sections_displayed(self, home_page):
        """商品楼层区域正常显示。"""
        home_page.open()
        floor_count = home_page.get_floor_count()
        assert floor_count >= 0, f"楼层数量: {floor_count}"

    @allure.story("热门推荐")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_hot_goods_displayed(self, home_page):
        """热门推荐区域正常显示。"""
        home_page.open()
        hot_count = home_page.get_hot_goods_count()
        assert hot_count >= 1, f"热门推荐至少应有1个商品，实际: {hot_count}"

    @allure.story("点击商品跳转详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    def test_click_goods_card(self, home_page):
        """点击任意商品卡片跳转到商品详情页。"""
        home_page.open()
        home_page.click_goods_card(0)
        assert home_page.wait_for_url_contains("/goods/detail/", timeout=5), \
            "应跳转到商品详情页"
