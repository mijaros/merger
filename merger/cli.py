import argparse

import coloredlogs

from .runtime import executor


def prepare_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("merger")
    parser.add_argument('--access-key', help='Access key to github', type=str, required=True)
    parser.add_argument('--label-name', help='Label to use for merging', type=str, required=True)
    parser.add_argument('--branch', help='Branch that will be produced', type=str, required=True)
    parser.add_argument('--base-branch',
                        help='Branch to be used as base for merging, default value: master',
                        default='master')
    parser.add_argument('--remote-repository',
                        help='Optional remote repository where new branch will be published - full git_url',
                        required=False, default=None)
    parser.add_argument('--repo-dir', help="Path where repository should be checked out",
                        default="repository")
    parser.add_argument('--no-comment', help="Don't comment on pull requests, when merge not possible",
                        action='store_true')
    parser.add_argument('repository', help='Name of github repository like hello/world')
    return parser


def merger_main():
    coloredlogs.install(level='INFO')
    parser = prepare_cli()
    args = parser.parse_args()
    executor(args)


if __name__ == '__main__':
    merger_main()
