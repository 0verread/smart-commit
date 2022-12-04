import openai_api
import os
import subprocess

api_token = os.environ.get("OPENAI_API_KEY")
if api_token is None:
  print("Please set the OPENAI_API_KEY environment variable.")


git_staged_cmd = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE)
git_staged_cmd = git_staged_cmd.stdout.decode("utf-8")

if git_staged_cmd.len() == 0:
  print("There are no staged files to commit.\nTry running git add to stage some files.")

is_repo = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE)
is_repo = is_repo.stdout.decode("utf-8").strip()

if is_repo != "true":
  print("It looks like you are not in a git repository.\nPlease run this command from the root of a git repository, or initialize one using git init.")

client = openai_api.Client.new(api_token)

output = subprocess.run(["git", "diff", "HEAD"], stdout=subprocess.PIPE)
output = output.stdout.decode("utf-8")

prompt_args = openai_api.api.CompletionArgs.builder().prompt(f"git diff HEAD\n{output}\n\n# Write a commit message describing the changes and the reasoning behind them\ngit commit -F- <<EOF")
  .engine("code-davinci-002")
  .temperature(0.0)
  .max_tokens(2000)
  .stop(["EOF"])

prompt_response = client.completions.create(prompt_args.build())

commit_message = prompt_response.get_completions()[0]["text"].strip()

subprocess.run(["git", "commit", "-F-", "<<EOF"], input=commit_message.encode("utf-8"))

print(f"Commit message generated: {commit_message}")
