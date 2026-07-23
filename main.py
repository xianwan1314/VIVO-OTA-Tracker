#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from src.window import VivoOtaTrackerGUI, configure_high_dpi
from PyQt5.QtWidgets import QApplication


def main():
    configure_high_dpi()
    app = QApplication(sys.argv)
    window = VivoOtaTrackerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
