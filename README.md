# 🤖 Git Analyzer: Your AI-Powered GitHub Activity Companion

---

Hey there! If you're anything like me, you've probably wondered about your own coding habits. How often do you commit? Are those commit messages actually useful? That's exactly why I built **Git Analyzer** – a little desktop app that uses AI to help me (and hopefully you!) get a better handle on our GitHub activity.

This is a personal project, really focused on learning how to dig into my own coding patterns. Fun fact: even the app's look and feel (the GUI) got some design help from AI!

## 🎯 What It Does

Here's what Git Analyzer can help you with:

* **Analyze Commit Messages:** Get tips on how to write better, clearer commits.
* **See an Activity Overview:** Track what I've accomplished daily, monthly, or yearly.
* **(Future Goal) Get Code Feedback:** Eventually, I'd love to have the AI analyze my code and suggest improvements and best practices.

## 🛠️ Tech Stack

| Category         | Technology    |
| :--------------- | :------------ |
| **GUI Framework** | PyQt5         |
| **AI Integration** | OpenAI API    |
| **Backend Logic** | Python        |

## 🚀 How to Run It

Getting Git Analyzer up and running is pretty straightforward:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/git-analyzer.git](https://github.com/your-username/git-analyzer.git)
    cd git-analyzer
    ```

2.  **Install Requirements:**
    Using a virtual environment is always a good idea here:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    ```bash
    python main.py
    ```

4.  **Connect to GitHub:**
    When the app opens, you'll need to link it to your GitHub account using a **GitHub Personal Access Token**. Just paste your token into the app. Don't worry, it's only used for that session and isn't stored anywhere.

---

I'm pretty excited about where Git Analyzer is headed and plan to add even more AI smarts down the line. If you check it out, feel free to poke around the code, give me some feedback, or even jump in and contribute!
