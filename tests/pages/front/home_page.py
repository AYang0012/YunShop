"""
首页 Page Object

URL: /
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class HomePage(BasePage):
    URL = BASE_URL + "/"

    # ── 分类菜单 ──
    CATEGORY_MENU   = (By.CSS_SELECTOR, ".category-menu")
    CAT_ITEMS       = (By.CSS_SELECTOR, ".cat-item")
    CAT_NAMES       = (By.CSS_SELECTOR, ".cat-name")
    CAT_POPUP       = (By.CSS_SELECTOR, ".category-popup")
    POPUP_TITLES    = (By.CSS_SELECTOR, ".popup-title")
    POPUP_TAGS      = (By.CSS_SELECTOR, ".popup-tag")

    # ── Banner 轮播 ──
    BANNER_AREA     = (By.CSS_SELECTOR, ".banner")
    CAROUSEL_TRACK  = (By.CSS_SELECTOR, ".carousel-track")
    CAROUSEL_SLIDES = (By.CSS_SELECTOR, ".carousel-slide")
    BANNER_IMG      = (By.CSS_SELECTOR, ".banner-img")
    ARROW_LEFT      = (By.CSS_SELECTOR, ".carousel-arrow.left")
    ARROW_RIGHT     = (By.CSS_SELECTOR, ".carousel-arrow.right")
    CAROUSEL_DOTS   = (By.CSS_SELECTOR, ".carousel-dot")
    DOT_ACTIVE      = (By.CSS_SELECTOR, ".carousel-dot.active")

    # ── 商品楼层 ──
    FLOORS          = (By.CSS_SELECTOR, ".floor")
    FLOOR_TITLES    = (By.CSS_SELECTOR, ".floor-title")
    FLOOR_GOODS     = (By.CSS_SELECTOR, ".floor-goods .goods-card")
    FLOOR_SUBS      = (By.CSS_SELECTOR, ".floor-sub")
    FLOOR_MORE      = (By.CSS_SELECTOR, ".floor-more")

    # ── 热门推荐 ──
    HOT_SECTION     = (By.CSS_SELECTOR, ".hot-section")
    HOT_GRID        = (By.CSS_SELECTOR, ".hot-grid .goods-card")
    SECTION_TITLE   = (By.CSS_SELECTOR, ".section-title")

    # ── 商品卡片通用 ──
    GOODS_CARD      = (By.CSS_SELECTOR, ".goods-card")
    GOODS_NAME      = (By.CSS_SELECTOR, ".goods-name")
    PRICE_CURRENT   = (By.CSS_SELECTOR, ".price-current")

    # ── 底部 ──
    FOOTER          = (By.CSS_SELECTOR, ".footer")

    @allure.step("打开首页")
    def open(self) -> None:
        super().open(self.URL)

    # ======================== 分类菜单 ========================

    def get_category_count(self) -> int:
        return self.element_count(self.CAT_ITEMS)

    def get_category_names(self) -> list:
        return [el.text for el in self.find_all(self.CAT_NAMES)]

    def hover_category(self, index: int = 0) -> None:
        """
        悬停第 index 个分类，弹出子分类面板。

        Args:
            index: 分类索引（0-based）
        """
        items = self.find_all(self.CAT_ITEMS)
        self._scroll_to(items[index])
        self.hover((By.CSS_SELECTOR, f".cat-item:nth-child({index + 1})"))
        self._pause(0.3)  # 等待过渡动画

    def is_popup_visible(self) -> bool:
        return self.is_displayed(self.CAT_POPUP)

    def get_popup_titles(self) -> list:
        return [el.text for el in self.find_all(self.POPUP_TITLES)]

    def click_category(self, index: int = 0) -> None:
        """点击分类菜单项，跳转到商品列表页。"""
        self.click((By.CSS_SELECTOR, f".cat-item:nth-child({index + 1})"))

    # ======================== Banner ========================

    def get_banner_count(self) -> int:
        return self.element_count(self.CAROUSEL_SLIDES)

    def is_banner_displayed(self) -> bool:
        return self.is_displayed(self.BANNER_AREA)

    def click_next_banner(self) -> None:
        self.hover(self.BANNER_AREA)
        self.click(self.ARROW_RIGHT)

    def click_prev_banner(self) -> None:
        self.hover(self.BANNER_AREA)
        self.click(self.ARROW_LEFT)

    def click_dot(self, index: int) -> None:
        dots = self.find_all(self.CAROUSEL_DOTS)
        if index < len(dots):
            dots[index].click()

    def hover_banner(self) -> None:
        """悬停 banner（暂停自动播放）。"""
        self.hover(self.BANNER_AREA)

    # ======================== 楼层 ========================

    def get_floor_count(self) -> int:
        return self.element_count(self.FLOORS)

    def get_floor_titles(self) -> list:
        return [el.text for el in self.find_all(self.FLOOR_TITLES)]

    def get_floor_goods_count(self, floor_index: int = 0) -> int:
        floors = self.find_all(self.FLOORS)
        if floor_index < len(floors):
            return len(floors[floor_index].find_elements(By.CSS_SELECTOR, ".goods-card"))
        return 0

    def click_floor_goods(self, floor_index: int = 0, goods_index: int = 0) -> None:
        """点击某个楼层中的商品卡片。"""
        floors = self.find_all(self.FLOORS)
        goods = floors[floor_index].find_elements(By.CSS_SELECTOR, ".goods-card")
        if goods_index < len(goods):
            goods[goods_index].click()

    # ======================== 热门推荐 ========================

    def get_hot_goods_count(self) -> int:
        return self.element_count(self.HOT_GRID)

    def is_hot_section_displayed(self) -> bool:
        return self.is_displayed(self.HOT_SECTION)

    def click_hot_goods(self, index: int = 0) -> None:
        items = self.find_all(self.HOT_GRID)
        if index < len(items):
            items[index].click()

    # ======================== 通用 ========================

    def click_goods_card(self, index: int = 0) -> None:
        cards = self.find_all(self.GOODS_CARD)
        if index < len(cards):
            cards[index].click()

    def is_home_page(self) -> bool:
        """判断当前页面是否为首页。"""
        return self.current_url.rstrip("/") in (self.URL.rstrip("/"), self.URL)
