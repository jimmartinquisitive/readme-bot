# main.py

import os
from github_client import get_authenticated_user_info, get_repo_contents, commit_readme_to_repo
from ai_generator import generate_readme

def main():
    """Main function to run the README generation tool."""
    print("=============================================")
    print("🤖 Welcome to the AI-Powered README Generator")
    print("=============================================")

    username, repos = get_authenticated_user_info()
    if username is None or repos is None:
        print("Could not fetch repository information. Exiting.")
        return
    if not repos:
        return

    print("\nAvailable Repositories:")
    for i, repo_name in enumerate(repos):
        print(f"  [{i + 1}] {repo_name}")

    try:
        choice = int(input("\nSelect a repository by number: ")) - 1
        if not 0 <= choice < len(repos):
            print("❌ Invalid selection.")
            return
        repo_name = repos[choice]
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    print(f"\n🚀 Starting process for repository: {repo_name}")

    file_contents = get_repo_contents(username, repo_name)
    if not file_contents:
        print("Could not retrieve file contents. Aborting.")
        return

    readme_content = generate_readme(repo_name, file_contents)

    # NEW: Confirmation step before committing to GitHub
    print("\n--- Generated README.md Preview ---")
    print(readme_content[:500] + "..." if len(readme_content) > 500 else readme_content)
    print("---------------------------------")
    
    confirm = input(f"Do you want to commit this README.md to the '{repo_name}' repository? (y/n): ").lower().strip()

    if confirm == 'y':
        commit_readme_to_repo(username, repo_name, readme_content)
        print("\n=============================================")
        print(f"🎉 Success! README committed to GitHub repository.")
        print("=============================================")
    else:
        # Save locally as a fallback if the user says no
        output_filename = f"README_{repo_name}.md"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("\n- Operation cancelled by user.")
        print(f"- README saved locally as: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    main()
