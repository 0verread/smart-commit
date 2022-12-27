#!/usr/bin/env python

import os
import openai
import subprocess

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from InquirerPy import prompt, inquirer

is_commitmsg_ready = False
commit_msg = ""

prompt_questions = [
  {
    'type': 'list',
    'name': 'options',
    'message': 'Commit message is ready. what do you want to do?',
    'choices': [
      'Commit',
      'See Commit message',
      'Edit Commit Message'
    ]
  }
]

def check_api_key():
  openai.api_key = os.environ.get("OPENAI_API_KEY")
  if openai.api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    return None
  return openai.api_key

def get_commit_msg():
  git_staged_cmd = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE).stdout.decode("utf-8")

  if len(git_staged_cmd) == 0:
    print("There are no staged files to commit.\nTry running git add to stage some files.")
    return
  is_repo = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
  if is_repo != "true":
    print("It looks like you are not in a git repository.\nMake sure you are in a git repository.")
    return
  output = subprocess.run(["git", "diff", "HEAD"], stdout=subprocess.PIPE).stdout.decode("utf-8")
  prompt_response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"git diff HEAD\n{output}\n\n#Write a one line git commit message that describes the changes",
    max_tokens=1024,
    temperature=0.5
  )
  commit_messages = prompt_response.choices[0]["text"] 
  is_commitmsg_ready=True
  return commit_messages

def commit_changes():
  if(check_api_key() is None):
    return None
  commit_msg = get_commit_msg()
  return commit_msg

  # subprocess.run(["git", "commit", "-m", commit_msg], input=commit_msg.encode("utf-8"))

def main():
  commit_msg  = commit_changes()
  if(commit_msg is None):
      return
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
  ) as progress:
    task = progress.add_task(description="Generating Commit message...", total=None)
    if is_commitmsg_ready:
      progress.update(task, advance=1)
  action  = inquirer.select(
    message="Commit message is ready. what do you want to do?",
    choices=[
      'Commit',
      'See Commit message',
      'Edit Commit Message' 
    ],
    default=None
  ).execute()
  if action == "See Commit message":
    ans  = prompt(prompt_questions)
    print(f"Commit message generated: {commit_msg}")
  elif action == "Edit Commit Message":
    
  print("Done!")


if __name__ == "__main__":
  main()

