import openai
import os
import subprocess

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
  print("Please set the OPENAI_API_KEY environment variable.")
  

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

# prompt_args = openai.CompletionArgs.builder().prompt(f"git diff HEAD\n{output}\n\n# Write a commit message describing the changes and the reasoning behind them\ngit commit -F- <<EOF").engine("code-davinci-002").temperature(0.0).max_tokens(2000).stop(["EOF"])

prompt_response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"git diff HEAD\n{output}\n\n# Please generate a commit message describing the changes\ngit commit -F- <<EOF",
    max_tokens=1024,
    temperature=0.5
)
commit_messages = prompt_response.choices[0]["text"]
# print(commit_messages)
# commit_message = prompt_response.get_completions()[0]["text"].strip()

subprocess.run(["git", "commit", "-m", "<<EOF"], input=commit_messages.encode("utf-8"))

print(f"Commit message generated: {commit_messages}")
