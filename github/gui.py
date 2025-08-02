#!/usr/bin/env python3
"""
Git Analyzer - PyQt6 GUI Application (Refined UI)
A modern, professional, and minimal interface for a GitHub analysis tool.
"""

import sys
import requests
import re
from typing import Optional, Tuple
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QMessageBox, QStatusBar,
    QFrame, QStyle, QListWidget, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# --- Import the actual logic handlers ---
try:
    # Assuming your handler files are in a 'github' directory
    from github.handler import GithubProfile, GithubRepo, GithubCommit
    from github.ai_anaylzer import analyze_commit_with_ai
except ImportError:
    print("Warning: A handler was not found. Using mock classes for GUI demonstration.")
    class GithubProfile:
        def test_github_connection(self, token): return True
        def _set_owner_name(self, token): return "mock_user"
    class GithubRepo:
        def get_user_repositories(self, token, owner): return ["mock-repo-1", "another-repo", "project-x"]
    @dataclass
    class GithubCommit:
        def get_repo_commits(self, token:str, owner:str, repo:str) -> list:
            return [
                "2023-10-27T10:00:00Z/feat: Implement user authentication",
                "2023-10-27T09:30:00Z/fix: Correct alignment on main page",
                "2023-10-26T15:20:00Z/docs: update readme",
            ]
    def analyze_commit_with_ai(commit_messages: list[str]) -> str:
        """MOCK: Simulates AI analysis of the entire commit history."""
        print("UI is pretending to analyze commit history with AI...")
        # This mock response simulates the kind of holistic feedback you'd get
        return (
            "**Overall Analysis:**\n\n"
            "The commit messages show a good adoption of the conventional commit format, which is excellent for clarity.\n\n"
            "**Strengths:**\n"
            "- Use of types like `feat`, `fix`, and `docs` is consistent.\n"
            "- Subjects are generally concise.\n\n"
            "**Areas for Improvement:**\n"
            "1.  **Capitalization:** Some subjects like 'update readme' are lowercase. For consistency, subjects should start with a capital letter.\n"
            "2.  **Clarity on Fixes:** A message like 'fix: Correct alignment on main page' is good, but could be even better by specifying *what* was aligned if it's not obvious."
        )


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
        self.github_commit = GithubCommit()

        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        """Initialize the main UI components and layout."""
        self.setWindowTitle("Git Analyzer")
        self.setMinimumSize(850, 800) # Increased height for new section
        
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
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
        self.connect_btn.setFixedWidth(120)
        self.connection_status = QLabel("❌ Not Connected")
        self.connection_status.setObjectName("statusError")
        self.connection_status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        connection_layout.addWidget(QLabel("GitHub Token:"), 0, 0)
        connection_layout.addWidget(self.token_input, 0, 1)
        connection_layout.addWidget(self.connect_btn, 0, 2)
        connection_layout.addWidget(self.connection_status, 1, 1, 1, 2)
        connection_layout.setColumnStretch(1, 1)
        main_layout.addWidget(connection_group)

        # --- Repository Selection Section ---
        self.repo_group = QGroupBox("2. Repository Selection")
        repo_layout = QVBoxLayout(self.repo_group)
        repo_layout.setSpacing(12)
        self.repo_combo = QComboBox()
        self.repo_combo.addItem("Connect to GitHub first...")
        self.repo_combo.currentIndexChanged.connect(self.on_repo_selected)
        repo_layout.addWidget(self.repo_combo)
        self.repo_group.setEnabled(False)
        main_layout.addWidget(self.repo_group)

        # --- Commit History Section ---
        self.commit_group = QGroupBox("3. Commit History")
        commit_layout = QVBoxLayout(self.commit_group)
        commit_layout.setSpacing(12)
        self.load_commits_btn = QPushButton("Load Commits")
        self.load_commits_btn.clicked.connect(self.load_commits)
        self.commit_list_widget = QListWidget()
        self.commit_list_widget.setAlternatingRowColors(True)
        commit_layout.addWidget(self.load_commits_btn)
        commit_layout.addWidget(self.commit_list_widget)
        self.commit_group.setEnabled(False)
        main_layout.addWidget(self.commit_group)
        
        # --- AI Analysis Section ---
        self.analysis_group = QGroupBox("4. AI Analysis")
        analysis_layout = QVBoxLayout(self.analysis_group)
        analysis_layout.setSpacing(12)
        
        self.analyze_commits_btn = QPushButton("Analyze All Commits")
        self.analyze_commits_btn.clicked.connect(self.run_ai_analysis)
        
        self.analysis_results_text = QTextEdit()
        self.analysis_results_text.setReadOnly(True)
        self.analysis_results_text.setPlaceholderText("AI feedback will appear here...")
        
        analysis_layout.addWidget(self.analyze_commits_btn)
        analysis_layout.addWidget(self.analysis_results_text)
        
        self.analysis_group.setEnabled(False)
        main_layout.addWidget(self.analysis_group)

        main_layout.addStretch(1)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def setup_styles(self):
        """Setup a modern, dark theme for the application using QSS."""
        self.setStyleSheet("""
            QMainWindow { background-color: #21252b; }
            QWidget {
                color: #c8ceda;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold; font-size: 15px; color: #56b6c2;
                border: 1px solid #323842; border-radius: 6px;
                margin-top: 1ex; background-color: #282c34;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 0 8px; left: 10px; background-color: #21252b;
            }
            QLabel#headerTitle {
                font-size: 24px; font-weight: 600; color: #e5c07b;
                padding: 5px 0;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 9px; border: 1px solid #323842;
                border-radius: 4px; background-color: #21252b;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border-color: #56b6c2; background-color: #2c313a;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QPushButton {
                background-color: #3e4451; border: 1px solid #4b5263;
                color: #c8ceda; padding: 9px 18px;
                border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5263; border-color: #56b6c2;
            }
            QPushButton:pressed { background-color: #323842; }
            QPushButton:disabled {
                background-color: #282c34; color: #4b5263;
                border-color: #323842;
            }
            QPushButton#connectButton {
                background-color: #56b6c2; color: #21252b;
            }
            QPushButton#connectButton:hover { background-color: #67c6d2; }
            QStatusBar {
                background-color: #282c34; border-top: 1px solid #323842;
                color: #9da5b4;
            }
            QMessageBox { background-color: #2c313a; }
            QListWidget {
                border: 1px solid #323842; border-radius: 4px;
                background-color: #21252b;
            }
            QListWidget::item { padding: 8px; }
            QListWidget::item:alternate { background-color: #2c313a; }
            QListWidget::item:selected {
                background-color: #56b6c2; color: #21252b;
            }
        """)

    def on_token_change(self, text):
        self.connect_btn.setEnabled(bool(text.strip()))

    def update_connection_status(self, message, is_success):
        self.connection_status.setText(message)
        self.connection_status.setObjectName("statusSuccess" if is_success else "statusError")
        self.connection_status.style().unpolish(self.connection_status)
        self.connection_status.style().polish(self.connection_status)
        self.connection_status.setStyleSheet("""
            QLabel#statusSuccess { color: #98c379; font-weight: bold; }
            QLabel#statusError { color: #e06c75; font-weight: bold; }
        """)
    
    def connect_to_github(self):
        token = self.token_input.text().strip()
        if not token: return
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        self.status_bar.showMessage("Attempting to connect to GitHub API...")
        QApplication.processEvents()
        try:
            if self.github_profile.test_github_connection(token):
                self.owner = self.github_profile._set_owner_name(token)
                if self.owner:
                    self.token = token
                    self.update_connection_status("✅ Connected", True)
                    self.status_bar.showMessage(f"Connected as '{self.owner}'. Loading repositories...")
                    self.repo_group.setEnabled(True)
                    self.token_input.setEnabled(False)
                    self.connect_btn.setText("Connected")
                    self.load_repositories()
                else: raise ValueError("Failed to retrieve owner name.")
            else: raise ConnectionError("Token may be invalid.")
        except Exception as e:
            self.update_connection_status("❌ Error", False)
            self.status_bar.showMessage("An error occurred during connection.")
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
            self.connect_btn.setEnabled(True)
            self.connect_btn.setText("Connect")

    def load_repositories(self):
        try:
            repos = self.github_repo.get_user_repositories(self.token, self.owner)
            self.repo_combo.clear()
            if repos:
                self.repo_combo.addItem("Select a repository...")
                self.repo_combo.addItems(sorted(repos, key=str.lower))
                self.status_bar.showMessage(f"Loaded {len(repos)} repositories.")
            else:
                self.repo_combo.addItem("No repositories found.")
                self.status_bar.showMessage("No repositories found for this account.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load repositories:\n{e}")

    def on_repo_selected(self, index):
        is_valid_repo = index > 0
        self.commit_group.setEnabled(is_valid_repo)
        self.analysis_group.setEnabled(False)
        self.commit_list_widget.clear()
        self.analysis_results_text.clear()

    def load_commits(self):
        selected_repo = self.repo_combo.currentText()
        if not selected_repo or selected_repo == "Select a repository...": return
        self.load_commits_btn.setEnabled(False)
        self.load_commits_btn.setText("Loading...")
        self.status_bar.showMessage(f"Fetching commits for {selected_repo}...")
        QApplication.processEvents()
        try:
            repo_name_only = selected_repo.split('/')[-1]
            commits = self.github_commit.get_repo_commits(self.token, self.owner, repo_name_only)
            self.commit_list_widget.clear()
            if commits:
                self.commit_list_widget.addItems(commits)
                self.status_bar.showMessage(f"Loaded {len(commits)} commits for {selected_repo}.")
                self.analysis_group.setEnabled(True)
            else:
                self.commit_list_widget.addItem("No commits found for this repository.")
                self.status_bar.showMessage("No commits found.")
                self.analysis_group.setEnabled(False)
        except Exception as e:
            self.status_bar.showMessage("Failed to load commits.")
            QMessageBox.warning(self, "Error", f"Could not load commits:\n{e}")
        finally:
            self.load_commits_btn.setEnabled(True)
            self.load_commits_btn.setText("Load Commits")

    def run_ai_analysis(self):
        """Gets all commits from the list and sends them for AI analysis."""
        commit_items = [self.commit_list_widget.item(i).text() for i in range(self.commit_list_widget.count())]
        if not commit_items or "No commits found" in commit_items[0]:
            QMessageBox.information(self, "No Commits", "There are no commits to analyze.")
            return
            
        self.analyze_commits_btn.setEnabled(False)
        self.analyze_commits_btn.setText("Analyzing...")
        self.status_bar.showMessage("Sending commits to AI for analysis...")
        QApplication.processEvents()

        # In a real app, this should be in a QThread to avoid freezing the GUI.
        try:
            analysis_result = analyze_commit_with_ai(commit_items)
            self.analysis_results_text.setText(analysis_result)
            self.status_bar.showMessage("AI analysis complete.")
        except Exception as e:
            self.status_bar.showMessage("An error occurred during AI analysis.")
            QMessageBox.critical(self, "AI Error", f"An error occurred during analysis:\n{e}")
        finally:
            self.analyze_commits_btn.setEnabled(True)
            self.analyze_commits_btn.setText("Analyze All Commits")

