import os
import openai
import subprocess

from rich.progress import Progress, SpinnerColumn, TextColumn
from InquirerPy import prompt, inquirer

is_commitmsg_ready = False
commit_msg = ""

def check_api_key():
  openai.api_key = os.environ.get("OPENAI_API_KEY")
  if openai.api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    return None
  return openai.api_key

def get_commit_msg():
  git_staged_cmd = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE).stdout.decode("utf-8")

  if len(git_staged_cmd) == 0:
    print("No stage files to commit. Run git add to stage some files.")
    return
  is_repo = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
  if is_repo != "true":
    print("you are not in a git repository.Move to a git repository.")
    return
  output = subprocess.run(["git", "diff", "HEAD"], stdout=subprocess.PIPE).stdout.decode("utf-8")
  prompt_response = openai.Completion.create(
    model="code-davinci-002",
    prompt=f"{output}\n\n#Write a one-line commit message describing the changes",
    max_tokens=2000,
    temperature=0.0
  )
  commit_messages = prompt_response.choices[0]["text"]
  is_commitmsg_ready=True
  return commit_messages

def main():
  if check_api_key() is None:
    return None
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
  ) as progress:
    task = progress.add_task(description="Generating commit message...", total=None)
    commit_msg  = get_commit_msg()
    if(commit_msg is None):
      return
    if is_commitmsg_ready:
      progress.update(task, advance=1)
  print(f"Commit message generated: {commit_msg}")
  action  = inquirer.select(
    message="Do you want to",
    choices=[
      'Commit with AI generated message?',
      'Commit with manually entered message?',
    ],
    default=None
  ).execute()
  if action == "Commit with AI generated message?":
    print(f"AI generated commit message: ", commit_msg)
  elif action == "Commit with manually entered message?":
    commit_msg = inquirer.text(message="Enter your commit message:").execute()
    print(f"Commit message: ", commit_msg)
  subprocess.run(["git", "commit", "-m", commit_msg], input=commit_msg.encode("utf-8"))
  print("Commit operation is done!")

if __name__ == "__main__":
  main()

