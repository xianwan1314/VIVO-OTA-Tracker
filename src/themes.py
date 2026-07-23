THEMES = {
    'light': {
        'name': '浅色',
        'app_bg': 'rgba(245, 247, 250, 0.52)',
        'card_bg': 'rgba(255, 255, 255, 0.76)',
        'text': '#1a1a2e',
        'text_secondary': '#666680',
        'accent': '#4a90d9',
        'accent_hover': '#357abd',
        'border': 'rgba(210, 218, 228, 0.78)',
        'log_bg': 'rgba(255, 255, 255, 0.68)',
        'log_text': '#1a1a2e',
        'btn_bg': 'rgba(232, 236, 241, 0.82)',
        'btn_text': '#1a1a2e',
        'btn_hover': 'rgba(221, 225, 230, 0.92)',
        'btn_primary_bg': '#4a90d9',
        'btn_primary_hover': '#357abd',
        'btn_primary_text': '#ffffff',
        'btn_success_bg': '#52c41a',
        'btn_success_hover': '#45a615',
        'btn_success_text': '#ffffff',
        'input_bg': 'rgba(255, 255, 255, 0.78)',
        'input_text': '#1a1a2e',
        'input_border': 'rgba(208, 213, 221, 0.86)',
        'input_focus': '#4a90d9',
        'group_title': '#4a90d9',
        'progress_bg': 'rgba(232, 236, 241, 0.70)',
        'progress_chunk': '#4a90d9',
        'scrollbar_bg': 'rgba(232, 236, 241, 0.35)',
        'scrollbar_thumb': 'rgba(192, 196, 204, 0.72)',
        'shadow': 'rgba(0,0,0,0.06)',
    },
    'dark': {
        'name': '深色',
        'app_bg': 'rgba(15, 15, 26, 0.58)',
        'card_bg': 'rgba(26, 26, 46, 0.74)',
        'text': '#e4e6eb',
        'text_secondary': '#b0b3b8',
        'accent': '#5b9bd5',
        'accent_hover': '#4a8ac4',
        'border': 'rgba(69, 75, 104, 0.72)',
        'log_bg': 'rgba(26, 26, 46, 0.68)',
        'log_text': '#e4e6eb',
        'btn_bg': 'rgba(42, 42, 68, 0.82)',
        'btn_text': '#e4e6eb',
        'btn_hover': 'rgba(53, 53, 90, 0.92)',
        'btn_primary_bg': '#5b9bd5',
        'btn_primary_hover': '#4a8ac4',
        'btn_primary_text': '#ffffff',
        'btn_success_bg': '#45a615',
        'btn_success_hover': '#3a8e11',
        'btn_success_text': '#ffffff',
        'input_bg': 'rgba(37, 37, 64, 0.82)',
        'input_text': '#e4e6eb',
        'input_border': 'rgba(77, 77, 111, 0.82)',
        'input_focus': '#5b9bd5',
        'group_title': '#5b9bd5',
        'progress_bg': 'rgba(42, 42, 68, 0.70)',
        'progress_chunk': '#5b9bd5',
        'scrollbar_bg': 'rgba(26, 26, 46, 0.35)',
        'scrollbar_thumb': 'rgba(77, 77, 92, 0.72)',
        'shadow': 'rgba(0,0,0,0.30)',
    }
}

WINDOW_STYLE_CONFIG = {
    'light': {
        'style': 'acrylic',
        'fallback_style': 'aero',
        'header_color': '#ffffff',
        'title_color': '#1a1a2e',
        'border_color': '#4a90d9',
    },
    'dark': {
        'style': 'acrylic',
        'fallback_style': 'dark',
        'header_color': '#1a1a2e',
        'title_color': '#e4e6eb',
        'border_color': '#5b9bd5',
    },
}


