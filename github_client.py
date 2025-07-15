# github_client.py

import os
import datetime
from dotenv import load_dotenv
from github import Github, GithubException, UnknownObjectException

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

# Initialize PyGithub
g = Github(GITHUB_TOKEN)

def get_authenticated_user_and_repos() -> tuple[str | None, list | None]:
    """
    Fetches the authenticated user's login and all their repository objects.
    """
    print("🔎 Authenticating and fetching all your repositories...")
    try:
        user = g.get_user()
        username = user.login
        print(f"✅ Authenticated as '{username}'.")

        # Return the full repository objects
        repos = list(user.get_repos(sort='updated'))
        print(f"✅ Found {len(repos)} repositories.")
        return username, repos
    except GithubException as e:
        print(f"❌ GitHub Error: {e.data.get('message', 'Could not authenticate.')}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None, None

def get_repo_contents(repo) -> dict:
    """
    Fetches the relevant file contents of a given repository object.
    """
    print(f"   - 📂 Reading files from '{repo.name}'...")
    try:
        # Use the main branch name dynamically
        branch = repo.get_branch(repo.default_branch)
        tree = repo.get_git_tree(branch.commit.sha, recursive=True).tree
        
        file_contents = {}
        ignored_extensions = {'.md', '.txt', '.json', '.xml', '.html', '.css', '.gitignore', '.png', '.jpg', '.svg', '.gif', '.lock'}
        ignored_dirs = {'node_modules', '.git', '.vscode', '__pycache__', 'dist', 'build', 'docs'}

        for element in tree:
            if element.type == 'blob':
                file_path = element.path
                if any(part in ignored_dirs for part in file_path.split('/')) or any(file_path.endswith(ext) for ext in ignored_extensions):
                    continue
                
                # To avoid fetching huge files, we can add a size check
                if element.size > 1_000_000: # 1MB limit
                    print(f"   - ⚠️  Skipping large file: {file_path}")
                    continue
                
                file_contents[file_path] = repo.get_contents(file_path).decoded_content.decode('utf-8', 'ignore')

        print(f"   - ✅ Found {len(file_contents)} relevant code files to analyze.")
        return file_contents
    except GithubException as e:
         print(f"   - ❌ GitHub Error fetching contents: {e.data.get('message')}")
    return {}

def get_readme_info(repo):
    """Checks for an existing README.md and returns its SHA if found."""
    try:
        readme = repo.get_contents("README.md")
        return readme.sha
    except UnknownObjectException:
        # This is the expected exception when a file is not found
        return None

def has_recent_commits(repo) -> bool:
    """Checks if the repository has had commits today."""
    today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        # Get commits since the start of today
        commits = repo.get_commits(since=today_start)
        # If the count is greater than 0, there are recent commits
        if commits.totalCount > 0:
            return True
        return False
    except GithubException as e:
        print(f"   - ❌ Could not check commits for {repo.name}: {e.data.get('message')}")
        return False

def commit_readme_to_repo(repo, readme_content: str, existing_readme_sha: str | None):
    """Creates or updates the README.md file and commits it to the repository."""
    print(f"   - ✍️ Committing README.md to '{repo.name}'...")
    try:
        commit_message = "docs: Create README.md with AI assistance"
        
        if existing_readme_sha:
            # If SHA is provided, update the file
            repo.update_file(
                path="README.md",
                message="docs: Update README.md with AI assistance",
                content=readme_content,
                sha=existing_readme_sha
            )
            print(f"   - ✅ README.md updated in '{repo.name}'.")
        else:
            # Otherwise, create a new file
            repo.create_file(
                path="README.md",
                message=commit_message,
                content=readme_content
            )
            print(f"   - ✅ New README.md created in '{repo.name}'.")

    except GithubException as e:
        print(f"   - ❌ GitHub Error during commit: {e.data.get('message')}")
    except Exception as e:
        print(f"   - ❌ An unexpected error occurred during commit: {e}")
