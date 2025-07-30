Git Analyzer
<p align="center">
<img src="https://placehold.co/800x400/282c34/c8ceda?text=Git+Analyzer+UI" alt="Git Analyzer Screenshot" width="700"/>
</p>

<p align="center">
<strong>A powerful desktop application to analyze your GitHub activity with AI-driven insights.</strong>
</p>

Git Analyzer helps developers gain deeper insights into their coding habits and repository history. By leveraging the GitHub API and the power of AI, this tool provides detailed analysis of your commits, activity, and code quality, helping you become a more effective and consistent developer.

Note: The graphical user interface (GUI) for this project was designed and developed with the assistance of an AI, enabling a rapid and modern development workflow.

Project Goals
The primary mission of Git Analyzer is to provide developers with actionable, AI-driven feedback. The project is centered around three core goals:

1. AI-Powered Commit Message Analysis
Good commit messages are crucial for team collaboration and project maintainability. This tool will analyze your daily commits and provide AI-generated suggestions to help you write clearer, more conventional, and more descriptive messages.

2. Comprehensive Activity Overview
Track your productivity and contributions over time. Git Analyzer will generate insightful summaries of your repository activity on a daily, monthly, and yearly basis, giving you a clear picture of what you've accomplished.

3. Intelligent Code Analysis
(Future Goal) The most ambitious goal is to integrate an AI that analyzes the actual code you've written. This feature will provide personalized tips on best practices, identify potential code smells, suggest refactoring opportunities, and help you adhere to modern coding standards.

Features
✅ Secure GitHub Connection: Connect to your GitHub account securely using a Personal Access Token.

✅ Repository Browser: Easily load and select from a list of your personal repositories.

✅ Modern, User-Friendly Interface: A clean, dark-themed UI built with Python and PyQt6.

⏳ (Planned) Daily commit summary and AI-driven message enhancement.

⏳ (Planned) Historical activity dashboards (daily, monthly, yearly).

⏳ (Planned) In-depth, AI-powered code review and suggestions.

Technology Stack
Backend: Python

GUI Framework: PyQt6

API Interaction: requests library

AI Integration: (To be implemented)

Getting Started
To get the application running on your local machine, follow these steps:

Prerequisites
Python 3.8+

A GitHub Personal Access Token with repo scope.

Installation & Execution
Clone the repository:

git clone https://github.com/your-username/git-analyzer.git
cd git-analyzer

Set up a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Run the application:

python main.py

Connect to GitHub:
Launch the application and paste your Personal Access Token directly into the input field to connect. The token is handled securely for the session and is not stored on disk.