def make_stylesheet(theme, scale=1.0):
    px = lambda value: max(1, int(round(value * scale)))
    return f"""
    QMainWindow {{
        background-color: {theme['app_bg']};
    }}
    QWidget {{
        color: {theme['text']};
        font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    }}
    QGroupBox {{
        background-color: {theme['card_bg']};
        border: {px(1)}px solid {theme['border']};
        border-radius: {px(10)}px;
        margin-top: {px(14)}px;
        padding: {px(22)}px {px(16)}px {px(18)}px {px(16)}px;
        font-weight: bold;
        font-size: {px(13)}px;
        color: {theme['group_title']};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 {px(8)}px;
        color: {theme['group_title']};
    }}
    QLabel {{
        color: {theme['text']};
        background: transparent;
    }}
    QLineEdit {{
        background-color: {theme['input_bg']};
        color: {theme['input_text']};
        border: {px(2)}px solid {theme['input_border']};
        border-radius: {px(8)}px;
        padding: {px(7)}px {px(12)}px;
        font-size: {px(13)}px;
        min-height: {px(20)}px;
    }}
    QLineEdit:focus {{
        border-color: {theme['input_focus']};
    }}
    QPushButton {{
        border: none;
        border-radius: {px(8)}px;
        padding: {px(8)}px {px(18)}px;
        font-size: {px(13)}px;
        font-weight: 500;
        background-color: {theme['btn_bg']};
        color: {theme['btn_text']};
    }}
    QPushButton:hover {{
        background-color: {theme['btn_hover']};
    }}
    QPushButton:pressed {{
        background-color: {theme['border']};
    }}
    QPushButton:disabled {{
        opacity: 0.45;
    }}
    QPushButton#runBtn {{
        background-color: {theme['btn_primary_bg']};
        color: {theme['btn_primary_text']};
        font-weight: bold;
    }}
    QPushButton#runBtn:hover {{
        background-color: {theme['btn_primary_hover']};
    }}
    QPushButton#copyBtn {{
        background-color: {theme['btn_success_bg']};
        color: {theme['btn_success_text']};
        font-weight: bold;
        border-radius: {px(8)}px;
    }}
    QPushButton#copyBtn:hover {{
        background-color: {theme['btn_success_hover']};
    }}
    QPushButton#iconBtn {{
        background: transparent;
        border: {px(2)}px solid {theme['border']};
        border-radius: {px(8)}px;
        padding: {px(6)}px {px(14)}px;
        font-weight: bold;
        font-size: {px(12)}px;
        color: {theme['text_secondary']};
    }}
    QPushButton#iconBtn:hover {{
        background-color: {theme['btn_hover']};
        color: {theme['text']};
    }}
    QComboBox {{
        background-color: {theme['input_bg']};
        color: {theme['input_text']};
        border: {px(2)}px solid {theme['input_border']};
        border-radius: {px(8)}px;
        padding: {px(7)}px {px(12)}px;
        font-size: {px(13)}px;
        min-height: {px(20)}px;
    }}
    QComboBox:hover {{
        border-color: {theme['input_focus']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: {px(28)}px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {theme['card_bg']};
        color: {theme['text']};
        border: {px(1)}px solid {theme['border']};
        selection-background-color: {theme['accent']};
        border-radius: {px(4)}px;
    }}
    QCheckBox {{
        color: {theme['text_secondary']};
        spacing: {px(6)}px;
        font-size: {px(12)}px;
    }}
    QCheckBox::indicator {{
        width: {px(16)}px; height: {px(16)}px;
        border: {px(2)}px solid {theme['input_border']};
        border-radius: {px(4)}px;
        background: {theme['input_bg']};
    }}
    QCheckBox::indicator:checked {{
        background: {theme['accent']};
        border-color: {theme['accent']};
    }}
    QProgressBar {{
        border: none;
        border-radius: {px(6)}px;
        background-color: {theme['progress_bg']};
        height: {px(6)}px;
        text-align: center;
        font-size: {px(11)}px;
    }}
    QProgressBar::chunk {{
        background-color: {theme['progress_chunk']};
        border-radius: {px(6)}px;
    }}
    QTextEdit {{
        background-color: {theme['log_bg']};
        color: {theme['log_text']};
        border: {px(2)}px solid {theme['border']};
        border-radius: {px(10)}px;
        padding: {px(12)}px;
        font-family: "Cascadia Code", "Consolas", "Microsoft YaHei", monospace;
        font-size: {px(12)}px;
    }}
    QWidget#updateLogPanel {{
        background-color: {theme['card_bg']};
        border: {px(1)}px solid {theme['border']};
        border-radius: {px(10)}px;
    }}
    QLabel#updateLogTitle {{
        color: {theme['group_title']};
        font-size: {px(14)}px;
        font-weight: bold;
    }}
    QPushButton#updateLogCloseBtn {{
        background-color: transparent;
        color: {theme['text_secondary']};
        border: none;
        border-radius: {px(6)}px;
        padding: {px(4)}px {px(8)}px;
        font-size: {px(16)}px;
        font-weight: bold;
    }}
    QPushButton#updateLogCloseBtn:hover {{
        background-color: {theme['btn_hover']};
        color: {theme['text']};
    }}
    QPushButton#updateLogToggleBtn {{
        background-color: {theme['btn_primary_bg']};
        color: {theme['btn_primary_text']};
        border: none;
        border-radius: {px(8)}px;
        padding: {px(6)}px {px(10)}px;
        font-size: {px(12)}px;
        font-weight: bold;
    }}
    QPushButton#updateLogToggleBtn:hover {{
        background-color: {theme['btn_primary_hover']};
    }}
    QTextBrowser#updateLogBrowser {{
        background-color: transparent;
        color: {theme['text']};
        border: none;
        padding: {px(8)}px;
        font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
        font-size: {px(13)}px;
    }}
    QLabel#toastBubble {{
        background-color: {theme['card_bg']};
        color: {theme['text']};
        border: {px(1)}px solid {theme['border']};
        border-radius: {px(8)}px;
        padding: {px(9)}px {px(14)}px;
        font-size: {px(13)}px;
        font-weight: 500;
    }}
    QScrollBar:vertical {{
        background: {theme['scrollbar_bg']};
        width: {px(8)}px;
        border-radius: {px(4)}px;
    }}
    QScrollBar::handle:vertical {{
        background: {theme['scrollbar_thumb']};
        border-radius: {px(4)}px;
        min-height: {px(30)}px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QMessageBox {{
        background-color: {theme['card_bg']};
    }}
    QMessageBox QLabel {{
        color: {theme['text']};
        font-size: {px(13)}px;
    }}
    QMessageBox QPushButton {{
        background-color: {theme['btn_primary_bg']};
        color: {theme['btn_primary_text']};
        border-radius: {px(6)}px;
        padding: {px(6)}px {px(20)}px;
        font-weight: bold;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {theme['btn_primary_hover']};
    }}
    """
