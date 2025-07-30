#!/usr/bin/env python3
"""
Git Analyzer - PyQt6 GUI Application (Refined UI)
A modern, professional, and minimal interface for a GitHub analysis tool.
"""

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QMessageBox, QStatusBar,
    QFrame, QStyle
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# --- Import the actual logic handlers ---
# 1. FIXED: Corrected the import path from 'handler.github' to 'github.handler'.
try:
    from github.handler import GithubProfile, GithubRepo
except ImportError:
    # Provide a fallback for GUI development if the handler is not found
    print("Warning: 'github.handler' not found. Using mock classes for GUI demonstration.")
    class GithubProfile:
        def test_github_connection(self, token): return False
        def _set_owner_name(self, token): return "mock_user"
    class GithubRepo:
        def get_user_repositories(self, token, owner): return ["mock-repo-1", "mock-repo-2"]


# --- Main Application ---
class GitAnalyzerGUI(QMainWindow):
    """
    The main window for the Git Analyzer application.
    Features a refined dark theme and a more minimal user interface.
    """
    def __init__(self):
        super().__init__()
        self.token = None
        self.owner = None
        # Initialize the actual handlers
        self.github_profile = GithubProfile()
        self.github_repo = GithubRepo()

        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        """Initialize the main UI components and layout."""
        self.setWindowTitle("Git Analyzer")
        # UI-FIX: Set a minimum size instead of a fixed one for better resizing.
        self.setMinimumSize(850, 550)
        
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # UI-FIX: Adjusted margins and spacing for a cleaner look.
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(18)

        # --- Header ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Git Analyzer")
        title_label.setObjectName("headerTitle")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # --- GitHub Connection Section ---
        connection_group = QGroupBox("1. GitHub Connection")
        connection_layout = QGridLayout(connection_group)
        connection_layout.setSpacing(12)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter your GitHub Personal Access Token")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.textChanged.connect(self.on_token_change)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setObjectName("connectButton")
        self.connect_btn.clicked.connect(self.connect_to_github)
        self.connect_btn.setEnabled(False)
        # UI-FIX: Set a fixed width for the button to prevent it from stretching oddly.
        self.connect_btn.setFixedWidth(120)

        self.connection_status = QLabel("❌ Not Connected")
        self.connection_status.setObjectName("statusError")
        self.connection_status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        connection_layout.addWidget(QLabel("GitHub Token:"), 0, 0)
        connection_layout.addWidget(self.token_input, 0, 1)
        connection_layout.addWidget(self.connect_btn, 0, 2)
        # UI-FIX: Placed status label on its own row to provide more space.
        connection_layout.addWidget(self.connection_status, 1, 1, 1, 2)
        connection_layout.setColumnStretch(1, 1) # Ensure token input takes up available space.


        main_layout.addWidget(connection_group)

        # --- Repository Selection Section ---
        self.repo_group = QGroupBox("2. Repository Selection")
        repo_layout = QVBoxLayout(self.repo_group)
        repo_layout.setSpacing(12)

        self.load_repos_btn = QPushButton("Load My Repositories")
        self.load_repos_btn.clicked.connect(self.load_repositories)

        self.repo_combo = QComboBox()
        self.repo_combo.addItem("Connect to GitHub first...")
        
        repo_layout.addWidget(self.load_repos_btn)
        repo_layout.addWidget(self.repo_combo)

        self.repo_group.setEnabled(False)
        main_layout.addWidget(self.repo_group)

        # --- Analysis Section (Placeholder) ---
        self.analysis_group = QGroupBox("3. Analysis")
        analysis_layout = QVBoxLayout(self.analysis_group)
        placeholder_label = QLabel("Analysis results will appear here.")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label.setObjectName("placeholderLabel")
        analysis_layout.addWidget(placeholder_label)
        self.analysis_group.setEnabled(False)
        main_layout.addWidget(self.analysis_group)

        main_layout.addStretch(1)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def setup_styles(self):
        """Setup a modern, dark theme for the application using QSS."""
        # UI-FIX: Refined the entire stylesheet for a more minimal and modern aesthetic.
        self.setStyleSheet("""
            QMainWindow {
                background-color: #21252b;
            }
            QWidget {
                color: #c8ceda;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 15px;
                color: #56b6c2; /* Teal accent */
                border: 1px solid #323842;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #282c34;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                left: 10px;
                background-color: #21252b;
            }
            QLabel#headerTitle {
                font-size: 24px;
                font-weight: 600; /* Semibold */
                color: #e5c07b;
                padding: 5px 0;
            }
            QLabel#placeholderLabel {
                color: #4b5263;
                font-style: italic;
                font-size: 16px;
                padding: 20px;
            }
            QLineEdit, QComboBox {
                padding: 9px;
                border: 1px solid #323842;
                border-radius: 4px;
                background-color: #21252b;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #56b6c2;
                background-color: #2c313a;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QPushButton {
                background-color: #3e4451;
                border: 1px solid #4b5263;
                color: #c8ceda;
                padding: 9px 18px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5263;
                border-color: #56b6c2;
            }
            QPushButton:pressed {
                background-color: #323842;
            }
            QPushButton:disabled {
                background-color: #282c34;
                color: #4b5263;
                border-color: #323842;
            }
            QPushButton#connectButton {
                background-color: #56b6c2; /* Teal accent for primary action */
                color: #21252b;
            }
            QPushButton#connectButton:hover {
                background-color: #67c6d2;
            }
            QStatusBar {
                background-color: #282c34;
                border-top: 1px solid #323842;
                color: #9da5b4;
            }
            QMessageBox {
                 background-color: #2c313a;
            }
        """)

    def on_token_change(self, text):
        """Enable or disable the connect button based on token input."""
        self.connect_btn.setEnabled(bool(text.strip()))

    def update_connection_status(self, message, is_success):
        """Helper to update the connection status label style and text."""
        self.connection_status.setText(message)
        self.connection_status.setObjectName("statusSuccess" if is_success else "statusError")
        self.connection_status.style().unpolish(self.connection_status)
        self.connection_status.style().polish(self.connection_status)
        self.connection_status.setStyleSheet("""
            QLabel#statusSuccess { color: #98c379; font-weight: bold; }
            QLabel#statusError { color: #e06c75; font-weight: bold; }
        """)

    def connect_to_github(self):
        """Handle the logic for connecting to the GitHub API."""
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Input Required", "Please enter a GitHub token.")
            return

        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        self.status_bar.showMessage("Attempting to connect to GitHub API...")
        QApplication.processEvents()

        try:
            success = self.github_profile.test_github_connection(token)
            if success:
                self.owner = self.github_profile._set_owner_name(token)
                if self.owner:
                    self.token = token
                    self.update_connection_status("✅ Connected", True)
                    self.status_bar.showMessage(f"Successfully connected as '{self.owner}'.")
                    self.repo_group.setEnabled(True)
                    self.token_input.setEnabled(False)
                    self.connect_btn.setText("Connected")
                else:
                    raise ValueError("Failed to retrieve owner name from token.")
            else:
                self.update_connection_status("❌ Connection Failed", False)
                self.status_bar.showMessage("Connection failed. The token may be invalid.")
                QMessageBox.critical(self, "Connection Error", "Failed to connect. Please verify your token.")
                self.connect_btn.setEnabled(True)
                self.connect_btn.setText("Connect")

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error during connection: {e}")
            self.update_connection_status("❌ Error", False)
            self.status_bar.showMessage("An error occurred during connection.")
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
            self.connect_btn.setEnabled(True)
            self.connect_btn.setText("Connect")

    def load_repositories(self):
        """Fetch and display the user's repositories in the combo box."""
        self.load_repos_btn.setEnabled(False)
        self.load_repos_btn.setText("Loading...")
        self.status_bar.showMessage("Fetching your repositories from GitHub...")
        QApplication.processEvents()

        try:
            repos = self.github_repo.get_user_repositories(self.token, self.owner)
            if repos:
                self.repo_combo.clear()
                self.repo_combo.addItem("Select a repository to analyze...")
                self.repo_combo.addItems(sorted(repos, key=str.lower))
                self.status_bar.showMessage(f"Successfully loaded {len(repos)} repositories.")
                self.analysis_group.setEnabled(True)
            else:
                self.repo_combo.clear()
                self.repo_combo.addItem("No repositories found or error occurred.")
                self.status_bar.showMessage("Could not find any repositories for this account.")
        
        except Exception as e:
            print(f"Error loading repositories: {e}")
            self.status_bar.showMessage("Failed to load repositories.")
            QMessageBox.warning(self, "Error", f"Could not load repositories:\n{e}")

        finally:
            self.load_repos_btn.setEnabled(True)
            self.load_repos_btn.setText("Reload Repositories")
