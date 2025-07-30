#!/usr/bin/env python3
"""
Git Analyzer - PyQt6 GUI Application (Clean Version)
Connection and Repository Loading Only
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from github.handler import GithubProfile, GithubRepo

class GitAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.token = None
        self.owner = None
        self.github_profile = GithubProfile()
        self.github_repo = GithubRepo()
        self.init_ui()
        self.setup_styles()
    
    def init_ui(self):
        self.setWindowTitle("Git Analyzer - GitHub Repository Analysis Tool")
        self.setGeometry(100, 100, 800, 400)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to connect to GitHub")
        
        # GitHub Connection Section
        connection_group = QGroupBox("GitHub Connection")
        connection_layout = QVBoxLayout(connection_group)
        
        # Token input row
        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("GitHub Token:"))
        
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter your GitHub Personal Access Token")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        token_layout.addWidget(self.token_input)
        
        self.connect_btn = QPushButton("Connect to GitHub")
        self.connect_btn.clicked.connect(self.connect_to_github)
        token_layout.addWidget(self.connect_btn)
        
        connection_layout.addLayout(token_layout)
        
        # Connection status
        self.connection_status = QLabel("❌ Not connected")
        self.connection_status.setStyleSheet("color: red; font-weight: bold;")
        connection_layout.addWidget(self.connection_status)
        
        main_layout.addWidget(connection_group)
        
        # Repository Selection Section
        repo_group = QGroupBox("Repository Selection")
        repo_layout = QVBoxLayout(repo_group)
        
        # Load repositories button
        self.load_repos_btn = QPushButton("Load My Repositories")
        self.load_repos_btn.clicked.connect(self.load_repositories)
        self.load_repos_btn.setEnabled(False)
        repo_layout.addWidget(self.load_repos_btn)
        
        # Repository dropdown
        repo_selection_layout = QHBoxLayout()
        repo_selection_layout.addWidget(QLabel("Select Repository:"))
        
        self.repo_combo = QComboBox()
        self.repo_combo.setMinimumWidth(400)
        self.repo_combo.addItem("Connect to GitHub first...")
        self.repo_combo.setEnabled(False)
        repo_selection_layout.addWidget(self.repo_combo)
        
        repo_layout.addLayout(repo_selection_layout)
        
        main_layout.addWidget(repo_group)
        
        # Add stretch to push everything to top
        main_layout.addStretch()
    
    def setup_styles(self):
        """Setup application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4CAF50;
            }
            QLabel {
                font-size: 14px;
            }
        """)
    
    def connect_to_github(self):
        """Handle GitHub connection"""
        token = self.token_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, "Warning", "Please enter a GitHub token")
            return
        
        # Disable button during connection
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        self.status_bar.showMessage("Connecting to GitHub...")
        
        # TODO: You will implement this function
        success = self.github_profile.test_github_connection(token)
        
        if success:
            self.connection_status.setText("✅ Connected to GitHub")
            self.connection_status.setStyleSheet("color: green; font-weight: bold;")
            self.load_repos_btn.setEnabled(True)
            self.status_bar.showMessage("Successfully connected to GitHub API")
            self.token = token  # Store the token
            self.owner = self.github_profile._set_owner_name(token)
        else:
            self.connection_status.setText("❌ Connection failed")
            self.connection_status.setStyleSheet("color: red; font-weight: bold;")
            self.status_bar.showMessage("Failed to connect to GitHub")
            QMessageBox.critical(self, "Connection Error", "Failed to connect to GitHub. Please check your token.")
        
        # Re-enable button
        self.connect_btn.setEnabled(True)
        self.connect_btn.setText("Connect to GitHub")
    
    def load_repositories(self):
        """Load user repositories"""
        self.load_repos_btn.setEnabled(False)
        self.load_repos_btn.setText("Loading Repositories...")
        self.status_bar.showMessage("Loading your repositories...")
        
        # TODO: You will implement this function
        repos = self.github_repo.get_user_repositories(self.token, self.owner)
        
        if repos:
            # Clear combo box and add repositories
            self.repo_combo.clear()
            self.repo_combo.addItem("Select a repository...")
            
            # Add each repository to combo box
            for repo in repos:
                self.repo_combo.addItem(repo)
            
            self.repo_combo.setEnabled(True)
            self.status_bar.showMessage(f"Loaded {len(repos)} repositories")
        else:
            self.repo_combo.clear()
            self.repo_combo.addItem("No repositories found")
            self.status_bar.showMessage("No repositories found")
        
        # Re-enable button
        self.load_repos_btn.setEnabled(True)
        self.load_repos_btn.setText("Load My Repositories")