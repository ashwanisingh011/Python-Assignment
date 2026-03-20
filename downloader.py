import instaloader
import os
from datetime import datetime

class InstagramDownloader:
    """
    A class to handle downloading photos from public Instagram profiles.
    Usage:
        downloader = InstagramDownloader()
        downloader.download_profile_photos("username")
    """
    
    def __init__(self, download_path="downloads"):
        self.loader = instaloader.Instaloader()
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def login(self, username, password):
        """Logs into Instagram to bypass restrictions."""
        try:
            self.loader.login(username, password)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def download_profile_photos(self, username, callback=None):
        """
        Downloads all public photos from the given username.
        :param username: The Instagram username to download from.
        :param callback: A function to call with status updates.
        """
        try:
            if callback: callback(f"Fetching profile: {username}...")
            
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            if profile.is_private:
                if callback: callback(f"Error: Profile '{username}' is private.")
                return False
            
            user_folder = os.path.join(self.download_path, username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            # Change directory to the user's folder for downloading
            # Instaloader by default downloads to the current working directory or a target folder
            # We will use the target parameter in download_post
            
            count = 0
            for post in profile.get_posts():
                if not post.is_video:
                    if callback: callback(f"Downloading post {count + 1}...")
                    self.loader.download_post(post, target=user_folder)
                    count += 1
            
            if callback: callback(f"Success! Downloaded {count} photos to {user_folder}.")
            return True

        except instaloader.exceptions.ProfileNotExistsException:
            if callback: callback(f"Error: Profile '{username}' does not exist.")
            return False
        except instaloader.exceptions.ConnectionException as e:
            if "401" in str(e) or "Unauthorized" in str(e):
                if "Please wait a few minutes" in str(e):
                    if callback: callback("Rate Limit: Instagram is asking to wait a few minutes before trying again.")
                else:
                    if callback: callback("Security Block: Instagram requires Login to access this profile.")
            else:
                if callback: callback(f"Network Issue: {str(e)}")
            return False
        except Exception as e:
            if callback: callback(f"Status: Stopped ({str(e)})")
            return False

if __name__ == "__main__":
    # Quick test
    downloader = InstagramDownloader()
    # Replace 'instagram' with a real public profile if testing manually
    # downloader.download_profile_photos("instagram")
