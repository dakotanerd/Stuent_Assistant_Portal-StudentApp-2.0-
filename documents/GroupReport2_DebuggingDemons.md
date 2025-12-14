# Project Group Report - 2

## Team: `Debugging Demons`

List team members and their GitHub usernames

* `Dale Asante`,`yesimdale`
* `Ethan Carter`,`ecarter-wpi`
* `Dakota Wellerbrady`,`dakotawellerbrady`
* `Alicia Zhu`,`zaicila`

---
**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

----
## 1. Iteration 2 - Summary

Summary

 * Teachers can now view applications submitted by students
 * Teachers can update the status of student applications to be accepted, rejected, or pending
 * Teachers can view their profile that includes their information
 * Students can now see their applications, recommended courses, and all courses
 * Students can see the sections they are able to apply for
 * Students can fill out the application form to apply for SAship
 * Students can view their profile that includes their information, their applications, and their past enrollments
 * Students can add a past enrollment that tracks the year they took a course and the grade they received
 * We added a lot of bootstrap to all pages and made the application look nicer
 * We deployed to AWS (with some bugs)
 * We updated database to Postgres

User Stories we completed:
* Create Course Section Application (Teacher) task - @DakotaWellerbrady, @ecarter-wpi
* Create Course Section Application (Student) task - @DakotaWellerbrady, @ecarter-wpi
* Deploy to AWS task - @zaicila
* Integrate PostgreSQL task - @zaicila
* Create Past Enrollments Table task - @DakotaWellerbrady, @ecarter-wpi
* Change Theme of Site to WPI task - @YesImDale
* Add Bootstrap Styling to All Pages task - @YesImDale
* Create Display Profile Page task - @YesImDale, @DakotaWellerbrady
* Create Edit Profile Form task - @YesImDale, @DakotaWellerbrady
* As a student, I want to track the status of my applications so that I know when an application is pending or has been approved/denied. User Story - @ecarter-wpi
* As a faculty member, I want to know if a new student applies for a position in my class so that I can review their application. User Story - @dakotawellerbrady
* As a student, I want to add supplementary information to my application upon submission such as a cover letter, resume, and references. User Story - @zaicila
* As a student, I want to apply for multiple student assistant positions at once. User Story - @ecarter-wpi
* As a student, I want to see course information, term, instructor, and qualifications so that I can easily look for ones that fit my qualifications and schedule. User Story - @DakotaWellerbrady, @zaicila
* As a student, I want to view recommended positions in order of how qualified I am for them so that I can choose the most suitable job opportunity. User Story - @YesImDale
* As a student, I want to see recommended positions based on my qualifications. User Story - @ecarter-wpi
* As a student, I want detailed information about each position to assess my qualifications. User Story - @DakotaWellerbrady, @zaicila
* As a student, I want to view all open student assistant positions to find job opportunities. User Story - @YesImDale, @ecarter-wpi
* As a faculty member, I want to know what their experience and grades were taking this course so I know what to expect from them and whether they are qualified for this job. User Story - @dakotawellerbrady
* As a faculty member, I want to allow students to submit their previous work and SA experience so that I can gauge their previous work experience better. - @zaicila
* As a faculty member, I want to specify requirements and qualifications necessary to be a student assistant in my class so that I can choose suitable assistants - @YesImDale, @ecarter-wpi
* As a faculty member, I want to create student assistant positions for my courses so that I can hire students to be an assistant in my class - @YesImDale, @ecarter-wpi
* As a faculty member, I want to edit my profile information to keep it up to date or make any necessary changes - @YesImDale, @DakotaWellerbrady
* As a user, I want to edit my profile information to keep it up to date or make any necessary changes - @YesImDale, @DakotaWellerbrady
* As a student, I want to enter the courses I have served as an SA for before as well as courses I received an A for so that the system can make better recommendations for me - @ecarter-wpi

----
## 2. Iteration 2 - Sprint Retrospective

What Went Well:
 * We accomplished the tasks we wanted to
 * We worked very well as a team and met at the times we wanted
 * We made expectations of each other very clear and gave specific tasks for everyone to complete for iteration2

What we want to do better:
 * We should start work on our tasks earlier so we are not as stressed to complete everything

----
## 3. Product Backlog refinement

 * Removed some user stories related to notifcations and scheduling
 * Moved some user stories from iteration2 to iteration3 that were related to full application functionality

----
## 4. Iteration 3 - Sprint Backlog

Iteration3 User Stories
Users stories that do not mention anyone are unassigned for the moment

* Withdraw Application Functionality for Students
* Update Application Status Functionality
* Recommended Positions Algorithm task
* Switch to WPI SSO Login task
* Get AWS Deployment to Work Properly task
* Create Edit Profile Form task - @YesImDale, @DakotaWellerbrady
* As a user, I want my personal information to be securely stored for privacy protection. User Story
* As a user, I want mobile access to manage my applications on the go. User Story
* As a user, I want the system to be easy to navigate for quick access to information - @YesImDale, @DakotaWellerbrady, @ecarter-wpi, @zaicila
* As a faculty member, I want to only be able to accept students that have not been accepted by another instructor for SAship already
* As a faculty member, I want to be able to select only the needed amount of SAs needed and close the availability for the course afterwards
* As a faculty member, I want to view the qualifications of each student in their applications so that I can make the most informed decision - @DakotaWellerbrady, @ecarter-wpi
* As a student, I want to withdraw pending applications if I am no longer interested in an that SA position
