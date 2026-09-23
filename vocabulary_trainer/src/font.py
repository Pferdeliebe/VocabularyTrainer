from PyQt6.QtGui import QFontDatabase
from qtpy import QtWidgets

class Font:
    def get_font(self, app: QtWidgets.QApplication) -> None:
        font_id = QFontDatabase.addApplicationFont(
            "../font/ComicNeue-Bold.ttf"
        )

        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)

            if font_families:
                app.setStyleSheet("""
                        QWidget {
                            font-family: "Comic Neue";
                            font-size: 18pt;
                        }
                    """)