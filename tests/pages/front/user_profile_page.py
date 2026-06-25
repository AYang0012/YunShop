"""
个人信息页 Page Object

URL: /user/profile
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class UserProfilePage(BasePage):
    URL = f"{BASE_URL}/user/profile"

    # ── 信息展示/编辑 ──
    NICKNAME_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='昵称']")
    MOBILE_INPUT    = (By.CSS_SELECTOR, "input[placeholder*='手机']")
    EMAIL_INPUT     = (By.CSS_SELECTOR, "input[placeholder*='邮箱']")
    AVATAR_UPLOAD   = (By.CSS_SELECTOR, ".el-upload, .avatar-uploader")
    AVATAR_IMG      = (By.CSS_SELECTOR, ".avatar img, .el-avatar img")

    # ── 保存 ──
    SAVE_BTN        = (By.XPATH, "//button[contains(.,'保存') or contains(.,'更新')]")

    @allure.step("打开个人信息")
    def open(self) -> None:
        super().open(self.URL)

    def get_nickname(self) -> str:
        return self.get_value(self.NICKNAME_INPUT)

    def get_mobile(self) -> str:
        return self.get_value(self.MOBILE_INPUT)

    @allure.step("修改昵称: {nickname}")
    def update_nickname(self, nickname: str) -> None:
        self.type(self.NICKNAME_INPUT, nickname)
        self.click(self.SAVE_BTN)

    @allure.step("修改邮箱: {email}")
    def update_email(self, email: str) -> None:
        self.type(self.EMAIL_INPUT, email)
        self.click(self.SAVE_BTN)

    @allure.step("上传头像: {file_path}")
    def upload_avatar(self, file_path: str) -> None:
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(file_path)
