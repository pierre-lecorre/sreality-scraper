import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Read config from environment variables
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO_SREALTY")
TOKEN = os.getenv("GITHUB_TOKEN")

if not OWNER or not REPO or not TOKEN:
    raise ValueError("Please set GITHUB_OWNER, GITHUB_REPO, and GITHUB_TOKEN environment variables")

ARTIFACTS_DIR = "github_artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

headers = {"Authorization": f"token {TOKEN}"}

def get_workflow_runs():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["workflow_runs"]

def get_artifacts(run_id):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/artifacts"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["artifacts"]

def download_artifact(artifact):
    name = artifact["name"]
    artifact_id = artifact["id"]
    filename = f"{name}_{artifact_id}.zip"
    filepath = os.path.join(ARTIFACTS_DIR, filename)

    if os.path.exists(filepath):
        print(f"Artifact '{filename}' already downloaded, skipping.")
        return

    print(f"Downloading artifact '{filename}'...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts/{artifact_id}/zip"
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded '{filename}'.")

def main():
    runs = get_workflow_runs()
    for run in runs:
        run_id = run["id"]
        artifacts = get_artifacts(run_id)
        for artifact in artifacts:
            download_artifact(artifact)

if __name__ == "__main__":
    main()