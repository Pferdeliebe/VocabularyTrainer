from qtpy import QtWidgets
import sys
from font import Font
from window_controller import Controller

get_font = Font()

def main() -> None:
    """Starts the application."""
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.start()
    get_font.get_font(app)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
