import inspect
import logging
from pathlib import Path
from typing import Dict, Any
import html


class CustomFormatter(logging.Formatter):
    """Handles both ANSI console colors and HTML formatting"""

    # ANSI Color Codes
    ANSI_COLORS = {
        'RESET': '\033[0m',
        'DEBUG': '\033[32m',  # Green
        'INFO': '\033[38;5;39m',  # Deeper sky blue (ANSI color 39)
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[1;31m',  # Bold Red
        'CLASS_HEADER': '\033[34m',  # Blue
        'TEST_HEADER': '\033[38;5;6m',  # Teal
        'PASS': '\033[1;32m',  # Bold Green
        'FAIL': '\033[1;31m',  # Bold Red
    }

    # HTML Color Styles
    HTML_COLORS = {
        'DEBUG': 'color:green',
        'INFO': 'color:#007FFF',  # Azure blue
        'WARNING': 'color:orange',
        'ERROR': 'color:red',
        'CRITICAL': 'color:Crimson;font-weight:bold',
        'CLASS_HEADER': 'color:blue',
        'TEST_HEADER': 'color:MediumAquamarine',
        'PASS': 'color:lime;font-weight:bold',
        'FAIL': 'color:red;font-weight:bold',
    }

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        self._html_mode = False
        self._ansi_mode = False

    def format(self, record: logging.LogRecord) -> str:
        """Format the record with colors based on output mode"""
        message = record.getMessage() if getattr(record, 'simple', False) else super().format(record)

        color = getattr(record, 'color', record.levelname)

        if self._html_mode:
            return self._format_html(message, color)

        elif self._ansi_mode:
            return self._format_ansi(message, color)

        return message

    def _format_ansi(self, message: str, color: str) -> str:
        """Format with ANSI color codes"""
        ansi_color = self.ANSI_COLORS.get(color, '')

        return f"{ansi_color}{message}{self.ANSI_COLORS['RESET']}"

    def _format_html(self, message: str, color: str) -> str:
        """Special HTML formatting that preserves console-style centering"""

        style = self.HTML_COLORS.get(color, '')
        escaped = html.escape(message)

        return f'<div style="font-family: monospace; white-space: pre;{style}">{escaped}</div>'

    def set_html_mode(self, enabled: bool):
        self._html_mode = enabled
        self._ansi_mode = not enabled


class CustomLogger(logging.Logger):
    """Logger with custom output capabilities"""

    def __init__(self, name: str, level=logging.INFO):
        super().__init__(name, level)

        self.setLevel(logging.DEBUG)  # set the root logger level

        self.test_results: Dict[str, int] = {'passed': 0, 'failed': 0}

    def setup_handlers(self, report_path: str, level: int):
        if  not self.handlers:
            log_dir = Path(report_path)
            log_dir.mkdir(parents=True, exist_ok=True)

            # Clear existing log files
            for log_file in [log_dir / "info.log", log_dir / "debug.log"]:
                if log_file.exists():
                    log_file.unlink()

            console_formatter = CustomFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_formatter.set_html_mode(enabled=False)

            html_formatter = CustomFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            html_formatter.set_html_mode(enabled=True)

            # 1. Terminal Handler (colored)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(console_formatter)
            self.addHandler(console_handler)

            # 2. Info File Handler (colored)
            info_handler = logging.FileHandler(filename=log_dir / "info.html", encoding='utf-8', mode='w')
            info_handler.setLevel(logging.INFO)
            info_handler.setFormatter(html_formatter)
            self.addHandler(info_handler)

            # 3. Debug File Handler (colored)
            debug_handler = logging.FileHandler(filename=log_dir / "debug.html", encoding='utf-8', mode='w')
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(html_formatter)
            self.addHandler(debug_handler)

    def print_class_header(self, class_name: str) -> None:
        header = self._format_header_footer(f"{class_name}.py")
        self._print_colored(message=header, color='CLASS_HEADER',simple= True)

    def print_test_header(self, test_name: str):
        header = self._format_header_footer(f"RUNNING: {test_name}")
        self._print_colored(message=header, color='TEST_HEADER',simple= True)

    def print_test_footer(self, item: Any) -> None:
        rep_call = getattr(item, 'rep_call', None)

        if rep_call is None:
            status, color = "UNKNOWN", 'WARNING'  # Handle missing rep_call

        elif getattr(rep_call, 'failed', False):
            status, color = "FAILED", 'FAIL'
        else:
            status, color = "PASSED", 'PASS'

        footer = self._format_header_footer(status)
        self._print_colored(message=footer, color=color, simple=True)

    def log_test_result(self, item: Any) -> None:
        rep_call = getattr(item, 'rep_call', None)

        if rep_call and getattr(rep_call, 'failed', False):
            self.test_results['failed'] += 1
        else:
            self.test_results['passed'] += 1

    def print_final_summary(self) -> None:
        total = self.test_results['passed'] + self.test_results['failed']
        passed_pct = (self.test_results['passed'] / total * 100) if total else 0
        failed_pct = (self.test_results['failed'] / total * 100) if total else 0

        summary = (
            f"\n{' TEST SUMMARY ':=^100}\n"
            f"Passed:    {self.test_results['passed']} ({passed_pct:.1f}%)\n"
            f"Failed:    {self.test_results['failed']} ({failed_pct:.1f}%)\n"
            f"Total:     {total}\n"
            f"{'':=^100}"
        )

        color = 'FAIL' if self.test_results['failed'] > 0 else 'PASS'
        self._print_colored(message=summary, color=color, simple=True)

    def _format_header_footer(self, text: str, width: int = 100, border_char: str = '=') -> str:
        border = border_char * width
        return f"\n{border}\n{text.center(width)}\n{border}\n"

    def info(self, msg, *args, exc_info = None, stack_info = False, stacklevel = 1, extra = None) -> None:
        super().info(msg=f'{self._get_current_class_name()} - {msg}', *args, exc_info=exc_info, stacklevel=stacklevel, extra=extra)

    def debug(self, msg, *args, exc_info = None, stacklevel = 1) -> None:
        super().debug(msg=f'{self._get_current_class_name()} - {msg}', *args, exc_info=exc_info, stacklevel=stacklevel)

    def warning(self, msg, *args, exc_info = None, stacklevel = 1) -> None:
        super().warning(msg=f'{self._get_current_class_name()} - {msg}', *args, exc_info=exc_info, stacklevel=stacklevel)

    def error(self, msg, *args, exc_info = None, stacklevel = 1) -> None:
        super().error(msg=f'{self._get_current_class_name()} - {msg}', *args, exc_info=exc_info, stacklevel=stacklevel)

    def _print_colored(self, message: str, color: str, level: int = logging.INFO, simple: bool = False):
        """Helper method for colored messages"""
        record = self.makeRecord(
            self.name, level, __file__, 0,
            message, None, None, None, {'color': color, 'simple': simple}
        )
        self.handle(record)

    def _get_current_class_name(self) -> str:
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)
        class_name = self.name
        # Find the frame that called the logger
        for frame_info in outer_frames:
            self_obj = frame_info.frame.f_locals.get('self')

            if self_obj and not isinstance(self_obj, CustomLogger):
                class_name = type(self_obj).__name__
                break

        return class_name