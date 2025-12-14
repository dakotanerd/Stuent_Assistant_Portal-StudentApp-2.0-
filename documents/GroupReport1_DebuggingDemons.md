# Project Group Report - 1

## Team: `Debugging Demons`

List team members and their GitHub usernames

* `Dale Asante`,`dakotawellerbrady`
* `Ethan Carter`,`ecarter-wpi`
* `Dakota Wellerbrady`,`yesimdale`
* `Alicia Zhu`,`zaicila`

---
**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

----
## 1. Schedule

Meeting Times:
 * Monday at 4 pm
 * Tuesday at 3 pm
 * Thursday at 4 pm
 * Friday at 1 pm
 * Additional meetings are scheduled whenever needed

----
## 2. Iteration 1 - Summary

 * Users can log in and create accounts as either Teacher or Student
 * Registration and login works and accounts for user type
 * Teachers can create course sections that has the data for the section as well as SA information specific to that section
 * Database set up for User, Student, Teacher, Course, and CourseSection
 * Permissions for every page were implemented
 * List the user stories completed in `Iteration-1`. Mention who worked on those user stories

#### User Stories completed in Iteration-1

* As a student, I want to be able to share my contact information so that professors can reach out to me personally. -- Dale, Dakota
* As an admin,  I want students and faculty ot be able to regsiter for separate accounts so that they can interact with each other properly and efficiently. -- Dale, Dakota
* As an administrator, I want to add courses to the course catalog so that faculty members can choose from them for creating their SA positions. -- Dakota, Alicia
* As an faculty member, I want to specify the number of SAs needed for a course so that there is no over-enrollment --Ethan,Dale
* As a user, I want the system to load quickly to apply efficiently. -All members

Dale and Dakota for much of the registration and login, which are not include in user stories

#### Tasks completed in Iteration-1

* Database Model - Create Student model in database schema - Ethan, Alicia  
* Database Model Create Faculty database model schema -- Ethan, Alicia
* Database Model Create Course Section database model schema -- Dakota
* Database Model Create Course database model schema -- Alicia
* Database Model Create User database model schema -- Ethan
* Create Registration Forms -- Dale, Dakota
* Create Login Form -- Dale, Dakota
* Create Course Form -- Ethan
* Create Authentication Routes -- Dale
* Create Main Routes -- Ethan, Alicia
* Create Main Index Pages -- Ethan, Dakota


## 3. Iteration 1 - Sprint Retrospective

What Went Well:
 * We accomplished the tasks we wanted to
 * We worked very well as a team and met at the times we wanted
What we want to do better:
 * We learned about using multiple branches and experienced many complications this week with only pushing to and pulling from one branch.
 * We will assign things more concretely this week so that everyone has a better idea of what parts of the iteration are their responsibility.
 * The initial setup was challenging for us as every part of the project relied on one another. Now that we have more of the project established, expanding the project will be easier.

----
## 4. Product Backlog refinement

 * We have moved edit and display profile to Iteration-2
 * We added a few database models that we created that were not initially in our Github Issues (Course Section, User)

----
## 5. Iteration 2 - Sprint Backlog


#### User Stories to complete in Iteration-2

* As a faculty member, I want to only be able to accept students that have not been accepted by another instructor for SAship already. -- Dale, Dakota
* As a faculty member, I want to be able to select only the needed amount of SAs needed and close the availability for the course afterwards. -- Dale, Dakota
* As a faculty member, I want to view the qualifications of each student in their applications so that I can make the most informed decision. -- Dale, Dakota
* As a student, I want to withdraw pending applications if I am no longer interested in an that SA position. -- Dakota, Ethan
* As a student, I want to track the status of my applications so that I know when an application is pending or has been approved/denied. -- Dakota, Ethan
* As a faculty member, I want to be notified when a new student applies for a position in my class so that I can review their application. -- Dakota, Ethan
* As a student, I want to indicate my availability in my application. --Ethan, Alicia
* As a student, I want to add supplementary information to my application upon submission such as a cover letter, resume, and references. - Ethan, Alicia
* As a student, I want to apply for multiple student assistant positions at once. -- Ethan, Alicia
* As a student, I want to see course information, term, instructor, qualifications, and times so that I can easily look for ones that fit my qualifications and schedule. -- Alicia, Dale
* As a student, I want to view recommended positions in order of how qualified I am for them so that I can choose the most suitable job opportunity. #33
* As a student, I want detailed information about each position to assess my qualifications. -- Alicia, Dale
* As a student, I want to view all open student assistant positions to find job opportunities. -- Alicia, Dale
* As an faculty member, I want to specify the number of SAs needed for a course so that there is no over-enrollment. -- Alicia
* As a faculty member, I want to know what their experience and grades were taking this course so I know what to expect from them and whether they are qualified for this job. -- Ethan
* As a faculty member, I want to allow students to submit their previous work and SA experience so that I can gauge their previous work experience better. -- Dakota
* As a user, I want to edit my profile information to keep it up to date or make any necessary changes. -- Dale
* As a student, I want to enter the courses I have served as an SA for before as well as courses I received an A for so that the system can make better recommendations for me. -- Ethan


#### Tasks to complete in Iteration-2

* Create display profile page
* Create edit profile form
* Create Application Form
* Create App Page
* Create App Table
* Create Positions Table
* Create Past Enrollments Table
* Implement past enrollments to student registration table
* Past Enrollment page ?
* Accept/reject applications (if we have time)
* Withdraw application for students
* Add deleting sections for teachers (maybe)
