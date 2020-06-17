import logging
import sys

from argparse import Namespace
from git import GitCommandError

from .github import GithubRepository, InvalidGithubConnection
from .repository import clone_repo, prepare_branch, merge_pulls, push_new_branch, add_push_remote


def executor(arguments: Namespace):
    github = prepare_github(arguments)
    repository, branch = prepare_repository(arguments.repo_dir,
                                            arguments.remote_repository,
                                            arguments.base_branch,
                                            arguments.branch,
                                            github)
    pull_requests = github.get_prs()
    merge_pulls(repository, branch, pull_requests, github)
    push_new_branch(repository, branch)


def prepare_repository(repo_dir: str,
                       remote_repository: str,
                       base_branch: str,
                       branch_name: str,
                       github: GithubRepository):
    repository = None
    try:
        repository = clone_repo(repo_dir, github.get_ssh_url())
    except GitCommandError as e:
        logging.error("Couldn't clone repository", e)
        sys.exit(-1)
    if repository is None:
        logging.error("Path %s already exists", repo_dir)
        sys.exit(-1)
    if remote_repository is not None:
        add_push_remote(repository, remote_repository)
    else:
        add_push_remote(repository, github.get_ssh_url())
    branch = prepare_branch(repository, branch_name, base_branch)
    return repository, branch


def prepare_github(arguments):
    github = GithubRepository(arguments.access_key, arguments.repository, arguments.label_name, arguments.no_comment)
    try:
        github.connect()
    except InvalidGithubConnection as e:
        logging.error("Failure while connecting to github", e)
        sys.exit(-1)
    return github
