from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class HomePage:
    """Insider ana sayfası için Page Object Model."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)

        # Cookie ve Pop-up Seçicileri
        self.cookie_accept_button = (By.ID, "wt-cli-accept-all-btn")
        self.push_notification_close = (By.CLASS_NAME, "close")

        # Navbar'daki Company Menüsü ve Careers Linki
        self.company_menu = (By.XPATH, "//li[contains(@class, 'nav-item dropdown')][6]")  # 6. öğe
        self.careers_link = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")

    def open_homepage(self):
        """Ana sayfayı açar ve yüklenmesini bekler."""
        print("TEST ADIMI: Ana sayfa açılıyor...")
        self.driver.get("https://useinsider.com/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Sayfanın yüklendiğini doğrula
        assert "Insider" in self.driver.title, "Ana sayfa yüklenemedi!"
        print("✓ Ana sayfa başarıyla yüklendi")

    def accept_cookies(self):
        """Çerezleri kabul eder."""
        print("TEST ADIMI: Çerez bildirimi kabul ediliyor...")
        try:
            accept_button = self.wait.until(EC.element_to_be_clickable(self.cookie_accept_button))
            accept_button.click()
            self.wait.until(EC.invisibility_of_element_located(self.cookie_accept_button))
            print("✓ Çerez bildirimi başarıyla kabul edildi")
        except Exception:
            print("ℹ️ Çerez bildirimi görünmüyor veya zaten kabul edilmiş")

    def close_push_notification(self):
        """Eğer push bildirimi çıkarsa, kapatır."""
        try:
            push_close_button = self.wait.until(EC.element_to_be_clickable(self.push_notification_close))
            push_close_button.click()
            print("✓ Push bildirimi başarıyla kapatıldı")
        except Exception:
            # Bu bir hata değil, bildirim olmayabilir
            pass

    def navigate_to_careers(self):
        """Navbar'daki 'Company' menüsüne hover yapar ve 'Careers' seçeneğini tıklar."""
        print("TEST ADIMI: Careers sayfasına yönlendiriliyor...")
        self.close_push_notification()

        # "Company" menüsüne hover yap
        company_menu = self.wait.until(EC.presence_of_element_located(self.company_menu))
        self.actions.move_to_element(company_menu).perform()
        print("✓ Company menüsüne hover yapıldı")

        # Menünün açıldığından emin ol
        self.wait.until(EC.visibility_of_element_located(self.careers_link))
        assert self.driver.find_element(*self.careers_link).is_displayed(), "Careers linki görünür değil!"

        # "Careers" linkini tıkla
        careers_link = self.wait.until(EC.element_to_be_clickable(self.careers_link))
        careers_link.click()
        print("✓ Careers linkine tıklandı")

        # Yeni sekmeye geç
        self.driver.switch_to.window(self.driver.window_handles[-1])
        print("✓ Careers sayfasına başarıyla yönlendirildi")
