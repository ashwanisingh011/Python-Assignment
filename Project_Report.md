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
Downloading photos from social media platforms like Instagram can be tedious if done manually. There is a need for a simple automated tool that can fetch and save public profile images efficiently.

### Objective of the Project
The goal of this project is to develop a Python-based desktop application with a graphical user interface (GUI) that allows users to download photos from any public Instagram profile by simply providing the username.

---

## 4. Python Concepts Used
- **Object-Oriented Programming (OOP):** Modularizing the downloader logic into classes.
- **Tkinter & TTK:** Building a professional Graphical User Interface (GUI) with themed widgets and a modern layout.
- **Authentication & Sessions:** Implementing login functionality to handle Instagram's security measures.
- **UI/UX Design:** Applying modern design principles like cards, clean spacing, and consistent color palettes.
- **Threading:** Running time-consuming downloads in the background to ensure the GUI remains responsive.
- **File Handling:** Creating directories and saving image files locally.
- **Exception Handling:** Managing network errors, invalid usernames, and private profile restrictions.
- **Third-party Libraries:** Using `instaloader` for interacting with web data.

---

## 5. System Design / Workflow
### Flowchart Explanation
1. **Start:** User launches the application.
2. **Input:** User enters an Instagram username.
3. **Validation:** System checks connection and existence of the profile.
4. **Privacy Check:** If private, show error. If public, proceed.
5. **Fetching:** Loop through posts and identify images.
6. **Downloading:** Save images into a designated folder.
7. **Complete:** Notify user and show success message.

---

## 6. Implementation
### Program Logic
The application uses two main components:
1. `downloader.py`: Contains the `InstagramDownloader` class which handles the `instaloader` session and downloading logic.
2. `main.py`: Contains the `InstagramDownloaderGUI` class which implements the Tkinter frontend and connects user actions to the downloader.

### Code Snippets
```python
# Core downloading loop
for post in profile.get_posts():
    if not post.is_video:
        self.loader.download_post(post, target=user_folder)
```

---

## 7. Output / Results
- **Screenshot:** (To be added after execution)
- **Sample Input:** `instagram` (public profile)
- **Output:** A folder named `downloads/instagram` containing photos.

---

## 8. Conclusion & Learning Outcomes
This project successfully demonstrates the use of Python for web automation and GUI development. 
**Skills Learned:**
- Integration of third-party APIs/libraries.
- Multi-threading for smoother GUI experience.
- Effective error handling in real-world scenarios.

---

## 9. References
- Python Documentation: [python.org](https://www.python.org/)
- Instaloader Documentation: [instaloader.github.io](https://instaloader.github.io/)
- Tkinter Tutorial: [tkdocs.com](https://tkdocs.com/)
