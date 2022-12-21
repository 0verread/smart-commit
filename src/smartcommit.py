import openai
import os
import subprocess

openai.api_key = os.environ.get("OPENAI_API_KEY")

def check_api_key():
  openai.api_key = os.environ.get("OPENAI_API_KEY")
  if openai.api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    return

check_api_key()

git_staged_cmd = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE)
git_staged_cmd = git_staged_cmd.stdout.decode("utf-8")

if len(git_staged_cmd) == 0:
  print("There are no staged files to commit.\nTry running git add to stage some files.")

is_repo = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE)
is_repo = is_repo.stdout.decode("utf-8").strip()

if is_repo != "true":
  print("It looks like you are not in a git repository.\nPlease run this command from the root of a git repository, or initialize one using git init.")

output = subprocess.run(["git", "diff", "HEAD"], stdout=subprocess.PIPE)
output = output.stdout.decode("utf-8")

prompt_response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"git diff HEAD\n{output}\n\n# Please generate a commit message describing the changes",
    max_tokens=1024,
    temperature=0.5
)
commit_messages = prompt_response.choices[0]["text"]

# subprocess.run(["git", "commit", "-m", commit_messages], input=commit_messages.encode("utf-8"))

print(f"Commit message generated: {commit_messages}")

# generate_git_commit():


# # if __name__ = "__main__":
# #   generate_git_commit