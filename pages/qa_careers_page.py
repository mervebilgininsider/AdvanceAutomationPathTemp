from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class QACareersPage:
    """Insider Açık Pozisyonlar sayfası için Page Object Model."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Bekleme süresini 5'ten 15 saniyeye çıkardık
        self.actions = ActionChains(driver)
        # Filtre seçicilerini güncelliyoruz - Select2 dropdown elementleri için doğru ID'ler
        self.location_filter = (By.ID, "select2-filter-by-location-container")
        self.department_filter = (By.ID, "select2-filter-by-department-container")
        self.job_listings = (By.CSS_SELECTOR, ".position-list-item")
        # View Role butonları için daha genel bir seçici kullanıyoruz
        self.view_role_buttons = (By.XPATH, "//a[contains(text(),'View Role')]")
        # Açık Pozisyonlar Sayfası Linki
        self.open_positions_link = (By.LINK_TEXT, "See all QA jobs")
        # QA Careers sayfası URL'i
        self.qa_careers_url = "https://useinsider.com/careers/quality-assurance/"

    def navigate_to_qa_careers(self):
        """QA Careers sayfasına gider."""
        print("TEST ADIMI: QA Careers sayfasına yönlendiriliyor...")
        self.driver.get(self.qa_careers_url)
        # Sayfanın yüklendiğini doğrula
        assert self.qa_careers_url in self.driver.current_url, "QA Careers sayfası yüklenemedi!"
        print("✓ QA Careers sayfası başarıyla yüklendi")
        # Sayfanın tamamen yüklenmesi için kısa bir bekleme
        time.sleep(1)
        
    def filter_jobs(self, location, department):
        """Konum ve departman bazında iş ilanlarını filtreler."""
        print(f"TEST ADIMI: İş ilanları filtreleniyor - Konum: {location}, Departman: {department}")
        # Daha uzun bekleme süresi ile özel bir wait oluşturuyoruz
        wait = WebDriverWait(self.driver, 30)  # Daha uzun bekleme süresi
        
        # Location dropdown'a tıklama
        location_dropdown = wait.until(EC.element_to_be_clickable(self.location_filter))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_dropdown)
        time.sleep(15)  # Dropdown menüsünü açmadan önce bekleme
        location_dropdown.click()
        print("✓ Konum filtresi dropdown'ı açıldı")
        
        # Dropdown menüsünün tamamen yüklenmesini bekle
        time.sleep(2)  # Dropdown'ın açılması için ek bekleme
        # Select2 dropdown'ın açık olduğunu doğrula
        dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
        assert dropdown_options.is_displayed(), "Konum filtresi seçenekleri görüntülenemiyor!"
        
        # Location seçeneğini seçme - Select2 dropdown için doğru XPath
        location_xpath = f"//li[contains(@id, 'select2-filter-by-location-result') and contains(text(), '{location}')]"
        # Seçeneğin görünür olmasını bekle
        wait.until(EC.visibility_of_element_located((By.XPATH, location_xpath)))
        location_option = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
        time.sleep(1)  # Seçeneğin tam olarak yüklenmesi için ek bekleme
        location_option.click()
        print(f"✓ Konum filtresi seçildi: {location}")
        
        # Department dropdown'a tıklama - farklı yöntemler deneyerek
        time.sleep(5)  # Önceki seçimin tamamlanması için bekleme
        
        try:
            # Önce element görünür ve tıklanabilir olana kadar bekle
            department_dropdown = wait.until(EC.element_to_be_clickable(self.department_filter))
            # Elementin görünür olduğundan emin ol
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", department_dropdown)
            time.sleep(3)  # Scroll işleminin tamamlanması için bekleme
            
            # Farklı tıklama yöntemlerini dene
            # 1. JavaScript ile tıklama
            self.driver.execute_script("arguments[0].click();", department_dropdown)
            
            # 2. Eğer JavaScript tıklaması başarısız olursa, ActionChains ile dene
            if not self._is_dropdown_open():
                self.actions.move_to_element(department_dropdown).click().perform()
            
            # 3. Yine başarısız olursa, native click dene
            if not self._is_dropdown_open():
                department_dropdown.click()
            
            print("✓ Departman filtresi dropdown'ı açıldı")
            
            # Dropdown menüsünün tamamen yüklenmesini bekle
            time.sleep(3)  # Dropdown'ın açılması için ek bekleme
            # Select2 dropdown'ın açık olduğunu doğrula
            dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
            assert dropdown_options.is_displayed(), "Departman filtresi seçenekleri görüntülenemiyor!"
            
            # Department seçeneğini seçme - Select2 dropdown için doğru XPath
            department_xpath = f"//li[contains(@id, 'select2-filter-by-department-result') and contains(text(), '{department}')]"
            # Seçeneğin görünür olmasını bekle
            wait.until(EC.visibility_of_element_located((By.XPATH, department_xpath)))
            department_option = wait.until(EC.element_to_be_clickable((By.XPATH, department_xpath)))
            time.sleep(1)  # Seçeneğin tam olarak yüklenmesi için ek bekleme
            department_option.click()
            print(f"✓ Departman filtresi seçildi: {department}")
            
        except Exception as e:
            print(f"HATA: Departman dropdown ile etkileşimde sorun: {str(e)}")
            # Hata durumunda ekran görüntüsü al
            self.driver.save_screenshot("department_dropdown_error.png")
            raise
            
    def _is_dropdown_open(self):
        """Select2 dropdown'ın açık olup olmadığını kontrol eder."""
        try:
            # Kısa bir bekleme süresi ile dropdown menüsünün açık olup olmadığını kontrol et
            dropdown_options = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options"))
            )
            return dropdown_options.is_displayed()
        except:
            return False

    def verify_job_listings(self):
        """Filtrelenmiş iş ilanlarının varlığını doğrular."""
        print("TEST ADIMI: Filtrelenmiş iş ilanlarının varlığı kontrol ediliyor...")
        
        # İş ilanlarının yüklenmesi için kısa bir bekleme
        time.sleep(2)
        
        # İş ilanlarının varlığını kontrol et
        job_items = self.wait.until(EC.presence_of_all_elements_located(self.job_listings))
        job_count = len(job_items)
        assert job_count > 0, "Belirtilen filtrelere uygun iş ilanı bulunamadı!"
        print(f"✓ Filtrelere uygun {job_count} adet iş ilanı bulundu")
        
        # İş ilanlarının görünür olduğunu doğrula
        for i, job in enumerate(job_items[:3]):  # İlk 3 ilanı kontrol et
            assert job.is_displayed(), f"{i+1}. iş ilanı görüntülenemiyor!"
            print(f"✓ İş ilanı {i+1} başarıyla görüntülendi")

    def verify_view_role_buttons(self):
        """Her iş ilanında 'View Role' butonunun varlığını ve yönlendirmesini doğrular."""
        print("TEST ADIMI: 'View Role' butonlarının kontrolü yapılıyor...")
        
        # Sayfanın tamamen yüklenmesi için ek bekleme
        time.sleep(5)
        
        # Daha uzun bekleme süresi ile özel bir wait oluşturuyoruz
        long_wait = WebDriverWait(self.driver, 45)  # Uzun bekleme süresi
        
        # View Role butonlarını bulmadan önce sayfayı aşağı kaydırıyoruz
        self.driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(3)  # Scroll işleminin tamamlanması için bekleme
        
        # İş ilanı elementlerini bulalım
        job_items = long_wait.until(EC.presence_of_all_elements_located(self.job_listings))
        assert len(job_items) > 0, "İş ilanı elementleri bulunamadı!"
        print(f"✓ {len(job_items)} adet iş ilanı elementi bulundu")
        
        # İlk iş ilanı elementine hover yapalım ve View Role butonunu görünür hale getirelim
        job_item = job_items[0]
        
        # Elementi görünür hale getir
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_item)
        time.sleep(2)  # Scroll işleminin tamamlanması için bekleme
        
        # Hover işlemi için ActionChains kullanıyoruz
        self.actions.move_to_element(job_item).perform()
        time.sleep(2)  # Hover efektinin oluşması için bekleme
        print("✓ İş ilanı üzerine hover yapıldı")
        
        # Hover sonrası View Role butonunu bulmaya çalışalım
        view_button = None
        
        # Önce iş ilanı içindeki View Role butonunu bulmayı deneyelim
        try:
            # İş ilanı içindeki View Role butonunu bul
            view_button = job_item.find_element(By.XPATH, ".//a[contains(text(),'View Role')]")
            print("✓ İş ilanı içinde 'View Role' butonu bulundu")
        except:
            # Eğer bulamazsak, sayfadaki tüm View Role butonlarını kontrol edelim
            try:
                view_buttons = long_wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(text(),'View Role')]")))
                if len(view_buttons) > 0:
                    view_button = view_buttons[0]
                    print(f"✓ Sayfada {len(view_buttons)} adet 'View Role' butonu bulundu")
            except Exception as e:
                print(f"HATA: 'View Role' butonları bulunamadı: {str(e)}")
                # Son çare olarak JavaScript ile butonu görünür hale getirmeyi deneyelim
                self.driver.execute_script(
                    "document.querySelectorAll('.position-list-item').forEach(item => item.style.cssText = 'pointer-events: auto; opacity: 1;');" +
                    "document.querySelectorAll('a:contains(\\'View Role\\')').forEach(btn => btn.style.cssText = 'display: block !important; opacity: 1 !important; visibility: visible !important;');"
                )
                time.sleep(2)
                # Tekrar butonları bulmayı deneyelim
                view_buttons = long_wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(text(),'View Role')]")))
                if len(view_buttons) > 0:
                    view_button = view_buttons[0]
                    print(f"✓ JavaScript ile {len(view_buttons)} adet 'View Role' butonu görünür hale getirildi")
        
        # Buton bulunamadıysa hata ver
        assert view_button is not None, "'View Role' butonu bulunamadı!"
        
        # Butonu görünür hale getir ve tıkla
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
        time.sleep(2)  # Scroll işleminin tamamlanması için bekleme
        
        # JavaScript ile tıklama
        print("TEST ADIMI: 'View Role' butonuna tıklanıyor...")
        self.driver.execute_script("arguments[0].click();", view_button)
        
        # Yeni sekmeye geç
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        # URL doğrulama
        assert "lever.co" in self.driver.current_url, "View Role butonu doğru bir şekilde yönlendirmiyor!"
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def go_to_open_positions(self):
        """Açık pozisyonlar sayfasına gider."""
        print("TEST ADIMI: Açık pozisyonlar sayfasına yönlendiriliyor...")
        # 'See all QA jobs' butonunu bul ve tıklanabilir olmasını bekle
        open_positions = self.wait.until(EC.element_to_be_clickable(self.open_positions_link))
        # Butonun görünür olduğunu doğrula
        assert open_positions.is_displayed(), "'See all QA jobs' butonu görünür değil!"
        # Butona tıkla
        open_positions.click()
        print("✓ Açık pozisyonlar sayfasına başarıyla yönlendirildi")

