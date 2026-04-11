# Project Report: Instagram Photo Downloader

## 1. Cover Page
- **College Name:** Silver Oak University
- **Department Name:** SOCCA
- **Course Name & Course Code:** BCA 
- **Project Title:** Instagram Photo Downloader
- **Student Name:** Ashwani Singh
- **Enrollment Number:** 2404030100150
- **Semester & Academic Year:** 4th Semeseter/ 2nd Year

---

## 2. Index Page
1. Cover Page
2. Index Page
3. Introduction
4. Python Concepts Used
5. System Design / Workflow
6. Implementation
7. Output / Results
8. Conclusion & Learning Outcomes
9. References

---

## 3. Introduction
### Problem Statement
Downloading photos from social media platforms like Instagram can be tedious if done manually. There is a need for a simple automated tool that can fetch and save public profile images efficiently without needing complex configurations. Furthermore, Instagram blocks rapid automated requests, which necessitates an application that can cleverly mitigate rate limits while downloading.

### Objective of the Project
The goal of this project is to develop a Python-based desktop application with a professional graphical user interface (GUI) that allows users to download photos (either full profile posts or just the profile picture) from any Instagram profile by simply providing the username or profile URL. The application also aims to improve reliability by incorporating an optional login system to save user sessions and prevent "rate limit" or connection blocks.

---

## 4. Python Concepts Used
- **Object-Oriented Programming (OOP):** Modularizing the core logic into classes, dividing the application cleanly into `InstagramDownloader` (backend) and `InstagramDownloaderGUI` (frontend).
- **Tkinter & TTK:** Building a professional Graphical User Interface (GUI) with themed widgets utilizing the 'clam' theme, modern layouts featuring card-like frames, and a clean 'Segoe UI' based typography.
- **Authentication & Sessions:** Implementing a login functionality to handle Instagram's security measures. Generating and restoring session files in a `.sessions` directory to ensure continuous automated access without repeatedly passing credentials.
- **UI/UX Design:** Applying modern design principles like cards, clean spacing, clear status labeling, and consistent color palettes (e.g., `#fafafa` background and `#0095f6` Instagram blue buttons).
- **Threading:** Using the `threading` module to run time-consuming downloads, logins, and API calls in the background, ensuring the GUI remains fully responsive to user interactions.
- **File & Directory Handling:** Leveraging the `os` module to automatically create `downloads` and private `.sessions` directories for organizing fetched media and saving secure local configurations.
- **Exception & Error Handling:** Managing network errors, invalid inputs (extracting usernames directly from pasted URLs), rate limits gracefully (using `random` delays), and private profile restrictions.
- **Third-party Libraries:** Using `instaloader` for efficiently scraping and interacting with Instagram web data without requiring an official, heavily-limited Instagram Developer API key.

---

## 5. System Design / Workflow
### Flowchart Explanation
1. **Start:** User launches the executable/application GUI.
2. **Session Initialization:** System silently checks for a previously saved `.sessions` file and re-authenticates if one is found.
3. **Login (Optional):** User can optionally supply credentials to create a new authenticated session to avoid downloading bottlenecks.
4. **Input:** User enters an Instagram username or pastes the full profile URL into the target entry box.
5. **Sanitization:** The application parses the input, truncating redundant strings and slicing out solely the username from any full URLs.
6. **Task Selection:** User chooses whether to "Download Profile Pic" or "Download Posts".
7. **Validation & Privacy Check:** The Instaloader backend verifies the existence of the profile and checks if it is set to private. If private or nonexistent, an error message is populated directly in the status text box.
8. **Fetching:** Loop through the profile's media. The system employs periodic `time.sleep` actions with randomized intervals (between 2 to 5 seconds) to simulate human browsing patterns, combating Instagram's rate limiting.
9. **Downloading:** Save images into a designated `downloads/<username>` folder.
10. **Complete:** Notify the user upon successful execution and reset UI controls.

---

## 6. Implementation
### Program Logic
The application rigidly adheres to the Model-View-Controller style utilizing two main Python components:

1. **`downloader.py` (Backend):** 
   Contains the `InstagramDownloader` class. Functions include `login()` for creating `.sessions`, `download_profile_photos()`, and `download_profile_picture()`. It isolates all `instaloader` interactions and executes the crucial exception handling blocks for errors such as `ProfileNotExistsException` and rate limiting/Connection blocks (`401 Unauthorized`).

2. **`main.py` (Frontend):** 
   Contains the `InstagramDownloaderGUI` class. It manages the Tkinter root, creates the visual frame elements, binds methods to buttons, initiates separate DAEMON threads for heavy functions (`start_download` & `start_download_pic`), and pushes live updates into the `status_text` console using thread-safe `root.after()` callbacks.

### Code Snippets
**Core downloading loop with rate-limiting bypass:**
```python
# Random delay to mimic human behavior and avoid rate limits
for post in posts:
    if not post.is_video:
        delay = random.uniform(2, 5)
        time.sleep(delay)
        self.loader.download_post(post, target=user_folder)
```

**Thread-safe status updates to GUI:**
```python
def _update_status(self, message):
    self.status_text.insert(tk.END, f"[{message}]\n")
    self.status_text.see(tk.END)
```

---

## 7. Output / Results
- **Screenshot:** (To be added after execution)
- **Sample Input (Username or URL):** `instagram` or `https://instagram.com/instagram` (public profile)
- **Status Updates During Execution:** Live feed of "Fetching profile...", "Preparing to download post 1...", "Downloaded 1 photo(s)..." etc.
- **Final Output:** A distinct folder named `downloads/instagram` populated with dynamically collected high-quality JPEG image files and metadata.

---

## 8. Conclusion & Learning Outcomes
This project successfully demonstrates the use of Python for modern web automation, resilient API interaction, and professional GUI development. 
**Skills Learned:**
- Proper integration and handling of sophisticated third-party automation libraries like `instaloader`.
- Application of `threading` principles to circumvent the Single-Threaded nature of Tkinter, providing a smooth user experience.
- Dealing with real-world web scraping hurdles—such as URL sanitization, randomizing request timers, generating persistent session files, and mitigating strict IP/Rate blockades instantiated by large corporations like Meta.
- Designing a polished, user-friendly tool replacing a tedious manual task.

---

## 9. References
- Python Official Documentation: [python.org](https://www.python.org/)
- Instaloader Documentation: [instaloader.github.io](https://instaloader.github.io/)
- Tkinter GUI Tutorial: [tkdocs.com](https://tkdocs.com/)
