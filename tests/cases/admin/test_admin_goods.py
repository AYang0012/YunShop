"""
后台商品管理 — 测试用例

覆盖场景：商品列表加载、添加商品、编辑商品、搜索、删除、上下架
需要管理员登录
"""
import allure
import pytest

from data.test_data import new_goods_data


@allure.feature("后台商品管理")
class TestAdminGoods:

    @allure.story("商品列表加载")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_goods_list_loads(self, admin_goods_list_page, admin_logged_in):
        """商品管理页正常加载，显示商品列表。"""
        admin_goods_list_page.open()
        assert "/admin/goods" in admin_goods_list_page.current_url, \
            "应位于商品管理页"

    @allure.story("添加商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p0
    def test_add_goods(self, admin_goods_list_page, admin_goods_edit_page, admin_logged_in):
        """打开添加商品页面并填写表单。"""
        admin_goods_list_page.open()
        admin_goods_list_page.click_add()

        assert admin_goods_edit_page.is_edit_page(), "应跳转到商品编辑页"

        goods_data = new_goods_data()
        admin_goods_edit_page.fill_form(**goods_data)
        admin_goods_edit_page.save()

        # 保存后应返回列表页
        assert "/admin/goods" in admin_goods_edit_page.current_url, \
            "保存后应返回列表页"

    @allure.story("搜索商品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_search_goods(self, admin_goods_list_page, admin_logged_in):
        """在商品管理页搜索商品。"""
        admin_goods_list_page.open()
        admin_goods_list_page.search("测试")

        # 搜索后应仍在该页
        assert "/admin/goods" in admin_goods_list_page.current_url, \
            "搜索后应在商品管理页"

    @allure.story("编辑商品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_edit_goods(self, admin_goods_list_page, admin_logged_in):
        """点击编辑按钮打开编辑页。"""
        admin_goods_list_page.open()
        if admin_goods_list_page.get_goods_count() == 0:
            pytest.skip("无商品可编辑")

        admin_goods_list_page.click_edit(0)
        assert "/admin/goods/edit" in admin_goods_list_page.current_url, \
            "应跳转到编辑页"

    @allure.story("上下架切换")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_toggle_sale_status(self, admin_goods_list_page, admin_logged_in):
        """切换第一个商品的上下架状态。"""
        admin_goods_list_page.open()
        if admin_goods_list_page.get_goods_count() == 0:
            pytest.skip("无商品可操作")

        admin_goods_list_page.toggle_sale(0)
        # 操作后应在商品管理页
        assert "/admin/goods" in admin_goods_list_page.current_url, \
            "切换上下架后应仍在列表页"

    @allure.story("后台Dashboard")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_dashboard_loads(self, admin_index_page, admin_logged_in):
        """仪表盘页面正常加载。"""
        admin_index_page.open()
        assert "/admin" in admin_index_page.current_url, \
            "应位于后台管理首页"

    @allure.story("后台导航")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p1
    @pytest.mark.parametrize("nav_method,expected_url", [
        ("go_goods", "/admin/goods"),
        ("go_order", "/admin/order"),
        ("go_user", "/admin/user"),
    ])
    def test_admin_navigation(self, admin_index_page, admin_logged_in, nav_method, expected_url):
        """测试后台侧边栏导航。"""
        admin_index_page.open()
        getattr(admin_index_page, nav_method)()
        assert admin_index_page.wait_for_url_contains(expected_url, timeout=5), \
            f"应导航到 {expected_url}"

    @allure.story("退出登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.admin
    @pytest.mark.login_required
    @pytest.mark.p1
    def test_admin_logout(self, admin_index_page, admin_logged_in):
        """管理员退出登录。"""
        admin_index_page.open()
        admin_index_page.logout()

        # 退出后应跳转到登录页
        assert admin_index_page.wait_for_url_contains("/admin/login", timeout=5) or \
            "/login" in admin_index_page.current_url, \
            "退出后应跳转到登录页"
