from github import Github, Repository, BadCredentialsException, UnknownObjectException, Label, PullRequest
from git import GitCommandError
from typing import Optional, List
from operator import itemgetter
import logging


MESSAGE = """
__The merge of this issue failed.__

Command that caused the error `{0}`
Standard output of git command:

```
{1}```

Error output of git command:

```
{2}```
"""


class InvalidGithubConnection(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GithubRepository:
    def __init__(self, access_key: str, repo_name: str, label: str, no_comment=True):
        self.repo_name: str = repo_name
        self.access_key: str = access_key
        self.label: str = label
        self.no_comment: bool = no_comment
        self.github: Repository = None

    def connect(self):
        self.github = initialize_connection(self.access_key, self.repo_name)
        logging.info("Connecting to github.")
        if self.github is None:
            raise InvalidGithubConnection(f"Connection to github was not initiated.")

    def get_prs(self) -> Optional[List[int]]:
        return get_pull_requests_with_label(self.github, self.label)

    def comment_failed_merge(self, pr_id: int, error: GitCommandError):
        if self.no_comment:
            logging.info('Skipping commenting failed mr, no comment was set.')
            return
        pull_request = None
        for pr in self.github.get_pulls():
            if pr.number == pr_id:
                pull_request = pr
                break
        if pull_request is None:
            logging.warning("Pull request %d not found, not commenting", pr_id)
            return

        pull_request.create_issue_comment(MESSAGE.format(' '.join(error.command), error.stdout, error.stderr))

    def get_ssh_url(self):
        return self.github.ssh_url


def initialize_connection(access_key: str, repo_name: str) -> Optional[Repository.Repository]:
    gh = Github(access_key)
    try:
        gh.get_user().bio
    except BadCredentialsException as e:
        logging.error(e)
        return None

    repo = None
    try:
        repo = gh.get_repo(repo_name)
    except UnknownObjectException as exception:
        logging.error(exception)
        return None
    return repo


def _find_label_by_name(labels: List[Label.Label], name: str) -> bool:
    for k in labels:
        if name == k.name:
            return True
    return False


def get_pull_requests_with_label(repo: Repository.Repository, label: str) -> List[int]:
    pull_requests = repo.get_pulls(state='open')
    pull_ids = {}
    for pr in pull_requests:
        labels = [k for k in pr.get_labels()]
        if _find_label_by_name(labels, label):
            pull_ids[pr.number] = sorted(
                [j.created_at for j in pr.get_issue_events() if j.event == 'labeled' and j.label.name == label])[-1]
    sorted_pulls = sorted(pull_ids.items(), key=itemgetter(1))
    return [k[0] for k in sorted_pulls]
