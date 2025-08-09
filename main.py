import os
import requests
import time
from pathlib import Path

# --- Configuration ---
GITHUB_USERNAME = "fuad-tafese-dev"
GITHUB_PAT = "your_personal_access_token"  # Replace with your PAT or use environment variables
PROJECTS_DIR = r"C:\Users\fuadt\PycharmProjects\PythonProject\Automated_github_repo_creating_and_pushing_projects\my_projects"  # Use your actual path
GITHUB_API_URL = "https://api.github.com/user/repos"
# ---------------------

# Headers for API requests
headers = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}


def create_github_repo(repo_name):
    """Creates a new repository on GitHub with proper error handling."""
    payload = {
        "name": repo_name,
        "private": False,
        "auto_init": False
    }
    try:
        response = requests.post(GITHUB_API_URL, headers=headers, json=payload)

        # Handle rate limiting
        if response.status_code == 403 and 'rate limit' in response.text.lower():
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            wait_time = max(reset_time - time.time(), 0) + 5
            print(f"⏳ Rate limited. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time)
            return create_github_repo(repo_name)

        if response.status_code == 201:
            print(f"✅ Repository '{repo_name}' created successfully.")
            return True
        else:
            print(f"❌ Failed to create repository '{repo_name}': {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❗ API Error creating '{repo_name}': {str(e)[:200]}")
        return False


def push_project_to_github(project_path, repo_name):
    """Initializes git and pushes the project to the new repo with proper line ending handling."""
    original_dir = os.getcwd()
    try:
        # Sanitize repo name
        safe_repo_name = repo_name.replace(" ", "-").lower()
        abs_path = os.path.abspath(project_path)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Path not found: {abs_path}")

        os.chdir(abs_path)

        # Configure Git for Windows line endings
        os.system("git config --global core.autocrlf true")
        os.system("git config --global core.safecrlf false")

        # Initialize Git if needed
        if not os.path.exists(".git"):
            os.system("git init")
            os.system("git add .")
            os.system('git commit -m "Initial commit"')

        # Set remote and push
        remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@github.com/{GITHUB_USERNAME}/{safe_repo_name}.git"
        os.system(f"git remote add origin {remote_url}")
        os.system("git branch -M main")

        # Push with quiet flag to reduce output
        push_result = os.system("git push -u origin main --quiet")

        if push_result == 0:
            print(f"🚀 Successfully pushed '{repo_name}'")
            return True
        else:
            print(f"⚠️ Push failed for '{repo_name}' (Git error: {push_result})")
            return False

    except Exception as e:
        print(f"❗ Error pushing '{repo_name}': {str(e)[:200]}")
        return False
    finally:
        os.chdir(original_dir)


def verify_projects_directory():
    """Verify the projects directory exists and contains valid projects."""
    if not os.path.exists(PROJECTS_DIR):
        raise FileNotFoundError(f"Projects directory not found: {PROJECTS_DIR}")

    projects = [d for d in os.listdir(PROJECTS_DIR)
                if os.path.isdir(os.path.join(PROJECTS_DIR, d))
                and not d.startswith('.')]

    if not projects:
        raise ValueError(f"No valid project folders found in: {PROJECTS_DIR}")

    print(f"📁 Found {len(projects)} projects to process")
    return projects


def main():
    """Main automation workflow with proper error handling."""
    try:
        print("🔍 Verifying setup...")
        projects = verify_projects_directory()

        print("\n🚀 Starting GitHub automation...")
        for idx, project in enumerate(projects, 1):
            project_path = os.path.join(PROJECTS_DIR, project)
            print(f"\n🔄 Processing project {idx}/{len(projects)}: {project}")

            if create_github_repo(project):
                if not push_project_to_github(project_path, project):
                    print(f"⏩ Skipping due to push failure: {project}")
            time.sleep(1)  # Rate limit protection

        print("\n🎉 All projects processed successfully!")

    except Exception as e:
        print(f"\n🔥 Critical error: {str(e)[:200]}")
        print("💡 Troubleshooting tips:")
        print(f"1. Verify projects directory exists: {PROJECTS_DIR}")
        print("2. Check your GitHub PAT has 'repo' permissions")
        print("3. Ensure projects are valid directories")
    finally:
        print("\n🏁 Script execution complete.")


if __name__ == "__main__":
    # Initial verification
    print(f"Python version: {os.sys.version}")
    print(f"Projects directory: {PROJECTS_DIR}")
    print(f"Directory exists: {os.path.exists(PROJECTS_DIR)}")

    main()