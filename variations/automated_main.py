# main.py

from github_client import (
    get_authenticated_user_and_repos, 
    get_repo_contents, 
    get_readme_info, 
    has_recent_commits, 
    commit_readme_to_repo
)
from ai_generator import generate_readme

def main():
    """
    Main function to run the automated README generation and update process.
    """
    print("======================================================")
    print("🤖 Starting Automated AI-Powered README Documentation")
    print("======================================================")

    _username, repos = get_authenticated_user_and_repos()
    if not repos:
        print("No repositories found or failed to authenticate. Exiting.")
        return

    for repo in repos:
        print(f"\nProcessing Repository: {repo.full_name}")
        
        # Check if the repository is archived or empty
        if repo.archived:
            print("   - ⏩ Skipping archived repository.")
            continue
        if repo.size == 0:
            print("   - ⏩ Skipping empty repository.")
            continue

        existing_readme_sha = get_readme_info(repo)
        
        should_generate = False
        if not existing_readme_sha:
            print("   - ℹ️ No README.md found.")
            should_generate = True
        else:
            print("   - ℹ️ README.md found. Checking for recent code changes...")
            if has_recent_commits(repo):
                print("   - 🔄 Recent commits detected.")
                should_generate = True
            else:
                print("   - ✅ No recent changes. README is up-to-date.")

        if should_generate:
            print("   - 🚀 Proceeding with README generation...")
            file_contents = get_repo_contents(repo)
            
            if not file_contents:
                print("   - ⚠️ No code files found to analyze. Skipping README generation.")
                continue

            readme_content = generate_readme(repo.name, file_contents)
            
            # Commit the new or updated README to the repository
            commit_readme_to_repo(repo, readme_content, existing_readme_sha)

    print("\n======================================================")
    print("🎉 Automated README process completed for all repositories.")
    print("======================================================")

if __name__ == "__main__":
    main()
