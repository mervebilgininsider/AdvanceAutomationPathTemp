from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # time modülünü import ediyoruz

class CareersPage:
    """Insider Kariyer Sayfası için Page Object Model."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Sayfadaki Bölümlerin Locator'ları
        self.locations_section = (By.ID, "career-our-location")
        self.teams_section = (By.XPATH, "//section[@data-id='a8e7b90']")
        self.life_at_insider_section = (By.ID, "find-job-widget")


    def verify_sections(self):
        """Belirtilen bölümlere scroll yapar ve görünürlüğünü doğrular."""
        print("TEST ADIMI: Careers sayfasındaki bölümler kontrol ediliyor...")
        
        # Locations section'a scroll yap ve verify et
        locations_element = self.wait.until(EC.presence_of_element_located(self.locations_section))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", locations_element)
        assert locations_element.is_displayed(), "Locations bölümü görüntülenemiyor!"
        time.sleep(2)  # Görsel doğrulama için bekleme
        print("✓ Locations bölümü başarıyla görüntülendi")
        
        # Teams section'a scroll yap ve verify et
        teams_element = self.wait.until(EC.presence_of_element_located(self.teams_section))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", teams_element)
        assert teams_element.is_displayed(), "Teams bölümü görüntülenemiyor!"
        time.sleep(2)  # Görsel doğrulama için bekleme
        print("✓ Teams bölümü başarıyla görüntülendi")
        
        # Life at insider section'a scroll yap ve verify et
        life_element = self.wait.until(EC.presence_of_element_located(self.life_at_insider_section))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", life_element)
        assert life_element.is_displayed(), "Life at Insider bölümü görüntülenemiyor!"
        time.sleep(2)  # Görsel doğrulama için bekleme
        print("✓ Life at Insider bölümü başarıyla görüntülendi")

   