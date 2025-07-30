from github.gui import QApplication , GitAnalyzerGUI
import sys

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Git Analyzer")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = GitAnalyzerGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()