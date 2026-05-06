from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    # 1. Inicializar el navegador 
    driver = webdriver.Chrome() 
    # 2. Navegar a la URL
    driver.get("https://ejemplo.com")
    # 3. Ejecución de pasos
    driver.find_element(By.ID, "user").send_keys("admin") 
    driver.find_element(By.ID, "pass").send_keys("1234") 
    driver.find_element(By.ID, "login-btn").click()
    # 4. Verificación
    assert "Bienvenido" in driver.page_source
    # 5. Cierre
    driver.quit()
