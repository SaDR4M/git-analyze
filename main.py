import asyncio

from decouple import config
from icecream import ic

from github.handler import GithubProfile , GithubRepo



ACCESS_TOKEN = config("GITHUB_ACCESS_TOKEN")

user_profile = asyncio.run(GithubProfile.create(ACCESS_TOKEN))
user_name = user_profile.login
ic(user_name)
user_repos = asyncio.run(GithubRepo.create(ACCESS_TOKEN , user_name))
