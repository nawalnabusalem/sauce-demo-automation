# Sauce Demo Automation 🧪

Automated UI testing project for [Sauce Demo](https://www.saucedemo.com/) using **Selenium** and **Pytest**, built with maintainability and scalability in mind.



## 📦 Project Structure

This project uses the **Page Object Model (POM)** to separate test logic from page interactions.

<pre> 
sauce-demo-automation/
├── pages/ # Page Object Models
│ ├── login/
│ ├── checkout/
│ └── ...
├── tests/ # Test files organized by feature
│ ├── login/
│ ├── checkout/
│ └── ...
├── utils/ # Helpers & custom tools
│ └── test_helper.py
├── loggers/ # custom logger
│ └── ogger.py
├── reports/ # HTML test reports
├── requirements.txt
└── conftest.py
</pre>


## 🚀 Features

- **Selenium WebDriver** for browser automation.  
- **Pytest** as the testing framework.  
- **Page Object Model (POM)** for maintainability.  
- **GitHub Actions CI** for running tests on push/pull.  
- **Custom Logger** with:
  - Colored console output.
  - HTML logging for debugging.
- **Test Helper** utilities:
  - Simplified assertions.
  - Reusable test logic.


## ⚙️ Running the Tests

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run tests
```bash
pytest tests/login --browser=chrome --headless --html=reports/Login/chrome/login-report.html --self-contained-html
```

## 🧰 Test Configuration Options
This project uses **pytest** with custom command-line options to provide flexibility in running tests across different browsers and environments.

### 🔧 Available CLI Options
| Option                | Description                                                                                                     | Default  | Example                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------- | -------- | --------------------------- |
| `--browser`           | Specify the browser to run tests on. Supported values: `chrome`, `edge`, `firefox`.                             | `chrome` | `--browser=firefox`         |
| `--timeout`           | Set global wait timeout (in seconds) for driver operations.                                                     | `10`     | `--timeout=20`              |
| `--console-log-level` | Set our custom log verbosity level. Options: `debug`, `info`, `warning`, `error`.                               | `info`   | `--console-log-level=debug` |
| `--headless`          | Run the browser in headless mode (no UI). Useful for CI/CD environments.                                        | `False`  | `--headless`                |



## 🛠️ Continuous Integration (CI)

GitHub Actions workflow is configured to run tests on each push or pull request:

- Runs on Windows runners.
- Uses pytest to execute and generate HTML reports.
- Supports all major browsers (Chrome, Firefox, Edge).

## 📃 Test Logs and Reports

In addition to the **pytest HTML** report, the framework also includes a custom logger that generates two separate HTML log files for enhanced debugging:
| Log File     | Description                                                      |
| ------------ | ---------------------------------------------------------------- |
| `debug.html` | Contains detailed logs, including debug-level messages.          |
| `info.html`  | Contains higher-level logs, such as test outcomes and key steps. |

These files are especially useful for debugging failed test cases or understanding test execution flow.

