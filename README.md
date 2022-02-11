

# Overview
Automatically upload assignments and avoid deadlines for UMT SKT 🙂 <br>

If one student uploads an assignment it will be downloaded parapharsed and uploaded to all student accounts, I'm basically making this because of my procrastination I didn't submit any assignment on time, and I had to face the consequences in exam results :(


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
  - [ ] Add Multiple Accounts (<i>Work in Progress</i>)
  - [ ] Check for Submitted Assignments
  - [ ] Download Assignment if One User Submitted
  - [ ] Upload/Sync Assignment Across All Users
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
 
 - [ ] Add Multiple Accounts (WIP)
 
      Explore 2d Arrays, Lists, Maps, Sqlite3, MySQL and other methods for temporary or persistant data storage to keep track of students and assignments, I think  sqlite3 will offer good performance and persistant data storage so I will explore it first

 <h2> Note </h2>
 This is a proof of concept, the final implementaion will be done using <b>scrapy-splash</b> instead of selenium

<h3> Don't hesitate to contribute :) </h3>
