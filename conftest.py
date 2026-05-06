import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


@pytest.fixture
def driver():
    """Configuración del navegador con opciones para CI/CD y local"""
    options = Options()
    # Activar headless en CI/CD (cuando GITHUB_ACTIONS está activo)
    if os.getenv('GITHUB_ACTIONS'):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capturar screenshot en caso de fallo para el reporte HTML"""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            screenshot = driver.get_screenshot_as_base64()
            html = f'''
            <div>
                <img src="data:image/png;base64,{screenshot}"
                style="width:300px;"
                onclick="window.open(this.src)"/>
            </div>
            '''
            extras.append(pytest_html.extras.html(html))
            report.extra = extras