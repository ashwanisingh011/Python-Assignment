import instaloader
import sys

try:
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, "instagram")
    print(profile.profile_pic_url)
except Exception as e:
    print("Error:", e)
