#!/usr/bin/python
from trello import TrelloClient
import subprocess
import sys

def read_creds(filename):
  with open(filename, 'r') as f:
    content = f.read()
    creds = {}
    cont_spl = content.split('\n')
    for line in cont_spl:
      line_spl = line.split('=')
      if line_spl[0] is not '':
        creds[line_spl[0]] = line_spl[1]
    return creds

def get_todo_board(t_client):
  boards = t_client.list_boards()
  for board in boards:
    if board.name == "Thesis TODO":
      return board

  # If we're here, the board doesn't exist
  # so create it
  return t_client.add_board("Thesis TODO")

def get_all_todos(diss_fn):
  p = subprocess.Popen(['sed', '-n', '/TODO:/,/^$/p', diss_fn],
  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  todos = out.split('\n\n')
  todos_filtered = []
  for todo in todos:
    if todo != '':
      todos_filtered.append(todo)
  return todos_filtered

def filter_todos(todos, lists):
  filtered = []
  for todo in todos:
    found = False
    for l in lists:
      if l.name == todo:
        found = True
        break
    if not found:
      filtered.append(todo)
  return filtered

def create_new_lists(todos, todo_board):
  for todo in todos:
    todo_board.add_list(todo)

def print_help():
  print "Please provide a path to the tex file"

def main():
  if len(sys.argv) < 2:
    print_help()
    quit()

  creds = read_creds("creds.txt")
  client = TrelloClient( api_key=creds["KEY"], api_secret=creds["SECRET"],
  token=creds["oauth_token"], token_secret=creds["oauth_token_secret"])
  todo_board = get_todo_board(client)
  all_lists = todo_board.open_lists()

  todos = get_all_todos(sys.argv[1])
  fil_todos = filter_todos(todos, all_lists)
  create_new_lists(fil_todos, todo_board)


if __name__ == "__main__":
  main()

