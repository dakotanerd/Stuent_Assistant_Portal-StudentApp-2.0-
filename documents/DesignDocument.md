# Project Design Document

## Student Assistant Portal
--------
Prepared by:

* Alicia Zhu, WPI - Computer Science
* Dale Asante, WPI - Computer Science, Psychology 
* Ethan Carter, WPI - Computer Science, IMGD
* Dakota Wellerbrady, WPI - Computer Science
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
    - [2.1 Database Model](#21-model)
    - [2.2 Subsystems and Interfaces](#22-subsystems-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
    - [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

### Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-15 |Initial draft | 1.0        |
|Revision 2 |2024-11-21 |Second draft  | 1.1|
|Revision 3      |2024-11-22      |Final         |1.2         |


# 1. Introduction

This file will provide information about the design and layout of our student assistant application portal.

# 2. Software Design

## 2.1 Database Model

[//]: <Provide a list of your tables (i.e., SQL Alchemy classes) in your database model and briefly explain the role of each table.>

Tables:
- User
- Student
- Teacher
- Application
- PastEnrollments
- Position
- Course
- CourseSections

[//]: <Provide a UML diagram of your database model showing the associations and relationships among tables.> 

## 2.2 Subsystems and Interfaces

### 2.2.1 Overview

[//]: <Describe the high-level architecture of your software:  i.e., the major subsystems and how they fit together. Provide a UML component diagram that illustrates the architecture of your software. Briefly mention the role of each subsystem in your architectural design. Please refer to the "System Level Design" lectures in Week 4.> 

Major Subsysytems:
1. Client
2. Teacher
3. Auth
4. Student
5. Error Handlers
6. Model
7. SQLite3 Database

When the user accesses our software, they will be redirected to the login page (auth page), depending on the user type once they login they will be taken to either the student main page or the teacher main page. The user will also be able to register as a student or teacher from the login page. Should anything go wrong during the authentication or registration process, the error handlers will return an error. When the user is adding information such as creating a class (teacher only action) it will be added to the model that will then access the SQLite 3 Database and commit the information to the database so it is saved. 


### 2.2.2 Interfaces

#### 2.2.2.1 \<Main> Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. student_index  | POST, GET | /student/index | displays the student home page. recommended courses, applications, and all courses will be displayed inside of the student_index route |
|2. teacher_index  | POST, GET | /teacher/index | displays the teacher home page. a teacher's sections and applications for these sections will be displayed through the teacher_index route |
|3. display_student_profile  | GET |   /student/profile  | displays student profile (name, wpi-id, major etc.) old SA positions will be shown here |
|4. display_teacher_profile  | GET |   /teacher/profile  | displays teacher profile (name, email, etc.) |
|5. apply  |  POST, GET  | /student/application  | allows for student to apply for an SA position | 
|6. create_section  |  POST, GET  |  /course/section/create  |  displays the applicatns of a given course  |
|7. applicant  | GET  |  /course/<course_id>/applicants  |  displays the applicants of a given course  | 
|8. applicant_data |  GET  |  /course/<course_id>/data  |  gathers the data for the applicants of a given course  | 
|9. application_accept | POST, GET | /application/<application_id>/accept | teachers can accept a student's application and confirms the student as an SA for the course |
|10. application_reject | POST, GET | /application/<application_id>/reject | teachers can reject a student's application which will delete their application from the positions database and show as rejected on the student home page |

#### 2.2.2.2 \<Auth> Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. student_register |  POST, GET  |  /student/register  |  register page for students, renders the form for students to register their accounts  |
|2. teacher_register |  POST, GET  |  /teacher/register  |  register page for teachers, renders the form for teachers to register their account  |
|3. login |  POST, GET  |  /login   |  page for allowing users to log in  |
|4. logout| POST, GET  |  /logout  |  logouts the user  | 

### 2.3 User Interface Design 

### Login Page
![Login Page Mockup](./images/SignIn2.png)

User Stories:
- As a user, I want my personal information to be securely stored for privacy protection.

### Register Page
![Positions Page Mockup](./images/Register2.png)
User Stories:
- As a user, I want my personal information to be securely stored for privacy protection.

### Student Homepage
![Dashboard Mockup](./images/Student_Portal.png)

User Stories:
- As a student, I want to view all open student assistant positions to find job opportunities.
- As a student, I want detailed information about each position to assess my qualifications.
- As a student, I want to see recommended positions based on my qualifications.
- As a student, I want to view recommended positions in order of how qualified I am for them so that I can choose the most suitable job opportunity.
- As a student, I want to see course information, term, instructor, qualifications, and times so that I can easily look for ones that fit my qualifications and schedule.
- As a student, I want to track the status of my applications so that I know when an application is pending or has been approved/denied.
- As a student, I want to receive notifications about whether my application status has changed.
- As a student, I want to receive notifications when a course that I am qualified for is created or has new availability.
- As a student, I want to withdraw pending applications if I am no longer interested in an that SA position.
- As a user, I want the system to be easy to navigate for quick access to information.
- As a user, I want the system to load quickly to apply efficiently.
- As a user, I want mobile access to manage my applications on the go.
- As a user, I want notifications about changes to my account or applications.

### Teacher Homepage
![Positions Page Mockup](./images/Teacher-Homepage.png)

User Stories:
- As a faculty member, I want to be notified when a new student applies for a position in my class so that I can review their application.
- As a faculty member, I want to be able to select only the needed amount of SAs needed and close the availability for the course afterwards.
- As a faculty member, I want to only be able to accept students that have not been accepted by another instructor for SAship already.
- As an administrator, I want to be notified when applications are confirmed and connections have been made so that I can start the official process of registration, payment details, and more.
- As a user, I want the system to be easy to navigate for quick access to information.
- As a user, I want the system to load quickly to apply efficiently.
- As a user, I want mobile access to manage my applications on the go.
- As a user, I want notifications about changes to my account or applications.

### Display Student Profile
![Positions Page Mockup](./images/Student_Profile2.png)

User Stories:
- As an administrator, I want students and faculty to be able to register for separate accounts so that they can interact with each other properply and efficiently.

### Display Teacher Profile 
![Positions Page Mockup](./images/View_Teacher_Profile.png)

User Stories:
- As an administrator, I want students and faculty to be able to register for separate accounts so that they can interact with each other properply and efficiently.

### SA Application Form
![Application Form Mockup](./images/Application.png)

User Stories:
- As a faculty member, I want to allow students to submit a brief description about why they want this position and what they will bring to the table.
- As a faculty member, I want to allow students to submit their previous work and SA experience so that I can gauge their previous work experience better.
- As a faculty member, I want to know what their experience and grades were taking this course so I know what to expect from them and whether they are qualified for this job.
- As a student, I want to apply for multiple student assistant positions at once.
- As a student, I want to add supplementary information to my application upon submission such as a cover letter, resume, and references.
- As a student, I want to indicate my availability in my application.
- As a faculty member, I want to view the qualifications of each student in their applications so that I can make the most informed decsion.

### Create Course Form
![Positions Page Mockup](./images/Create_Course.png)

User Stories:
- As a faculty member, I want to create student assistant positions for my courses so that I can hire students to be an assistant in my class.
- As a faculty member, I want to specify requirements and qualifications necessary to be a student assistant in my class so that I can choose suitable assistants.
- As an administrator, I want to add courses to the course catalog so that faculty members can choose from them for creating their SA positions.
- As an administrator, I want to specifiy the number of SAs needed for a course so that there is no overenrollment.

# 3. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

 * You will first  submit a draft version of this document:
    * "Project 3 : Project Design Document - draft" (5pts). 
* We will provide feedback on your document and you will revise and update it.
    * "Project 5 : Project Design Document - final" (80pts) 

Below is the grading rubric that we will use to evaluate the final version of your document. 

|**MaxPoints**| **Design** |
|:---------:|:-------------------------------------------------------------------------|
|           | Are all parts of the document in agreement with the product requirements? |
| 8         | Is the architecture of the system ([2.2.1 Overview](#221-overview)) described well, with the major components and their interfaces?         
| 8        | Is the database model (i.e., [2.1 Database Model](#21-database-model)) explained well with sufficient detail? Do the team clearly explain the purpose of each table included in the model?| 
|          | Is the document making good use of semi-formal notation (i.e., UML diagrams)? Does the document provide a clear UML class diagram visualizing the DB model of the system? |
| 18        | Is the UML class diagram complete? Does it include all classes (tables) and does it clearly mark the PK and FKs for each table? Does it clearly show the associations between them? Are the multiplicities of the associations shown correctly? ([2.1 Database Model](#21-database-model)) |
| 25        | Are all major interfaces (i.e., the routes) listed? Are the routes explained in sufficient detail? ([2.2.2 Interfaces](#222-interfaces)) |
| 13        | Is the view and the user interfaces explained well? Did the team provide the screenshots of the interfaces they built so far.  ([2.3 User Interface Design](#23-user-interface-design)) |
|           | **Clarity** |
|           | Is the solution at a fairly consistent and appropriate level of detail? Is the solution clear enough to be turned over to an independent group for implementation and still be understood? |
| 5         | Is the document carefully written, without typos and grammatical errors?  |
| 3         | Is the document well formatted? (Make sure to check your document on GitHub. You will loose points if there are formatting issues in your document.  )  |
|           |  |
| 80         | **Total** |
|           |  |

--------
# 4. Diagrams

### UML Diagram
![image](https://github.com/user-attachments/assets/59ac5e70-c24b-4232-a777-d44135af96b7)



### UML Component Diagram
![UML class diagram](https://github.com/user-attachments/assets/deb94c11-2414-4e77-94c5-e05c8b008993)
