import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager as FirefoxDriverManager


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser driver type, valid values: chrome(default), edge, firefox")
    parser.addoption("--timeout", action="store", default="10", help="Waiting driver timeout in seconds, default 10 seconds")
    parser.addoption("--console-log-level", action="store", default="info", help="Console log level, valid values: debug, info, warning, error")
    parser.addoption("--headless", action="store_true", default=False, help="Run tests in headless mode (no browser window), default False")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser_name == "edge":
        options = EdgeOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(service=FirefoxService(FirefoxDriverManager().install()), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}, available browsers are chrome, edge, and firefox")

    driver.maximize_window()

    yield driver

    driver.quit()


def pytest_runtest_logstart(nodeid, location):
    """Disable test start messages"""
    pass

def pytest_runtest_logfinish(nodeid, location):
    """Disable test finish messages"""
    pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Store all phases (setup/call/teardown)
    setattr(item, f"rep_{rep.when}", rep)
