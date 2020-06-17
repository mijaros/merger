import logging

from git import Repo, GitCommandError, Head
from pathlib import Path
from typing import List, Optional

from .github import GithubRepository


def clone_repo(path: str, ssh_url: str) -> Optional[Repo]:
    p = Path(path)
    if p.exists():
        return None
    result = Repo.clone_from(ssh_url, p.as_posix())
    return result


def prepare_branch(repo: Repo, branch_name: str, base_branch: str) -> Head:
    if branch_name in repo.remote('up_remote').refs:
        repo.remote('up_remote').push(refspec=f':{branch_name}')
    if branch_name in repo.heads:
        branch = repo.heads[branch_name]
        repo.delete_head(branch)
    base_head = repo.heads[base_branch]
    head = repo.create_head(branch_name, base_head)
    repo.head.reference = head
    return head


def merge_pulls(repo: Repo, branch: Head, pull_numbers: List[int], upstream: GithubRepository):
    for id in pull_numbers:
        fetch = repo.remote('origin').fetch(f'pull/{id}/head')[0]
        fetch_head = repo.create_head(f'pull-{id}', fetch)
        merge_base = repo.merge_base(branch, fetch_head)
        try:
            repo.index.merge_tree(fetch_head, base=merge_base)
        except GitCommandError as err:
            logging.warning("Merge of %d failed with message %s", id, err)
            upstream.comment_failed_merge(id, err)
            continue
        repo.index.commit(f'Merge pr #{id} into {branch.name}',
                          parent_commits=(branch.commit, fetch_head.commit))


def add_push_remote(repo: Repo, remote_url: str):
    repo.create_remote('up_remote', remote_url)
    repo.remote('up_remote').fetch()


def push_new_branch(repo: Repo, branch: Head):
    repo.remote('up_remote').push(branch)


