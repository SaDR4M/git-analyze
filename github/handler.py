import requests
# third party
import asyncio
import aiohttp
from decouple import config
from icecream import ic
from typing import Optional , Literal , Iterator
from dataclasses import dataclass
# local
from github.urls import (
    GITHUB_COMMIT_URL,
    GITHUB_USER_URL,
    GITHUB_USERS_REPO_URL
)

    
class GithubProfile:
    
    def _set_owner_name(self , token:str) -> str | None :
        """Set owner name to fetch further data"""
        try :
            response = requests.get(
                url=GITHUB_USER_URL, 
                headers =  {
                    "Authorization" : f"Bearer {token}"
                },
                params = {
                    "type" : "all"
                }
            )
            if response.status_code == 200 :
                data = response.json()
                owner_name = data.get("login" , None)
                
                if owner_name is None :
                    raise ValueError("Owner cannot be None , Failed to fetch user's name")
                
                setattr(self , "owner" , owner_name)
    
                return owner_name
            else :
                return None
            
        except Exception as e :
            raise e
        
                
    def test_github_connection(self, token:str) -> bool :
        """test connection with the user token"""
        try :
            response = requests.get(
                url=GITHUB_USER_URL, 
                headers =  {
                    "Authorization" : f"Bearer {token}"
                },
                params = {
                    "type" : "all"
                }
            )
            if response.status_code == 200 :
                return True
            else :
                return False
            
        except Exception as e :
            raise e
        

    @property
    def get_owner(self) -> str:
        return self.owner

@dataclass
class GithubRepo :
    page : int = 1
    per_page : int = 30
    
    def get_user_repositories(self , token:str , owner:str , page: Optional[int] = None , per_page : Optional[int] = None ) -> Iterator[str]:    
        """Fetch user's repoistory list then pass to another function to set needed attrs"""
        page_number =  page if page is not None else self.page,
        per_page_number = per_page if per_page is not None else self.per_page
        # Avoid getting more than 30 for single page repo
        
        if per_page_number > 30 :
            raise ValueError("Maximum repos to fetch in single page is 30") 
        
        response = requests.get(
            url = GITHUB_USERS_REPO_URL.format(),
            headers ={
            "Authorization" : f"Bearer {token}",
            },
            params =  {
                "page" : page_number,
                "per_page" : per_page_number
            }
        )
        
        repo_list = [
            f"{owner}/{repo.get('name', '').lower()}"
            for repo in response.json()
        ] if response.status_code == 200 else []
        ic(repo_list)
        return repo_list
    
class GithubCommit:
    pass
    
    
