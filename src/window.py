import os
import re
import sys
import json
import html
import urllib.parse

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QDialog, QDialogButtonBox, QFrame)
from PyQt5.QtCore import Qt, QSize, QProcess, QUrl
from PyQt5.QtGui import QClipboard, QIcon, QPixmap, QFont
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

from qfluentwidgets import (LineEdit, ComboBox, PrimaryPushButton, PushButton,
                           CheckBox, TextEdit, TextBrowser, BodyLabel,
                           CaptionLabel, SubtitleLabel, TitleLabel,
                           ProgressBar, setTheme, Theme,
                           setThemeColor, InfoBar, InfoBarPosition,
                           FluentIcon as FIF, ScrollArea)

from .i18n import t, APP_VERSION
from .models import DEVICE_DATABASE, display_series_name, display_model_name
from .ota_core import (resource_path, build_java_command,
                       prepare_work_dir, cleanup_work_dir, parse_ota_result)

try:
    import pywinstyles
except ImportError:
    pywinstyles = None


def configure_high_dpi():
    from PyQt5.QtCore import Qt
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


class VivoOtaTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'zh'
        self.theme = 'light'

        setThemeColor('#0e6dfd')
        setTheme(Theme.LIGHT)

        self.setWindowTitle(t('window_title', self.lang))
        self.setFixedSize(840, 720)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        icon_path = resource_path("assets/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            QApplication.instance().setWindowIcon(QIcon(icon_path))

        font = QApplication.font()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(7)
        QApplication.setFont(font)

        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        self.config_dir = os.path.join(appdata, 'VivoOtaTracker')
        os.makedirs(self.config_dir, exist_ok=True)

        self.current_config = {
            'DEVICE_TYPE': 'phone',
            'MODEL_SW_VER': '',
            'DEVICE_MODEL': '',
            'SW_VERSION': '',
            'ANDROID_VER': ''
        }

        self.current_stage = None
        self.raw_output = ""
        self.last_result_text = ""
        self.last_result_data = {}
        self.last_update_log_text = ""
        self._update_log_visible = False
        self.last_update_log_html = ""
        self.update_log_url = ""
        self.update_log_data_url = ""
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self._on_update_log_page_loaded)

        self.init_ui()

    # ── UI init ────────────────────────────────────────

    def init_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        main_layout = self.main_layout
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        # ── Top bar ──
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.logo_label = QLabel()
        logo_path = resource_path("assets/logo_os11_img_pad.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaledToHeight(28, Qt.SmoothTransformation)
                self.logo_label.setPixmap(logo_pixmap)
        else:
            self.logo_label.setText("Vivo OTA")
        self.logo_label.setFixedHeight(32)
        top_row.addWidget(self.logo_label)

        self.title_label = BodyLabel("Vivo OTA Tracker")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_row.addWidget(self.title_label)
        top_row.addStretch()

        self.lang_btn = PushButton(t('lang_toggle', self.lang))
        self.lang_btn.setToolTip(t('lang_tip', self.lang))
        self.lang_btn.setFixedHeight(28)
        self.lang_btn.clicked.connect(self.toggle_language)
        top_row.addWidget(self.lang_btn)

        self.changelog_btn = PushButton(t('changelog_btn', self.lang))
        self.changelog_btn.setFixedHeight(28)
        self.changelog_btn.clicked.connect(self.show_changelog)
        top_row.addWidget(self.changelog_btn)

        self.about_btn = PushButton(t('about_btn', self.lang))
        self.about_btn.setFixedHeight(28)
        self.about_btn.clicked.connect(self.show_about)
        top_row.addWidget(self.about_btn)
        main_layout.addLayout(top_row)

        # ── Device selection card ──
        self.device_card = QFrame()
        self.device_card.setObjectName("GlassCard")
        device_layout = QVBoxLayout(self.device_card)
        device_layout.setContentsMargins(16, 12, 16, 12)
        device_layout.setSpacing(8)

        self.device_card_title = BodyLabel(t('device_model_select', self.lang))
        font = self.device_card_title.font()
        font.setBold(True)
        self.device_card_title.setFont(font)
        device_layout.addWidget(self.device_card_title)

        row0 = QHBoxLayout()
        row0.setSpacing(8)
        self.series_label = BodyLabel(t('series', self.lang))
        self.series_label.setFixedWidth(110)
        self.series_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row0.addWidget(self.series_label)
        self.series_combo = ComboBox()
        self._populate_series_combo()
        self.series_combo.currentIndexChanged.connect(self.on_series_changed)
        self._make_glass_popup(self.series_combo)
        row0.addWidget(self.series_combo, 1)
        device_layout.addLayout(row0)

        row0_2 = QHBoxLayout()
        row0_2.setSpacing(8)
        self.model_label = BodyLabel(t('model', self.lang))
        self.model_label.setFixedWidth(110)
        self.model_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row0_2.addWidget(self.model_label)
        self.model_combo = ComboBox()
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        self._make_glass_popup(self.model_combo)
        row0_2.addWidget(self.model_combo, 1)
        device_layout.addLayout(row0_2)
        main_layout.addWidget(self.device_card)

        # ── Config params card ──
        self.config_card = QFrame()
        self.config_card.setObjectName("GlassCard")
        config_layout = QVBoxLayout(self.config_card)
        config_layout.setContentsMargins(16, 12, 16, 12)
        config_layout.setSpacing(8)

        self.config_card_title = BodyLabel(t('config_params', self.lang))
        font = self.config_card_title.font()
        font.setBold(True)
        self.config_card_title.setFont(font)
        config_layout.addWidget(self.config_card_title)

        row1 = QHBoxLayout()
        row1.setSpacing(8)
        self.model_sw_ver_label = BodyLabel(t('model_sw_ver_label', self.lang))
        self.model_sw_ver_label.setFixedWidth(110)
        self.model_sw_ver_label.setToolTip(t('model_sw_ver_tip', self.lang))
        self.model_sw_ver_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row1.addWidget(self.model_sw_ver_label)
        self.model_sw_ver_edit = LineEdit()
        self.model_sw_ver_edit.setPlaceholderText(t('model_sw_ver_ph', self.lang))
        row1.addWidget(self.model_sw_ver_edit, 1)
        config_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(8)
        self.device_model_label = BodyLabel(t('device_model_label', self.lang))
        self.device_model_label.setFixedWidth(110)
        self.device_model_label.setToolTip(t('device_model_tip', self.lang))
        self.device_model_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row2.addWidget(self.device_model_label)
        self.device_model_edit = LineEdit()
        self.device_model_edit.setPlaceholderText(t('device_model_ph', self.lang))
        row2.addWidget(self.device_model_edit, 1)
        config_layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.setSpacing(8)
        self.sw_version_label = BodyLabel(t('sw_version_label', self.lang))
        self.sw_version_label.setFixedWidth(110)
        self.sw_version_label.setToolTip(t('sw_version_tip', self.lang))
        self.sw_version_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row3.addWidget(self.sw_version_label)
        self.sw_version_edits = []
        widths = [40, 34, 40, 34, 44]
        for i in range(5):
            edit = LineEdit()
            edit.setAlignment(Qt.AlignCenter)
            edit.setFixedWidth(widths[i])
            edit.textChanged.connect(self.on_sw_version_changed)
            self.sw_version_edits.append(edit)
            row3.addWidget(edit)
            if i < 4:
                dot = BodyLabel(".")
                dot.setAlignment(Qt.AlignCenter)
                dot.setFixedWidth(8)
                row3.addWidget(dot)
        row3.addStretch()
        config_layout.addLayout(row3)

        row4 = QHBoxLayout()
        row4.setSpacing(8)
        self.android_ver_label = BodyLabel(t('android_ver_label', self.lang))
        self.android_ver_label.setFixedWidth(110)
        self.android_ver_label.setToolTip(t('android_ver_tip', self.lang))
        self.android_ver_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row4.addWidget(self.android_ver_label)
        self.android_ver_edit = ComboBox()
        self.android_ver_edit.addItems([str(v) for v in range(10, 17)])
        self.android_ver_edit.setCurrentText("16")
        self.android_ver_edit.setToolTip(t('android_ver_tip', self.lang))
        self.android_ver_edit.setFixedWidth(100)
        self._make_glass_popup(self.android_ver_edit)
        row4.addWidget(self.android_ver_edit)
        row4.addStretch()
        config_layout.addLayout(row4)

        row5 = QHBoxLayout()
        row5.setSpacing(8)
        self.snp_label = BodyLabel(t('snp_label', self.lang))
        self.snp_label.setFixedWidth(110)
        self.snp_label.setToolTip(t('snp_tip', self.lang))
        self.snp_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row5.addWidget(self.snp_label)
        self.snp_edit = LineEdit()
        self.snp_edit.setFixedWidth(160)
        self.snp_edit.setToolTip(t('snp_tip', self.lang))
        row5.addWidget(self.snp_edit)
        row5.addSpacing(16)
        self.is_full_checkbox = CheckBox(t('is_full_label', self.lang))
        self.is_full_checkbox.setChecked(True)
        self.is_full_checkbox.setToolTip(t('is_full_tip', self.lang))
        row5.addWidget(self.is_full_checkbox)
        config_layout.addLayout(row5)
        main_layout.addWidget(self.config_card)

        # ── Button row ──
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        self.run_btn = PrimaryPushButton(t('start_get_link', self.lang))
        self.run_btn.setFixedHeight(38)
        self.run_btn.clicked.connect(self.run_tracker)
        icon_path = resource_path("assets/ic_upgrade.png")
        if os.path.exists(icon_path):
            self.run_btn.setIcon(QIcon(icon_path))
            self.run_btn.setIconSize(QSize(18, 18))
        self.verbose_checkbox = CheckBox(t('verbose_mode', self.lang))
        self.verbose_checkbox.setToolTip(t('verbose_tip', self.lang))
        self.copy_btn = PushButton(t('copy_clipboard', self.lang))
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setVisible(False)
        button_layout.addStretch()
        button_layout.addWidget(self.run_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.verbose_checkbox)
        button_layout.addWidget(self.copy_btn)
        main_layout.addLayout(button_layout)

        # ── Progress bar ──
        self.progress_bar = ProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # ── Log output ──
        self.log_output = TextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(160)
        main_layout.addWidget(self.log_output)

        # ── Credit label ──
        self.credit_label = QLabel()
        self.credit_label.setOpenExternalLinks(True)
        self.credit_label.setTextFormat(Qt.RichText)
        self.credit_label.setAlignment(Qt.AlignCenter)
        self._update_credit_label()
        main_layout.addWidget(self.credit_label)

        # ── Update log dialog + toggle button ──
        self._init_update_log_dialog()
        self.update_log_toggle_btn = PushButton(t('update_log_link', self.lang))
        self.update_log_toggle_btn.setFixedHeight(28)
        self.update_log_toggle_btn.clicked.connect(self.toggle_update_log_panel)
        self.update_log_toggle_btn.setVisible(False)
        button_layout.addWidget(self.update_log_toggle_btn)

        # ── Process ──
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_process_output)
        self.process.readyReadStandardError.connect(self.on_process_error)
        self.process.finished.connect(self.on_process_finished)

        self.on_series_changed()

        if pywinstyles and sys.platform == 'win32':
            pywinstyles.apply_style(self, "acrylic")
            hwnd = int(self.winId())
            pywinstyles.ChangeDWMAccent(hwnd, 30, 3, color=0x99EEEEEE)

        self._apply_glass()

    def _make_glass_popup(self, combo):
        original_create = combo._createComboMenu

        def create_glass_menu():
            menu = original_create()
            try:
                menu.view.setStyleSheet(
                    "MenuActionListWidget { background-color: rgba(255,255,255,40); color: #fff; "
                    "border: none; border-radius: 8px; padding: 4px; outline: none; }"
                    "MenuActionListWidget::item { padding: 6px 16px; border-radius: 5px; color: #fff; }"
                    "MenuActionListWidget::item:selected { background-color: rgba(14,109,253,120); color: #fff; border: none; }")
            except Exception:
                pass
            return menu

        combo._createComboMenu = create_glass_menu

    def _apply_glass(self):
        bg_card = "#GlassCard { background-color: rgba(255,255,255,35); border: 1px solid rgba(255,255,255,80); border-radius: 12px; }"
        bg_input = "QWidget { background-color: rgba(255,255,255,45); color: #fff; border: 1px solid rgba(255,255,255,100); border-radius: 6px; font-size: 9px; }"
        bg_btn = """
            PushButton {
                background-color: rgba(255,255,255,25);
                color: #fff;
                border: 1px solid rgba(255,255,255,90);
                border-radius: 8px;
                padding: 5px 16px;
            }
            PushButton:hover {
                background-color: rgba(255,255,255,55);
                border: 1px solid rgba(255,255,255,160);
            }
            PushButton:pressed {
                background-color: rgba(255,255,255,15);
                border: 1px solid rgba(255,255,255,60);
            }
        """
        bg_label = "QLabel { background: transparent; color: #fff; font-weight: 500; }"
        bg_textedit = "QTextEdit { background-color: rgba(255,255,255,30); color: #fff; border: 1px solid rgba(255,255,255,90); border-radius: 6px; font-size: 9px; }"

        self.device_card.setStyleSheet(bg_card)
        self.config_card.setStyleSheet(bg_card)

        for edit in self.findChildren(LineEdit):
            edit.setStyleSheet(bg_input)

        for edit in self.findChildren(TextEdit):
            edit.setStyleSheet(bg_textedit)

        for browser in self.findChildren(TextBrowser):
            browser.setStyleSheet("QTextBrowser { background-color: rgba(255,255,255,30); color: #fff; border: 1px solid rgba(255,255,255,90); border-radius: 6px; font-size: 9px; }")

        for combo in self.findChildren(ComboBox):
            combo.setStyleSheet(bg_input)

        for btn in self.findChildren(PushButton):
            btn.setStyleSheet(bg_btn)

        self.run_btn.setStyleSheet("""
            PrimaryPushButton {
                background-color: rgba(14,109,253,180);
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 6px 20px 6px 32px;
                font-weight: 600;
            }
            PrimaryPushButton:hover {
                background-color: rgba(14,109,253,220);
            }
            PrimaryPushButton:pressed {
                background-color: rgba(14,109,253,140);
            }
        """)

        for bar in self.findChildren(ProgressBar):
            bar.setStyleSheet("ProgressBar { background-color: rgba(255,255,255,30); border-radius: 5px; }")

        for lbl in self.findChildren(QLabel):
            lbl.setStyleSheet(bg_label)

        for cb in self.findChildren(CheckBox):
            cb.setStyleSheet("QCheckBox { background: transparent; color: #fff; font-weight: 500; }")

    def _apply_dialog_glass(self, dlg):
        dlg.setAttribute(Qt.WA_TranslucentBackground)
        if pywinstyles and sys.platform == 'win32':
            pywinstyles.apply_style(dlg, "acrylic")
            hwnd = int(dlg.winId())
            pywinstyles.ChangeDWMAccent(hwnd, 30, 3, color=0x99EEEEEE)

    def _init_update_log_dialog(self):
        self.update_log_dialog = QDialog(self)
        self.update_log_dialog.setWindowTitle(t('update_log_title', self.lang))
        self.update_log_dialog.setFixedSize(520, 600)
        dlg_layout = QVBoxLayout(self.update_log_dialog)
        dlg_layout.setContentsMargins(16, 16, 16, 16)
        dlg_layout.setSpacing(8)

        self.update_log_browser = TextBrowser()
        self.update_log_browser.setOpenExternalLinks(True)
        self.update_log_browser.setStyleSheet(
            "QTextBrowser { background-color: rgba(255,255,255,30); color: #fff; "
            "border: 1px solid rgba(255,255,255,90); border-radius: 6px; font-size: 9px; }")
        dlg_layout.addWidget(self.update_log_browser)

        self._apply_dialog_glass(self.update_log_dialog)

    # ── Event handlers ─────────────────────────────────

    def closeEvent(self, event):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished(3000)
        cleanup_work_dir(getattr(self, 'work_dir', None))
        event.accept()

    # ── Toast ──────────────────────────────────────────

    def show_toast(self, message):
        InfoBar.success(
            title='',
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self
        )

    # ── Update log panel (simplified) ──────────────────

    def show_update_log_panel(self, html_content):
        if not hasattr(self, 'update_log_dialog'):
            return
        self.last_update_log_html = html_content or self._build_update_log_html(
            t('update_log_empty', self.lang), is_html=False)
        self.update_log_browser.setHtml(self.last_update_log_html)
        self.update_log_dialog.show()
        self.update_log_dialog.raise_()
        self.update_log_dialog.activateWindow()
        self._update_log_visible = True
        self.update_log_toggle_btn.setVisible(True)
        self.update_log_toggle_btn.setText(t('update_log_link', self.lang))

    def hide_update_log_panel(self):
        if hasattr(self, 'update_log_dialog'):
            self.update_log_dialog.hide()

    def toggle_update_log_panel(self):
        if self.update_log_dialog.isVisible():
            self.hide_update_log_panel()
        elif self.last_update_log_html:
            self.show_update_log_panel(self.last_update_log_html)
        elif self.update_log_url:
            self.load_update_log_url(self.update_log_url)
        else:
            html = self._build_update_log_html(t('update_log_empty', self.lang), is_html=False)
            self.show_update_log_panel(html)

    def reset_update_log_panel(self):
        if hasattr(self, 'update_log_dialog'):
            self.update_log_dialog.hide()
        self._update_log_visible = False
        self.last_update_log_html = ""
        self.update_log_url = ""
        self.update_log_data_url = ""
        if hasattr(self, 'update_log_toggle_btn'):
            self.update_log_toggle_btn.setVisible(False)

    # ── Network: update log URL loading ────────────────

    def load_update_log_url(self, url):
        if not url:
            return
        self.update_log_url = url
        self.update_log_data_url = ""
        loading = t('update_log_loading', self.lang)
        self.show_update_log_panel(self._build_update_log_html(loading, is_html=False))
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"User-Agent", b"Mozilla/5.0 VivoOtaTracker/1.0")
        self.network_manager.get(request)

    def _on_update_log_page_loaded(self, reply):
        url = reply.url().toString()
        if reply.error():
            message = f"{t('update_log_load_failed', self.lang)}\n\n{reply.errorString()}"
            self.update_log_browser.setHtml(self._build_update_log_html(message, is_html=False))
            reply.deleteLater()
            return
        data = bytes(reply.readAll())
        reply.deleteLater()
        page_text = self._decode_webpage_bytes(data)
        if self.update_log_data_url and url == self.update_log_data_url:
            self.last_update_log_text = self._extract_vivo_update_data_text(page_text)
            self.last_update_log_html = self._build_vivo_update_data_html(page_text, url)
            self.update_log_browser.setHtml(self.last_update_log_html)
            self.last_result_text = self.format_clipboard_result(self.last_result_data, self.update_log_url)
            return
        data_url = self._find_vivo_update_data_url(page_text, url)
        if data_url:
            self.update_log_data_url = data_url
            self.update_log_browser.setHtml(
                self._build_update_log_html(t('update_log_loading', self.lang), is_html=False))
            request = QNetworkRequest(QUrl(data_url))
            request.setRawHeader(b"User-Agent", b"Mozilla/5.0 VivoOtaTracker/1.0")
            self.network_manager.get(request)
            return
        self.last_update_log_html = self._build_update_log_html(self._html_to_visible_text(page_text), is_html=False)
        self.last_update_log_text = self._html_to_visible_text(page_text)
        self.last_result_text = self.format_clipboard_result(self.last_result_data, self.update_log_url)
        self.update_log_browser.setHtml(self.last_update_log_html)

    # ── Webpage parsing helpers ────────────────────────

    def _decode_webpage_bytes(self, data):
        for encoding in ('utf-8', 'gb18030', 'gbk'):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                pass
        return data.decode('utf-8', errors='replace')

    def _find_vivo_update_data_url(self, page_html, page_url):
        if './data/' not in page_html and '/data/' not in page_html:
            return ""
        parsed = urllib.parse.urlparse(page_url)
        query = urllib.parse.parse_qs(parsed.query)
        lang = query.get('language', ['CN'])[0] or 'CN'
        if lang.upper() in ('ZH_CN', 'CN-ZH'):
            lang = 'CN'
        data_path = f"data/{lang}.js"
        return urllib.parse.urljoin(page_url, data_path)

    def _build_vivo_update_data_html(self, data_text, source_url):
        try:
            data = json.loads(data_text)
        except Exception:
            return self._build_update_log_html(self._html_to_visible_text(data_text), is_html=False)
        parts = []
        head = data.get('headContent')
        if isinstance(head, str) and head.strip():
            parts.append(f'<p>{html.escape(head.strip())}</p>')

        def desc_items(item):
            values = []
            desc = item.get('descContents')
            if isinstance(desc, list):
                for entry in desc:
                    if isinstance(entry, str):
                        values.append(entry)
                    elif isinstance(entry, dict):
                        value = entry.get('content') or entry.get('text')
                        if isinstance(value, str):
                            values.append(value)
            if not values and isinstance(item.get('content'), list):
                values.extend(str(v) for v in item['content'] if str(v).strip())
            return values

        def append_section(item, level=3):
            if not isinstance(item, dict):
                return
            title = item.get('title')
            children = item.get('children')
            lines = desc_items(item)
            if title:
                tag = 'h2' if level <= 2 else 'h3'
                parts.append(f'<{tag}>{html.escape(str(title))}</{tag}>')
            if lines:
                parts.append('<ul>')
                for line in lines:
                    parts.append(f'<li>{html.escape(str(line).strip())}</li>')
                parts.append('</ul>')
            if isinstance(children, list):
                for child in children:
                    append_section(child, level + 1)

        body = data.get('body')
        if isinstance(body, list):
            for item in body:
                append_section(item)
        if not parts:
            parts.append(f'<p class="empty">{html.escape(t("update_log_empty", self.lang))}</p>')
        return self._build_update_log_html(''.join(parts), is_html=True)

    def _extract_vivo_update_data_text(self, data_text):
        try:
            data = json.loads(data_text)
        except Exception:
            return self._html_to_visible_text(data_text)
        lines = []
        head = data.get('headContent')
        if isinstance(head, str) and head.strip():
            lines.append(head.strip())

        def desc_items(item):
            values = []
            desc = item.get('descContents')
            if isinstance(desc, list):
                for entry in desc:
                    if isinstance(entry, str):
                        values.append(entry)
                    elif isinstance(entry, dict):
                        value = entry.get('content') or entry.get('text')
                        if isinstance(value, str):
                            values.append(value)
            if not values and isinstance(item.get('content'), list):
                values.extend(str(v) for v in item['content'] if str(v).strip())
            return values

        def append_section(item):
            if not isinstance(item, dict):
                return
            title = item.get('title')
            if title:
                if lines and lines[-1] != "":
                    lines.append("")
                lines.append(str(title).strip())
            for line in desc_items(item):
                value = str(line).strip()
                if value:
                    lines.append(value)
            children = item.get('children')
            if isinstance(children, list):
                for child in children:
                    append_section(child)

        body = data.get('body')
        if isinstance(body, list):
            for item in body:
                append_section(item)
        return '\n'.join(line for line in lines if line is not None).strip()

    def _html_to_visible_text(self, page_html):
        text = re.sub(r'<script\b[^>]*>.*?</script>', ' ', page_html, flags=re.I | re.S)
        text = re.sub(r'<style\b[^>]*>.*?</style>', ' ', text, flags=re.I | re.S)
        text = re.sub(r'<!--.*?-->', ' ', text, flags=re.S)
        text = re.sub(r'</(p|div|li|dt|dd|h[1-6]|section|br)\s*>', '\n', text, flags=re.I)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)
        lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        return '\n'.join(lines) or t('update_log_empty', self.lang)

    # ── Update log HTML building ───────────────────────

    def _looks_like_html(self, text):
        return bool(re.search(r'</?(html|body|div|p|br|span|ul|ol|li|table|section|h[1-6])\b', text, re.I))

    def _looks_like_update_log_url(self, text):
        lower = text.lower()
        return (
            lower.startswith(('http://', 'https://')) and
            ('sysdesc.vivo.com.cn' in lower or '/upgrade/h5/' in lower or lower.endswith('/index.html'))
        )

    def _extract_update_log_url(self, raw_text, json_result=None):
        if json_result and json_result.get('changelog_url'):
            url = json_result['changelog_url'].replace('\\/', '/')
            if self._looks_like_update_log_url(url) or url.startswith('http'):
                return url

        payload = self._extract_raw_update_payload(raw_text)
        search_text = payload or raw_text
        if not search_text:
            return ""
        try:
            data = json.loads(payload) if payload else None
        except Exception:
            data = None
        candidates = []
        key_tokens = ('desc', 'log', 'content', 'html', 'url', 'h5', 'web', 'detail', 'release', 'note')

        def add_candidate(key, value):
            if not isinstance(value, str):
                return
            text = value.strip().replace('\\/', '/')
            if not self._looks_like_update_log_url(text):
                return
            score = 0
            lower_key = str(key).lower()
            lower = text.lower()
            if 'sysdesc.vivo.com.cn' in lower:
                score += 40
            if '/upgrade/h5/' in lower:
                score += 30
            if lower.endswith('/index.html'):
                score += 20
            if any(token in lower_key for token in key_tokens):
                score += 15
            candidates.append((score, text))

        def walk(obj, key=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, k)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item, key)
            else:
                add_candidate(key, obj)

        if data is not None:
            walk(data)
        else:
            for match in re.finditer(r'https?://[^\s"\'<>]+', search_text.replace('\\/', '/'), re.I):
                add_candidate('url', match.group(0))
        if not candidates:
            return ""
        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]

    def _extract_raw_update_payload(self, raw_text):
        from .ota_core import _extract_raw_update_payload as _extract
        return _extract(raw_text)

    def _build_update_log_html(self, content, is_html=None):
        if is_html is None:
            is_html = self._looks_like_html(content)
        body = content if is_html else html.escape(content).replace('\r\n', '\n').replace('\n', '<br>')
        text_color = '#ffffff'
        secondary = '#cccccc'
        accent = '#66b3ff'
        return f"""
        <!doctype html><html><head><meta charset="utf-8"><style>
            body {{ margin:0; padding:0; background:transparent; color:{text_color};
                   font-family:"Microsoft YaHei","Segoe UI",sans-serif; font-size:13px; line-height:1.7; }}
            a {{ color:{accent}; }}
            p {{ margin:0 0 10px 0; }}
            ul, ol {{ margin-top:6px; padding-left:22px; }}
            li {{ margin:4px 0; }}
            h1, h2, h3 {{ color:{accent}; margin:8px 0; }}
            .empty {{ color:{secondary}; }}
        </style></head><body>{body}</body></html>
        """

    def _extract_update_log_html(self, raw_text, json_result=None):
        payload = json_result.get('raw_response', '') if json_result else self._extract_raw_update_payload(raw_text)
        if not payload:
            return ""
        try:
            data = json.loads(payload)
        except Exception:
            data = None
        candidates = []
        key_tokens = ('log', 'desc', 'description', 'content', 'release', 'note',
                      'intro', 'detail', 'explain', 'feature', 'change')
        negative_tokens = ('url', 'pk', 'md5', 'hash', 'name', 'version', 'len', 'size')

        def add_candidate(key, value):
            if not isinstance(value, str):
                return
            text = value.strip()
            if len(text) < 12:
                return
            lower_key = str(key).lower()
            lower_text = text.lower()
            if lower_text.startswith(('http://', 'https://')):
                return
            if any(token in lower_key for token in negative_tokens):
                return
            score = 0
            if any(token in lower_key for token in key_tokens):
                score += 20
            if self._looks_like_html(text):
                score += 30
            if '<br' in lower_text or '&lt;' in lower_text:
                score += 8
            if any(word in text for word in ('更新', '优化', '修复', '新增', '系统', '安全', '稳定')):
                score += 8
            score += min(len(text) // 80, 12)
            if score > 0:
                candidates.append((score, text))

        def walk(obj, key=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, k)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item, key)
            else:
                add_candidate(key, obj)

        if data is not None:
            walk(data)
        if not candidates:
            return ""
        candidates.sort(key=lambda item: item[0], reverse=True)
        content = candidates[0][1]
        return self._build_update_log_html(content)

    # ── Language / UI text ─────────────────────────────

    def _update_credit_label(self):
        version_info = f"{APP_VERSION} | 2026-07-24" if self.lang == 'zh' else f"{APP_VERSION} | Built 2026-07-24"
        credit_html = (
            '<div style="text-align:center; padding:6px 0;">'
            '<span style="color:#ccc; font-size:11px;">'
            + t('credit_text', self.lang) +
            '</span>'
            '<a href="https://github.com/JerryTse-OSS/VIVO-OTA-Tracker" '
            'style="color:#66b3ff; font-size:11px; text-decoration:none;">'
            'JerryTse-OSS/VIVO-OTA-Tracker'
            '</a>'
            '<br><span style="color:#bbb; font-size:10px;">' + version_info + '</span>'
            '</div>'
        )
        self.credit_label.setText(credit_html)

    def _refresh_ui_texts(self):
        self.setWindowTitle(t('window_title', self.lang))
        self.lang_btn.setText(t('lang_toggle', self.lang))
        self.lang_btn.setToolTip(t('lang_tip', self.lang))
        self.changelog_btn.setText(t('changelog_btn', self.lang))
        self.changelog_btn.setText(t('changelog_btn', self.lang))
        self.about_btn.setText(t('about_btn', self.lang))
        self.device_card_title.setText(t('device_model_select', self.lang))
        self.series_label.setText(t('series', self.lang))
        self.model_label.setText(t('model', self.lang))
        self.config_card_title.setText(t('config_params', self.lang))
        self.model_sw_ver_label.setText(t('model_sw_ver_label', self.lang))
        self.model_sw_ver_label.setToolTip(t('model_sw_ver_tip', self.lang))
        self.model_sw_ver_edit.setPlaceholderText(t('model_sw_ver_ph', self.lang))
        self.device_model_label.setText(t('device_model_label', self.lang))
        self.device_model_label.setToolTip(t('device_model_tip', self.lang))
        self.device_model_edit.setPlaceholderText(t('device_model_ph', self.lang))
        self.sw_version_label.setText(t('sw_version_label', self.lang))
        self.sw_version_label.setToolTip(t('sw_version_tip', self.lang))
        self.android_ver_label.setText(t('android_ver_label', self.lang))
        self.android_ver_label.setToolTip(t('android_ver_tip', self.lang))
        self.snp_label.setText(t('snp_label', self.lang))
        self.snp_label.setToolTip(t('snp_tip', self.lang))
        self.snp_edit.setPlaceholderText(t('snp_ph', self.lang))
        self.is_full_checkbox.setText(t('is_full_label', self.lang))
        self.is_full_checkbox.setToolTip(t('is_full_tip', self.lang))
        self.android_ver_edit.setToolTip(t('android_ver_tip', self.lang))
        self.run_btn.setText(t('start_get_link', self.lang))
        self.verbose_checkbox.setText(t('verbose_mode', self.lang))
        self.verbose_checkbox.setToolTip(t('verbose_tip', self.lang))
        self.copy_btn.setText(t('copy_clipboard', self.lang))
        self.update_log_dialog.setWindowTitle(t('update_log_title', self.lang))
        self.update_log_toggle_btn.setText(t('update_log_link', self.lang))
        self._update_credit_label()

    def toggle_language(self):
        new_lang = 'en' if self.lang == 'zh' else 'zh'
        old_series_key = self.series_combo.currentData()
        old_model_data = self.model_combo.currentData()
        self.lang = new_lang
        self._refresh_ui_texts()
        self._populate_series_combo(old_series_key)
        self.on_series_changed()
        if old_model_data:
            for index in range(self.model_combo.count()):
                if self.model_combo.itemData(index) == old_model_data:
                    self.model_combo.setCurrentIndex(index)
                    break

    def show_changelog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(t('changelog_title', self.lang))
        dlg.setFixedSize(440, 480)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(16, 16, 16, 16)

        browser = TextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet(
            "QTextBrowser { background-color: rgba(255,255,255,30); color: #fff; "
            "border: 1px solid rgba(255,255,255,90); border-radius: 6px; font-size: 9px; }")
        browser.setHtml(t('changelog_text', self.lang))
        layout.addWidget(browser)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(btn_box)
        btn_box.accepted.connect(dlg.accept)

        self._apply_dialog_glass(dlg)
        dlg.exec_()

    def show_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(t('about_title', self.lang))
        dlg.setFixedSize(440, 420)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)

        browser = TextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet(
            "QTextBrowser { background-color: rgba(255,255,255,30); color: #fff; "
            "border: 1px solid rgba(255,255,255,90); border-radius: 6px; font-size: 10px; }")
        browser.setHtml(t('about_text', self.lang))
        layout.addWidget(browser)

        ok_btn = PushButton(t('ok_btn', self.lang))
        ok_btn.setFixedHeight(32)
        ok_btn.setStyleSheet("""
            PushButton {
                background-color: rgba(255,255,255,25);
                color: #fff;
                border: 1px solid rgba(255,255,255,90);
                border-radius: 8px;
            }
            PushButton:hover {
                background-color: rgba(255,255,255,55);
            }
        """)
        ok_btn.clicked.connect(dlg.accept)
        layout.addWidget(ok_btn, 0, Qt.AlignCenter)

        self._apply_dialog_glass(dlg)
        dlg.exec_()

    # ── Combo box population ───────────────────────────

    def _populate_series_combo(self, selected_key=None):
        self.series_combo.blockSignals(True)
        self.series_combo.clear()
        self.series_combo.addItem(t('select_device', self.lang), None)
        for series in DEVICE_DATABASE.keys():
            self.series_combo.addItem(display_series_name(series, self.lang), userData=series)
        if selected_key:
            for index in range(self.series_combo.count()):
                if self.series_combo.itemData(index) == selected_key:
                    self.series_combo.setCurrentIndex(index)
                    break
            else:
                self.series_combo.setCurrentIndex(0)
        else:
            self.series_combo.setCurrentIndex(0)
        self.series_combo.blockSignals(False)

    def on_series_changed(self, index=None):
        series = self.series_combo.currentData()
        self.model_combo.clear()
        self.model_combo.addItem(t('select_device', self.lang), None)
        if series not in DEVICE_DATABASE:
            self.model_sw_ver_edit.clear()
            self.device_model_edit.clear()
            self.current_config['MODEL_SW_VER'] = ''
            self.current_config['DEVICE_MODEL'] = ''
            return
        devices = DEVICE_DATABASE[series]
        for device in devices:
            self.model_combo.addItem(display_model_name(device, self.lang), userData=device)

    def on_model_changed(self, index):
        if index >= 0:
            device = self.model_combo.currentData()
            if not device:
                return
            self.model_sw_ver_edit.setText(device["codename"])
            self.device_model_edit.setText(device["model_sw_ver"])
            self.current_config['MODEL_SW_VER'] = device["codename"]
            self.current_config['DEVICE_MODEL'] = device["model_sw_ver"]

    # ── SW version helpers ─────────────────────────────

    def _get_sw_version(self):
        parts = [e.text().strip() for e in self.sw_version_edits]
        while parts and not parts[-1]:
            parts.pop()
        if not parts:
            return ''
        return '.'.join(parts)

    def _set_sw_version(self, ver):
        for e in self.sw_version_edits:
            e.clear()
        if not ver:
            return
        parts = ver.split('.')
        for i, p in enumerate(parts):
            if i < len(self.sw_version_edits):
                self.sw_version_edits[i].setText(p.strip())

    def on_sw_version_changed(self, text=None):
        ver = self._get_sw_version()
        match = re.match(r'\s*(1[0-6])(?:\.|$)', ver or '')
        if not match:
            return
        detected = match.group(1)
        if self.android_ver_edit.findText(detected) >= 0:
            self.android_ver_edit.setCurrentText(detected)

    # ── Run tracker ────────────────────────────────────

    def run_tracker(self):
        self.current_config['DEVICE_TYPE'] = 'tablet' if self.model_sw_ver_edit.text().strip().startswith('DPD') else 'phone'
        self.current_config['MODEL_SW_VER'] = self.model_sw_ver_edit.text().strip()
        self.current_config['DEVICE_MODEL'] = self.device_model_edit.text().strip()
        self.current_config['SW_VERSION'] = self._get_sw_version()
        self.current_config['ANDROID_VER'] = self.android_ver_edit.currentText().strip()
        self.current_config['SNP'] = self.snp_edit.text().strip() or 'A0000000000000A'
        self.current_config['IS_FULL'] = 'true' if self.is_full_checkbox.isChecked() else 'false'

        android_ver = self.current_config['ANDROID_VER']
        if not self.current_config['MODEL_SW_VER'] or \
           not self.current_config['DEVICE_MODEL'] or \
           not self.current_config['SW_VERSION'] or \
           not android_ver.isdigit():
            dlg = QDialog(self)
            dlg.setWindowTitle(t('warn_title', self.lang))
            dlg.setFixedSize(360, 160)
            dlg_layout = QVBoxLayout(dlg)
            dlg_layout.setContentsMargins(24, 24, 24, 24)
            msg_label = QLabel(t('warn_fill_all', self.lang))
            msg_label.setStyleSheet("color: #fff; font-size: 14px; background: transparent;")
            msg_label.setWordWrap(True)
            msg_label.setAlignment(Qt.AlignCenter)
            dlg_layout.addWidget(msg_label)
            ok_btn = PushButton(t('ok_btn', self.lang))
            ok_btn.setFixedHeight(32)
            ok_btn.setStyleSheet("""
                PushButton {
                    background-color: rgba(255,255,255,25);
                    color: #fff;
                    border: 1px solid rgba(255,255,255,90);
                    border-radius: 8px;
                }
                PushButton:hover {
                    background-color: rgba(255,255,255,55);
                }
            """)
            ok_btn.clicked.connect(dlg.accept)
            dlg_layout.addWidget(ok_btn, 0, Qt.AlignCenter)
            self._apply_dialog_glass(dlg)
            dlg.exec()
            return

        self.log_output.clear()
        self.raw_output = ""
        self.last_result_text = ""
        self.last_result_data = {}
        self.last_update_log_text = ""
        self.copy_btn.setVisible(False)
        self.reset_update_log_panel()

        if not self.verbose_checkbox.isChecked():
            self.log_output.append(t('please_wait', self.lang))
        else:
            self.log_output.append("==============================================")
            self.log_output.append("  Vivo OTA Tracker")
            self.log_output.append("==============================================")
            self.log_output.append("")

        self.run_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        cleanup_work_dir(getattr(self, 'work_dir', None))
        self.work_dir = prepare_work_dir()

        java_cmd, device_type = build_java_command(self.current_config, self.work_dir)
        if not java_cmd:
            self.log_output.append(f"[{t('error_title', self.lang)}] {t('error_no_java', self.lang)}")
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)
            return

        self.current_config['DEVICE_TYPE'] = device_type
        if self.verbose_checkbox.isChecked():
            self.log_output.append(f"{t('exec_cmd', self.lang)}: " + " ".join(java_cmd))
            self.log_output.append("")

        self.current_stage = 'run'
        self.process.setWorkingDirectory(self.work_dir)
        self.process.start(java_cmd[0], java_cmd[1:])

    def on_process_output(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        self.raw_output += output
        if self.verbose_checkbox.isChecked():
            self.log_output.append(output)
            self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def on_process_error(self):
        error = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
        self.raw_output += error
        if self.verbose_checkbox.isChecked():
            self.log_output.append(error)
            self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    # ── Result formatting ──────────────────────────────

    def _current_device_name(self):
        device = self.model_combo.currentData() if hasattr(self, 'model_combo') else None
        if isinstance(device, dict) and device.get('model'):
            return device['model']
        if self.current_config.get('DEVICE_MODEL') or self.current_config.get('MODEL_SW_VER'):
            return f"{self.current_config.get('DEVICE_MODEL', '')} / {self.current_config.get('MODEL_SW_VER', '')}".strip(' /')
        return ""

    def _device_type_display(self, device_type):
        mapping = {'phone': t('phone_cn', self.lang), 'tablet': t('tablet_cn', self.lang)}
        return mapping.get(device_type, device_type or "")

    def _result_lines(self, parsed, update_log_value=""):
        device_type = parsed.get('device_type') or self.current_config.get('DEVICE_TYPE', '')
        file_size = parsed.get('file_size') or parsed.get('file_size_mb', '')
        return [
            "vivo OTA Tracker By mytiantian",
            "",
            f"设备名称：{self._current_device_name()}",
            f"设备类型：{self._device_type_display(device_type)}",
            f"Android版本：{self.current_config.get('ANDROID_VER', '')}",
            f"软件版本：{parsed.get('update_version', '')}",
            f"软件包大小：{file_size + ' MB' if file_size else ''}",
            f"下载链接：{parsed.get('download_url', '')}",
            f"版本更新日志：{update_log_value}",
        ]

    def format_clean_result(self, parsed, update_log_value=""):
        return '\n'.join(self._result_lines(parsed, update_log_value))

    def format_clipboard_result(self, parsed, update_log_link=""):
        lines = self._result_lines(parsed, "")
        lines = lines[:-1] + ["", f"版本更新日志：{update_log_link or ''}"]
        return '\n'.join(lines).strip()

    def copy_to_clipboard(self):
        if not self.last_result_text:
            w = MessageBox(t('info_title', self.lang), t('no_result_to_copy', self.lang), self)
            w.cancelButton.hide()
            w.yesButton.setText('OK')
            w.exec()
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(self.last_result_text, QClipboard.Clipboard)
        clipboard.setText(self.last_result_text, QClipboard.Selection)
        self.show_toast(t('copied', self.lang))

    # ── Process finished ───────────────────────────────

    def on_process_finished(self, exit_code):
        cleanup_work_dir(getattr(self, 'work_dir', None))
        self.work_dir = None

        if exit_code != 0:
            self.log_output.append(f"\n[{t('error_title', self.lang)}] {t('error_exec_fail', self.lang)}: {exit_code}")
            self.progress_bar.setVisible(False)
            self.copy_btn.setVisible(False)
            self.run_btn.setEnabled(True)
            return

        if self.current_stage == 'run':
            parsed, _ = parse_ota_result(self.raw_output)

            if isinstance(parsed, dict) and parsed.get('raw_response'):
                json_result = parsed
            else:
                json_result = None

            update_log_url = self._extract_update_log_url(self.raw_output, json_result)
            update_log_html = self._extract_update_log_html(self.raw_output, json_result)
            update_log_value = update_log_url or ("已获取，点击右侧按钮查看" if update_log_html else "")

            self.last_result_data = parsed

            if not self.verbose_checkbox.isChecked():
                clean_result = self.format_clean_result(parsed, update_log_value)
                self.log_output.clear()
                self.log_output.append(clean_result)
                self.last_result_text = self.format_clipboard_result(parsed, update_log_url)
                self.copy_btn.setVisible(True)
            else:
                self.last_result_text = self.format_clipboard_result(parsed, update_log_url)
                self.copy_btn.setVisible(True)

            self.log_output.append("")
            self.log_output.append(t('done', self.lang))
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)
            self.current_stage = None
            self.raw_output = ""

            if update_log_url:
                self.update_log_url = update_log_url
                self.update_log_toggle_btn.setVisible(True)
            elif update_log_html:
                self.last_update_log_html = update_log_html
                self.update_log_browser.setHtml(update_log_html)
                self.last_update_log_text = self.update_log_browser.toPlainText().strip()
                self.update_log_toggle_btn.setVisible(True)
                self.last_result_text = self.format_clipboard_result(parsed, "")
