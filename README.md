

# Overview
Automatically upload assignments and avoid deadlines for UMT SKT 🙂 <br>

If one student uploads an assignment it will be downloaded paraphrased and uploaded to all student accounts, I'm basically making this because of my procrastination I didn't submit any assignment on time, and I had to face the consequences in exam results :(


<h2> Dependencies </h2>
Python3,
Selenium,
Google Chrome,
WebDriver for Chrome,
beautifulSoup4


<br>


# Roadmap

- [x] ~~Initial Implementation~~
- [x] ~~Extract Assignment Links~~
  - [x] ~~One Course~~
  - [ ] Multiple Courses
- [ ] Multiuser
  - [x] ~~Add Multiple Accounts~~ 
  - [x] ~~Check for Submitted Assignments~~
  - [x] ~~Download Assignment if One User Submitted~~
  - [ ] Upload/Sync Assignment Across All Users
    - [x] ~~Basic Implementation~~
    - [x] ~~Dynamically change assignment file names~~
    - [ ] Dynamically change the cover page of assignments
- [ ] Check for Enrollment
  - [ ] Skip if enrollment is closed
  - [ ] Automatically enroll if possible
- [ ] Paraphrasing Assignments
  - [x] ~~Basic Paraphrasing with <b>NLTK</b>~~
  - [ ] Advanced Paraphrasing 
  - [ ] Explore python-docx module
- [ ] Figure Out <i><b>XHR Requests</b></i> for dynamically loaded course sections
- [ ] Generate CSV/EXCEL file
- [ ] Whatsapp Bot
  - [ ] Explore APIs like Twilio etc
  - [ ] Notifications
  - [ ] Screenshots

 <h2> Current Task </h2>
 
A refactor is needed is to better organize the code, and make it modular to add new features <h2> Note </h2>
 This is a proof of concept, the final implementation will be done using <b>scrapy-splash</b> instead of selenium

<h3> Don't hesitate to contribute :) </h3>
