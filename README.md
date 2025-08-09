# Automated GitHub Repo Creation & Project Pushing

## 📌 Overview
This Python automation script **creates GitHub repositories for multiple local projects** and **pushes them automatically** to your GitHub account.  
It’s useful when you have many local projects that haven’t been uploaded to GitHub yet — instead of manually creating repos and pushing each one, the script does it all in a loop.

---

## 🚀 Features
- **Bulk repository creation** using the GitHub REST API.
- **Automatic Git initialization** for each project.
- **Commits & pushes all code** to a newly created GitHub repo.
- **Handles GitHub API rate limits** gracefully.
- **Cross-platform path handling** via `os` and `pathlib`.

---

## 📂 Project Structure
my_projects/
├── project1/
│ ├── main.py
│ └── ...
├── project2/
│ ├── app.js
│ └── ...
└── ...
main.py

- **`my_projects/`** → contains all local projects you want to upload.  
- **`automation_script.py`** → the automation code.

---

## ⚙️ Prerequisites
1. **Python 3.7+** installed.
2. **Git** installed and added to system PATH.
3. A **GitHub Personal Access Token (PAT)** with:
   - `repo` scope (to create and push repositories).
   - `workflow` scope (optional for CI/CD).
4. All projects to push should be inside a single directory (`PROJECTS_DIR` in the script).

---

## 🔑 Setup
1. **Clone this automation repo**:
   ```bash
   git clone https://github.com/fuad-tafese-dev/Automated_github_repo_creating_and_pushing_projects.git
   cd Automated_github_repo_creating_and_pushing_projects
