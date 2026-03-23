import instaloader
import os
import time
import random
from datetime import datetime

class InstagramDownloader:
    """
    A class to handle downloading photos from public Instagram profiles.
    Usage:
        downloader = InstagramDownloader()
        downloader.download_profile_photos("username")
    """
    
    def __init__(self, download_path="downloads", sessions_path=".sessions"):
        self.loader = instaloader.Instaloader()
        self.download_path = download_path
        self.sessions_path = sessions_path
        
        # Ensure directories exist
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        if not os.path.exists(self.sessions_path):
            os.makedirs(self.sessions_path, mode=0o700) # Private directory
        
        self.current_user = None
        self._load_last_session()

    def _save_session(self, username):
        """Saves the current session to a file."""
        try:
            session_file = os.path.join(self.sessions_path, f"session-{username}")
            self.loader.save_session_to_file(session_file)
            # Also save the last username used
            with open(os.path.join(self.sessions_path, "last_user.txt"), "w") as f:
                f.write(username)
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def _load_last_session(self):
        """Attempts to load the last used session."""
        last_user_file = os.path.join(self.sessions_path, "last_user.txt")
        if os.path.exists(last_user_file):
            try:
                with open(last_user_file, "r") as f:
                    username = f.read().strip()
                session_file = os.path.join(self.sessions_path, f"session-{username}")
                if os.path.exists(session_file):
                    self.loader.load_session_from_file(username, session_file)
                    self.current_user = username
                    print(f"Loaded session for {username}")
            except Exception as e:
                print(f"Error loading session: {e}")

    def login(self, username, password):
        """Logs into Instagram and saves the session."""
        try:
            self.loader.login(username, password)
            self._save_session(username)
            self.current_user = username
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
            posts = profile.get_posts()
            
            for post in posts:
                if not post.is_video:
                    if callback: callback(f"Preparing to download post {count + 1}...")
                    
                    # Random delay to mimic human behavior and avoid rate limits
                    # Instaloader has its own delays, but extra safety helps
                    delay = random.uniform(2, 5)
                    time.sleep(delay)
                    
                    self.loader.download_post(post, target=user_folder)
                    count += 1
                    if callback: callback(f"Downloaded {count} photo(s).")
            
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
