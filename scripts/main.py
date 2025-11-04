import gui as gui
from gui import basicTextAnalyzer

if __name__ == "__main__":
    app = basicTextAnalyzer()
    app.app.iconbitmap("../assets/ico/basicTextAnalyser-256.ico")
    app.run()