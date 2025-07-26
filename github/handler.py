import requests
# third party
import asyncio
import aiohttp
from decouple import config
from icecream import ic
# local
from github.urls import (
    GITHUB_COMMIT_URL,
    GITHUB_USER_URL,
    GITHUB_USERS_REPO_URL
)

ACCESS_TOKEN = config("GITHUB_ACCESS_TOKEN")

class GithubProfile:
    def __init__(self , token) :
        self.token = token
        self.headers =  {
            "Authorization" : f"Bearer {ACCESS_TOKEN}"
        }
        
        self.avatar_url = None
        self.followers = None
        self.following = None
        self.name = None
        self.user_name = None
        self.allowed_attrs = None
    
    @classmethod
    async def create(cls , token:str) :
        """Factory class to create profile instance"""
        ic(token)
        user = cls(token)
        await user._fetch_user_data()
        return user
        
    async def _fetch_user_data(self) -> dict :
        """Fetch user's profile data then pass it to another function to set needed attrs"""
        async with aiohttp.ClientSession() as session :
            
            async with session.get(
                url = GITHUB_USER_URL,
                headers = self.headers,
                params = {
                    "type" : "all"
                }
            ) as response :
                
                if response.status == 200 :
                    data = await response.json()
                    self._set_attributes(**data)
                else :
                    raise aiohttp.BadContentDispositionParam
                 
    def _set_attributes(self , **kwargs) :
        """set user's profile attribute"""
        allowed_attrs = ["avatar_url" , "followers" , "following" , "name" , "login" , "allowed_attrs"]
        for key,value in kwargs.items() :
            if key in allowed_attrs :
                setattr(self , key , value)
                

    
class GithubRepo :
    def __init__(self , token:str , login:str) :
        self.token = token
        self.login = login
        self.header =  {
            "Authorization" : f"Bearer {ACCESS_TOKEN}",
        }
        self.params = {
            "page" : 1,
            "per_page" : 30
        }
        
    @classmethod
    async def create(cls , token:str, login:str) :
        """Factory class to create repo instance"""
        repo = cls(token , login)
        await repo._fetch_user_repos()
        return repo
        
        
    async def _fetch_user_repos(self) -> dict:    
        """Fetch user's repoistory list then pass to another function to set needed attrs"""
        async with aiohttp.ClientSession() as session :    
            
            async with session.get(
                url = GITHUB_USERS_REPO_URL.format(),
                headers = self.header,
                params = self.params
            ) as response :
                if response.status == 200 :
                    data = await response.json()
                    ic(data)
                    repo_list = []
                    for repo in data :
                        repo_list.append(
                            dict(name=repo.get("name"))
                        )
                    ic(repo_list)
                    # self._set_attributes(**response_json)
                else :
                    raise aiohttp.BadContentDispositionParam
                
            
    def _set_attributes(self , **kwargs) :
        pass
        
    
# class GithubCommit:
#     def __init__(self):
#         self.header = {
#             "Authorization" : f"Bearer {ACCESS_TOKEN}"
#         }
        
#     async def get_latest_commits(self , owner:str , repo:str) -> dict:
#         print(GITHUB_COMMIT_URL)
#         response = requests.get(
#             url=GITHUB_COMMIT_URL.format(owner=owner , repo=repo),
#             headers=self.header,
#             # TODO add since or until
#             params = {
#                 "page" : 1,
#                 "per_page" : 100,
#             }
#         )
#         response_json = response.json()
#         full_data = [{"commit"  : commit["commit"]["message"]} for commit in response_json]
#         print(full_data)
#         return None
        