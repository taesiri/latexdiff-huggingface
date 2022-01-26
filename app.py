import gradio as gr
import git
import tempfile
import shutil
import subprocess
import os

cwd = os.getcwd()
gcounter = 1000

def generate_git(OldVersion, NewVersion, tmp_dir_name):
  new_repo = git.Repo.init(tmp_dir_name)
  with new_repo.config_writer() as git_config:
    git_config.set_value('user', 'email', 'latexdiff@latexdiff.latexdiff')
    git_config.set_value('user', 'name', 'git Latex Diff')

  shutil.unpack_archive(OldVersion.name, tmp_dir_name)

  new_repo.index.add('*')
  new_repo.index.commit('Initial commit.')

  shutil.unpack_archive(NewVersion.name, tmp_dir_name)

  new_repo.index.add('*')
  new_repo.index.commit('Changes')

def generate_diff(tmp_dir_name):
  subprocess.check_call([f'{cwd}/git-latexdiff',  'HEAD~1', '--cleanup', 'keeppdf', '-o', 'mydiff.pdf'], cwd=tmp_dir_name)

def gen_all(OldVersion, NewVersion):
  global gcounter
  gcounter+=1

  dirpath = tempfile.mkdtemp()
  fake_git_name = 'something'
  generate_git(OldVersion, NewVersion, dirpath)
  generate_diff(dirpath)
  shutil.move(f'{dirpath}/mydiff.pdf', f'{cwd}/results/{gcounter}.pdf')
  shutil.rmtree(dirpath)

  return f'{cwd}/results/{gcounter}.pdf'

os.makedirs('results', exist_ok=True)

title = "Latex Diff"
description = "This Space automatically generates LatexDiff for two different versions of your latex project."
article = "<p style='text-align: center'><a href='https://gitlab.com/git-latexdiff/git-latexdiff' target='_blank'>Git LatexDiff GitLab Repo</a></p>"


iface = gr.Interface(gen_all, 
                    ["file", "file"], "file",
                    allow_screenshot=False, allow_flagging=False, 
                    title=title,
                    description=description,
                    article=article,
                    examples=[['1.zip','2.zip']])
iface.launch(enable_queue=True)
