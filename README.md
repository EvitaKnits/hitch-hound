![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Hitch Hound: a lightweight issue-tracker

'Hitch Hound' is built using Django, Python, Bootstrap, JavaScript and PostgreSQL. It is hosted on Heroku.
Automated testing is done with Unittest for Python.

(Add responsive screenshot here)

# Table of Contents
1. [Purpose](#purpose)
2. [Requirement Gathering and Planning](#requirement-gathering-and-planning) <br>
    a. [Brief Competitor Analysis and Target Demographic](#brief-competitor-analysis-and-target-demographic) <br>
    b. [Data and Security features](#data-and-security-features)<br>
    c. [Epics and User Stories](#epics-and-user-stories) <br>
    d. [User Journeys](#user-journeys) <br>
    e. [User Permissions](#user-permissions)<br>
3. [Data Design](#data) <br>
    a. [Database Schema](#database-schema) <br>
    b. [Data Manipulation](#data-manipulation) <br>
    c. [Data Validation](#data-validation) <br>
4. [User Interface Design](#user-interface-design) <br>
    a. [Computer Wireframes](#computer-wireframes)<br>
    b. [Mobile Wireframes](#mobile-wireframes)<br>
    c. [Colour Scheme](#colour-scheme) <br>
    d. [Logo](#logo) <br>
5. [Testing](#testing) <br>
    a. [Test Plan](#test-plan) <br>
    b. [Automated Testing](#automated-testing) <br>
    c. [Manual Testing](#manual-testing) <br>
    d. [Browser Compatibility and Screen Size Responsiveness](#browser-compatibility-and-screen-size-responsiveness) <br>
    e. [Key Responsiveness Differences](#key-responsiveness-differences) <br>
    f. [Accessibility](#accessibility) <br>
6. [Bugs](#bugs)
7. [Deployment](#deployment)
8. [Agile Methodology](#agile-methodology) <br>
    a. [Sprint One](#sprint-one-2705-to-0206) <br>
    b. [Sprint Two](#sprint-two-0306-to-0906) <br>
    c. [Sprint Three](#sprint-three-1006-to-1606) <br>
9. [Credits](#credits)

## Purpose
The objective of this program is to streamline the process of tracking and communicating about issues and bugs arising in software development projects. It is lightweight and intuitive, providing ample functionality for small to medium enterprises who don't need an elevated level of auditing and oversight. 

## Requirement Gathering and Planning

Before starting the coding for this project, I created a detailed plan including my database schema, user journeys and wireframes.

### Brief Competitor Analysis and Target Demographic
When considering competitors in the realm of issue and bug tracking software, it's helpful to look at some well-known options. Atlassian's Jira is widely recognised for its range of features and flexibility, making it a go-to choice for companies of all sizes. Another popular option is GitHub's issue tracking system, which seamlessly integrates with its version control platform, making it a convenient choice for teams already using GitHub. Additionally, tools like Trello are valued for their user-friendly interface and adaptability, though they do lack some of the specific features tailored for issue tracking. In this landscape, my program intends to stand out by focusing on simplicity and ease of use, making it ideal for small to medium enterprises (SMEs) looking for a straightforward solution without unnecessary complexity. The goal is to provide a practical and efficient tool for managing software development issues, offering a simpler alternative in a market dominated by larger, more complex platforms.

### Data and Security Features

With this in mind, the data features chosen are clean and simple. Users can create issues that they associate with a particular project. This allows for a streamlined and intuitive user experience, enhancing productivity and facilitating effective project management. 

The security features cover the essentials: authentication with a username and password, data validation and sanitisation, and keeping track of any changes made with an audit trail.

### Epics and User Stories

My user stories can be seen in full in the associated GitHub Project on my repo. This is where all the details, including tasks and acceptance criteria can be seen. These user stories have been assigned to Epics.

Epic 1: User Management
- Create basic front-end
- User Registration 
- User Login and Logout
- Password Reset
- Create and Edit Role-Based Permissions
- View and Assign Superuser Status to Users

Epic 2: Issue Management 
- Create Issue
- Edit Issue 
- View Issues
- Close, Cancel or Delete Issues 
- Comment on Issues
- Attach Files to Issues

Epic 3: Notifications and Error Messaging
- Add Meaningful 404 Page
- Receive Notifications from Other Users' Actions

Epic 4: Enhanced Issue Management
- Provide a Change History Log
- Connect 2+ Issues as Related
- Search for Issues by Keyword

Epic 5: Project Management
- Create Project
- Edit Project
- Delete Projects

Epic 6: Reporting
- Add Reporting
 
### User Journeys

As a lightweight issue tracking program, my goal was to make each user journey as simple as possible with the fewest steps, whilst still providing value and flexibility of working method. There are ten core user journeys. The below is not an exhaustive list of all possible user journeys, just the most important ones:

1. New User
```mermaid
flowchart LR
    A[Navigate to Hitch Hound] --> B[Enter details on Sign Up form]
    B --> C[Click Sign Up button]
    C --> D[Log in with email and password]
```

2. Create an Issue
```mermaid
flowchart LR
    A[Log In] --> B[Click '+'\n button]
    B --> |New Item \nPopup|C[Click 'Issue'\n button]
    C --> D[Fill in New\n Issue form]
    D --> E[Click 'Submit \nNew Issue' button]
```

3. Browse Issues
```mermaid
flowchart TD
    A[Log In] --> B[Click 'Issues' in\n the navigation bar]
    A --> C[Click 'Projects' in\n the navigation bar]
    A --> D[Click 'Reports' in \nthe navigation bar]
    A --> E[Click on User Profile\n in the navigation bar]
    B --> F[Scroll through issues\nand click through pages]
    C --> G[Click 'View All Issues'\nbutton next to the \ndesired project]
    D --> H[Click on 'Issue Listing \nby Status' button]
    H --> I[Select status in dropdown]
    E --> J[Scroll through issues\n and click through pages]
```
4. Edit an Issue
```mermaid
flowchart LR
    A[Log In] --> B[Navigate to an issue as per \n 'Browse Issues' user journey]
    B --> C[Click\n 'Edit Issue']
    C --> D[Amend details\n or add a comment]
    D --> E[Click\n 'Save Issue']
```

5. Close, Cancel or Delete an Issue
```mermaid
flowchart LR
    A[Log In] --> B[Navigate to an issue as per\n 'Browse Issues' user journey]
    B --> C[Set status to 'Closed'\n or 'Cancelled']
    B --> E[Click 'Delete Issue']
    E --> F[Confirm deletion]
    C --> D[Click 'Save Changes']
```
6. Create a Project
```mermaid
flowchart LR
    A[Log In] --> B[Click '+'\n button]
    B --> |New Item \nPopup|C[Click 'Project'\n button]
    C --> D[Fill in New\n Project form]
    D --> E[Click 'Create \nNew Project' button]
```

7. Browse Projects
```mermaid
flowchart LR
    A[Log In] --> B[Click 'Projects' in\n the navigation bar]
    B --> C[Scroll through projects\n and click through pages]
```

8. Edit a Project
```mermaid
flowchart LR
    A[Log In] --> B[Navigate to a project as per\n 'Browse Projects' user journey]
    B --> C[Click 'Edit\n Project' button]
    C --> D[Amend\n details]
    D --> E[Click\n 'Save Project']
```

9. Delete a Project
```mermaid
flowchart LR
    A[Log In] --> B[Navigate to a project as per\n 'Browse Projects' user journey]
    B --> C[Click 'Delete\n Project' button]
    C --> D[Confirm deletion]
```

10. Generate Reports
```mermaid
flowchart LR
    A[Log In] --> B[Click on 'Reports' in\nthe navigation bar]
    B --> C[Click on one of the\n available report buttons]
    C --> D[Adjust settings as needed\n with dropdowns provided]
```

### User Permissions

There are four types of user, each with different permissions.

| Type | Can create issue? | Can change status to | Can close issue?| Can access admin panel? |
|---|---|---|---|---|
| **Role Based** |
| --> Developer | Yes | In-Progress | No | No |
| --> Quality Assurance | Yes | Testing | No | No |
| --> Product Manager | Yes | Approved |Yes | No |
| **Secondary** |
| --> Superuser | Yes | Any | Yes | Yes |

Each user *must* be assigned a role-based type and *may* also be assigned the superuser type additionally. 

## Data Design

### Database Schema 

The following Entity Relationship Diagram (ERD) illustrates the key entities and relationships in Hitch Hound. It defines the relationships between Issues and all other entities.

![erd](documentation/erd.png)

*Added mid-development: 
A 'Project ID' to be the primary key for the Projects table. This was required because at the time of designing my database, I didn't realise that it is not possible to edit a primary key. Therefore the title could not be the primary key because the title needs to be editable by users. 

### Data Manipulation

Hitch Hound uses CRUD principles to guide all data manipulation. 

#### Issues
- Create: report a new issue, filling in all mandatory fields.
- Read: retrieve an issue by project, issues page, reports or user profile.
- Update: edit an issue's fields or add a new comment. 
- Delete: delete an issue.

#### Projects
- Create: start a new project, filling in the title. 
- Read: retrieve a project via the projects page.
- Update: change the title of a project. 
- Delete: delete a project and all of its issues. 

#### Other Data

- The 'Change' entity type is a type of metadata created after an 'Issue' entity is updated in any way. It is not possible to update or delete a 'Change' entity.
- The 'Comment' entity type is simply one of the updates to the 'Issue' entity type.

### Data Validation

The following data validation rules ensure the accuracy and reliability of information stored in the system, ensuring all entries adhere to expected formats.

#### Users
- userID: Must be a unique integer
- firstName: Must be non-empty string 
- lastName: Must be non-empty string
- emailAddress: Must be a valid email format and unique within the system
- password: Must meet complexity requirements (e.g., minimum length, inclusion of special characters)
- role: Must be one of the predefined roles (developer, quality assurance or product manager)
- superuser: Must be a boolean value

#### Projects
- projectID: Must be a unique integer (*Added mid-development. See note below ERD for more information)
- title: Must be a unique, non-empty string

#### Issues
- issueID: Must be a unique integer
- title: Must be a non-empty string
- description: Must be a string, can be empty
- severity: Must be one of the predefined levels (4-low, 3-medium, 2-high, 1-critical)
- project: Must reference a valid project title
- type: Must be one of the predefined types (bug, missed requirement or other issue)
- status: Must be one of the predefined statuses (open, in progress, testing, approved, closed or cancelled)
- reporter: Must reference valid userID
- developer: Must reference valid userID
- qualityAssurance: Must reference valid userID
- productManager: Must reference valid userID

#### Comments
- commentID: Must be a unique integer
- commentText: Must be a non-empty string
- userID: Must reference a valid userID
- issueID: Must reference a valid issueID
- commentTimestamp: Must be a valid timestamp

#### Changes
- changeID: Must be a unique integer
- issueID: Must reference a valid issueID
- userID: Must reference a valid userID
- changeTimestamp: Must be a valid timestamp
- fieldChanged: Must be one of the predefined types (all 'Issue' attributes apart from IssueID).
- oldValue: Must be a string, can be empty.
- newValue: Must be a string, can be empty.

## User Interface Design

### Computer Wireframes

The wireframes I created illustrate the core user interface and functionality of Hitch Hound from both a desktop/laptop perspective and a mobile/tablet perspective. These visual guides serve as a blueprint for the design and structure of the application, ensuring a cohesive and intuitive user experience. 

#### Home: Sign Up

![signup](documentation/signup.png)

#### Home: Log In

![login](documentation/login.png)

#### Home: Logged In

![loggedin](documentation/loggedin.png)

#### Individual Issue

![individualissue](documentation/individualissue.png)

#### Issue Change History

![changehistory](documentation/changehistory.png)

#### New Issue

![newissue](documentation/newissue.png)


#### Projects

![projects](documentation/projects.png)

#### Individual Project

![individualproject](documentation/individualproject.png)

#### New Project

![newproject](documentation/newproject.png)

#### Edit Project

![editproject](documentation/editproject.png)

#### Reports

![reports](documentation/reports.png)


#### User Profile

![userprofile](documentation/userprofile.png)


#### Notification Modal

![notificationmodal](documentation/notificationmodal.png)

#### 404 Page

![404page](documentation/404page.png)

### Mobile Wireframes

| Sign Up | Log In |
|---|---|
|![signupmobile](documentation/signupmobile.png) | ![loginmobile](documentation/loginmobile.png) |

| All Issues | Individual Issue  |
|---|---|
|![loggedinmobile](documentation/loggedinmobile.png)| ![individualissuemobile](documentation/individualissuemobile.png)|

|Issue Change History| New Issue |
|---|---|
|![changehistorymobile](documentation/changehistorymobile.png) | ![newissuemobile](documentation/newissuemobile.png) |

| Projects | Individual Projects |
|---|---|
|![projectsmobile](documentation/projectsmobile.png) | ![individualprojectmobile](documentation/individualprojectmobile.png) |

| New Project | Edit Project |
|---|---|
|![newprojectmobile](documentation/newprojectmobile.png) | ![editprojectmobile](documentation/editprojectmobile.png) |

| Reports |
|---|
| ![reportsmobile](documentation/reportsmobile.png) | 

| User Profile | Notifications |
|---|---|
|![userprofilemobile](documentation/userprofilemobile.png)| ![notificationmobile](documentation/notificationsmobile.png) |

| 404 Page |
|---|
| ![404pagemobile](documentation/404pagemobile.png) |

### Colour Scheme 

I wanted to pick a muted palette to reflect the business nature of my program. I chose my base colour and then selected two lighter shades to implement as a gradient. I then desaturated my base colour by 90% to find a complementary charcoal grey. Finally, I lightened my colour by 95% to find a complementary cream colour. 

![colourscheme](documentation/colourscheme.png)

### Logo + Favicon

As I had chosen the name 'Hitch Hound' for my program, I thought this dog in a shield was perfect for my logo:<br> 
![shield](documentation/shield.png)

And this dog was perfect for my favicon:<br>
![dog](documentation/dog.png)

## Testing

### Test Plan

**Continuous Testing**

Through a combination of automated testing written using Unittest for Python, and manual testing from the front-end, I achieved a good coverage of test cases. The code I wrote was also passed through validators/linters at the end to ensure adherance to coding standards and best practices, ultimately aiming for robust and maintainable code. I considered using Jest to test my JavaScript files but on balance decided that it was not worth doing because the amount of JavaScript was quite small and the functions quite simple. I will be completing a fifth project with advanced front-end frameworks such as React which is better suited to Jest testing, so I will apply it more valuably there. 

### Automated Testing
When I was sufficiently through my project to have a stable enough codebase, I started adding automated tests incrementally for each area. The tests for views, forms and models were added to each app. 

### Manual Testing

My manual testing covered: 

- Each user journey from end to end
- The level of access when logged out 
- The level of access when logged in as a regular user
- The level of access when logged in as a superuser

### Browser Compatibility and Screen Size Responsiveness

I viewed the program on each of the three key screen sizes (mobile, tablet and computer), using devtools, on four of the most popular browsers. I also used the responsive setting to slide the width of the screen from narrow all the way through to wide to check the transition points. 

Pixel references for each of the screen sizes:

|Screen | Pixels |
|-----|-----|
| Mobile - iPhone SE | 375px |
| Tablet - iPad Mini | 768px |
| Computer | 1366px |

| Browser | Screen Size | Appearance | Responsiveness |
|-------|-----|-----|-----|
| Chrome | Mobile | Bug 19  | Good |
| | Tablet | Bug 19  | Good  |
| | Computer | Good | Good |
| | Transition Points | Good | Good |
| Firefox | Mobile | Bug 19  | Good |
| | Tablet | Bug 19 | Good |
| | Computer | Good | Good |
| | Transition Points | Good | Good |
| Safari | Mobile | Bug 19 | Good  |
| | Tablet | Bug 19 | Good  |
| | Computer |  Good |Good  |
| | Transition Points | Good | Good |
| Edge | Mobile | Bug 19 | Good |
| | Tablet | Bug 19  | Good |
| | Computer | Good | Good |
| | Transition Points | Good | Good |

### Code Validation

| Language | Validation Method | Outcome |
|---|----|----|
| HTML | Via direct input on [W3C HTML Validator](https://validator.w3.org/) | 9 errors across all pages. All resolved.|
| CSS | Via direct input on [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | No errors found. |
| JavaScript | [JS Hint](https://jshint.com/) | 1 error: missing semicolons. All resolved.  |
| Python | [PEP8 Code Institute Python Linter](https://pep8ci.herokuapp.com/) | X errors. All resolved. |

### Accessibility 

**Lighthouse**
To ensure the front end of my program was accessible I used Lighthouse. 

Here are the results: 
(screenshot)

**Colour Contrast**
I also checked the colour contrast using of my color palette combinations using [Coolors](https://coolors.co/contrast-checker/112a46-acc8e5.)

**Alternative Text**
I ensured I had set alternative text for the only image on my site: the logo. 

## Bugs

Here is the list of bugs mostly found towards the end of development when I encountered functionality not working as intended that I had previously thought did. I don't believe I have left any unresolved bugs. 

### Bug One

#### Issue
About halfway through development, I tried to change the primary key of my 'Project' model from the 'Title' field to a new 'Project ID' field. This was because I had discovered that it is not possible to edit a primary key, so if a user wanted to change the title of their project, they would not be able to do so. Whilst making this change, I also found that Django automatically assigns an auto-incrementing ID to every model you create. I may have learnt this at some point, but because this auto-assignment is implicit and not actually visible in the files I was working on, I did not realise. 

I had to delete the ID fields from all my models and recreate my database. The issue this ultimately created was that I had been working for quite some time on the original data models and they were intertwined throughout my functionality. Making this change broke a significant portion of my existing functionality. 

#### Solution
The solution to this was going through systematically, encountering errors and resolving them until all references to IDs had either been removed or switched to the auto-assigned ones in Django. 

### Bug Two

#### Issue
I noticed that the error message on my login page wasn't working anymore. When incorrect login credentials are entered, the page simply reloads without displaying any error message, leaving the user unaware of why they haven't been logged in. 

#### Solution
The solution involved modifying the template to properly handle and display error messaging when login credentials are incorrect. I previously had a small bit of Javascript at the bottom of the page to handle this, but as it wasn't working, I changed to using Django templating language in the body of the template and it started working again. See related commit for the code change.

### Bug Three

#### Issue
Sorting by project or reporter on the Issues Listing page causes a FieldError: "Cannot resolve keyword 'project.title' into field" and "Cannot resolve keyword 'reporter.username' into field." 

#### Solution

For both of these, I discovered that in Django, you need to use double underscores instead of dots to traverse relationships between models. So because 'Projects' and 'Users' are two separate models from the 'Issue' model which is the main one being used in this table, I needed to use underscores for them, not dots. For example, 'project__title' not 'project.title'.

### Bug Four

#### Issue
When a large amount of text is added to the Issue Description field, it causes the table on the Issue Detail page to go off the right edge of the page.
![Bug 4 Issue Detail](documentation/bug4-issue.png)

It also causes there to be a scroll bar on the Change History page.
![Bug 4 Change History](documentation/bug4-history.png)

#### Solution
I added Bootstrap's text wrapping and word break utilities on the offending table columns. 

This is what they looked like after the change: 
![Bug 4 Issue Fix](documentation/bug4-fix.png)
![Bug 4 History Fix](documentation/bug4-fix2.png)

### Bug Five

#### Issue
A separate issue caused by a large amount of text that persisted after the fix for bug four, was the throwing off of the header row on the Change History table. See solution images in bug four above. 

#### Solution
I added Bootstrap's utility that prevents text wrapping to the whole table heading row. 

![Bug 5 fix](documentation/bug5.png)

### Bug Six

#### Issue
I noticed that instead of values such as 'In Progress' - I could see values formatted as 'in_progress' on the UI. I took a look at my models and I had ordered my choice sets correctly, with the stored value first, then the display value. So it meant that I was showing the stored database values rather than the corresponding display values. Here, the Severity, Type and Status columns are using the stored values as evidence by the lowercase words and underscores.
![Bug 6](documentation/bug6.png)

#### Solution
The solution was to go through the site and find all the places I am displaying such fields and ensure I am using the display values. For example, where I had used `issue.status`, I now used `issue.get_status_display`. This ensured all the display values were being shown on the UI. Here is the same table using the display values: 
![Bug 6 fix](documentation/bug6-fix.png)

### Bug Seven

#### Issue
The sorting by Severity on tables like the Issue Listing page, was not working as expected. The column was being sorted alphabetically rather than by severity. 

#### Solution
I changed the Issue Model's 'Severity' choices to integers and sorted by those instead of the previous names, so the display names remain in the format '1-Critical' but the stored values are just integers, e.g. 1. This solved the issue and allowed the sorting by severity to be accurate. 

### Bug Eight
![Bug 8](documentation/bug8.png)

#### Issue
There was an alert on the Password Reset form page indicating the deletion of a project, which is irrelevant to the scenario. 

#### Solution
I found that I had a block of code implementing alerts on this page. I removed this and that removed the project deletion alert. 

![Bug 8 Fix](documentation/bug8-fix.png)

### Bug Nine

#### Issue
When I finished the main coding of my project and started to go through my files to tidy them all up, I came across my secret ket in my settings file. I had overlooked this throughout development and therefore committed it to GitHub. It was therefore no longer secret. 

#### Solution 
I used [Djecrety](https://djecrety.ir/) to generate a new secret key, placed this in the env file and hooked it up to the settings. This reinstated this security setting correctly. 

### Bug Ten

#### Issue
After I had finished going through and adding my docstrings and comments, as well as ensuring consistent quote marks and naming across all files, I had accidentally made changes that meant my pie charts and alerts were no longer displaying. 

#### Solution
I found that I had used my IDE to do an automatic format (right-click/format document) and that this had thrown the data and labels off in the code snippet below. Restoring them to this state made my pie charts reappear.

`const labels = {{ labels | safe }};`<br>
`const data = {{ data | safe }};`

I also found that I had somehow duplicated the line below in my alerts.js file. Deleting this made my alerts reappear.

`if (predefinedAlertType) {`

### Bug Eleven

#### Issue
The user details form on the Profile page is not working as expected: the Cancel button saves the form rather than cancelling any changes. 

#### Solution
I made a change so that the Cancel button simply refreshes the Profile page, thus effectively removing any changes and setting the form back to non-edit mode. 

### Bug Twelve

#### Issue
Alerts are eroneously showing up in three different scenarios: 
1. When a user goes to the 'Change Password' form from the Profile page and clicks the 'Save' button, the 'successfully changed password' alert appears on the next page the user accesses that has an alert placeholder on it, regardless of if they actually changed their password or not. 
2. When a user uses the 'Create Issue' form without adding all mandatory information and clicks the 'Save' button, receives validation errors, then decides not to create a new issue and cancels, the 'created a new issue' alert appears anyway. 
3. When a user uses the 'Create Project' form without filling the field in and clicks the 'Save' button, receives a validation error, then decides not to create a new project and cancels, the 'created a new project' alert appears anyway. 

#### Solution
I found that I had set up the alerts to be triggered when clicking the button, rather than when the new item is actually saved. I removed this behaviour from the buttons and switched to setting the session variable in the view when the new item is saved successfully. This meant that I moved the session variable to the server side and therefore needed to pass it to the client side via the context on each page that displays the alerts. This solved all three scenarios. 

### Bug Thirteen

#### Issue
I made a change that removed the 'Status' field from the form used to create a new issue. This is because when an issue is created it should automatically be set to 'Open' and not be changeable at this stage. It should however be changeable afterwards, when a user edits an issue. I realised I accidentally removed the 'Status' field from both the create and edit issue forms. 

#### Solution
As the same form is used for creating and editing issues, I needed to include the 'Status' field conditionally. So I added the 'Status' field back into the list of fields for this form, then made sure it only appears on the edit issue form by checking whether the issue instance already exists or not. If it does not exist already, this means its a new issue and the status field should not appear, therefore it is removed from the list of fields. 

### Bug Fourteen

#### Issue
The 404 page shows 'Login' in the navbar rather than the full menu that the user needs to use to navigate away from the 404 page. 

#### Solution
When I changed the way my navbar was coded in order to remove repetition whilst ensuring the correct version of the navbar is included in each page, I overlooked the 404 page. I just had to add the correct context to the custom_404 view and this reinstated the full navbar. 

### Bug Fifteen

#### Issue
The Edit Issue page does not show an alert to explain to the user why they cannot change the Status of issues to a particular value. 

#### Solution
I looked back at the changes I made when I first implemented it and I saw that at some point along the way I had lost the section in my Edit Issue template, which displays the alerts. Adding this back in fixed the issue. I also realised that I had duplicate and redundant code in the 'Change Issue Status' view. It was redundant because I had incorporated the functionality into the main 'Edit Issue' view, so I deleted the other view. Also, related to this bug, I saw that in my message to the user about why they couldn't change the status to a particular value, I was showing the internal status values rather than the intended display values, so I changed this too. 

### Bug Sixteen

#### Issue
When a user clicks 'Add a Comment' on an Issue Detail page, without entering any text into the box, the page refreshes and the navbar contains only a link to 'Login' despite the user already being logged in and it having no relevance to the task at hand. 

#### Solution
I made a change so that the 'Add a Comment' button is disabled when there is no text in the comment box. This solves the issue.

### Bug Seventeen

#### Issue
On the Change History page of an Issue, and on the Issue Status Summary report, I was showing the stored database values rather than the corresponding display values. This is the same type of issue as Bug Six. 

![Bug Seventeen](documentation/bug17.png)

#### Solution
For the Change History page, this needed a more in-depth solution in my Change model, where I implemented methods to dynamically fetch and show the display values for various fields based on their defined choices. For the Report, I updated the view to map the status values to their display names before passing them to the pie chart so it could display them correctly. 

![Bug Seventeen Fixed](documentation/bug17-fix.png)

#### Bug Eighteen

#### Issue
After deleting a project, an alert appears on the 'Edit Issue' page when the user next accesses it informing them 'Project Deleted Successfully'. Firstly, a similar alert will have been seen on the Projects page when the user is directed back there after project deletion. Secondly, this alert is not relevant to the Edit Issue page.

![Bug Eighteen](documentation/bug18.png)

#### Solution
I found that I had accidentally left a line of code in my 'Delete Project' view from a previous version of my alerting system that was causing this message to appear. I removed this line and the bug was fixed.

#### Bug Nineteen

#### Issue
This bug contains all the cosmetic issues found on mobile and tablet screens during browser and responsivity testing: 
- a. Burger Menu is aligned right and looks odd.
- b. Buttons on 'Issue Detail' page stuck together on two rows.
- c. Issue Table header row is split across 2 rows when the title column has an entry longer than 15 characters.
- d. 'Select a report' is split over 3 lines in the report area and looks untidy.
- e. 'Edit' and 'Change Password' buttons should be stacked and full width on 'Profile' page when not in edit mode and 'Save Changes' and 'Cancel' buttons should also be stacked and full width when in edit mode, following convention set elsewhere. This should be on mobile screens. 
- f. All buttons on the 'Edit Issue' page should be full width and stacked on tablets as it already is on mobile screens. 
- g. On Chrome and Edge only: the dropdowns on forms have tiny text and float away from their field label.
- h. The pie charts are too small on tablet screens and have a varying amount of padding underneath depending on the various screen sizes. This should be consistent.
- i. The pie charts sometimes had no padding at the bottom of the screen and other times did have it, depending on screen size. This was despite me not specifying padding my screen size.

#### Solution
These have all been solved: 
- a. The burger menu has been changed to an offcanvas navbar using Bootstrap.
- b. The buttons on 'Issue Detail' pages have been converted to 100% width on mobile screens in the same way that other buttons on different pages were already.
- c. The title column has been restricted to 15 characters maximum on smaller screens and left at 50 characters on larger screens. Two columns removed from tablet size screens for the Issue table to help with information spacing on this size screen too. 
- d. This has been renamed 'Select Report'.
- e. These buttons have all been made full width and stacked on mobile and tablet screens.
- f. These buttons have all been made full width and stacked on tablet screens. 
- g. This turned out to be a bug with the Chrome and Edge dev tools mobile emulators. When tested on an actual mobile device, the dropdowns appeared correctly. 
- h. I changed the Bootstrap column settings to increase their sizes on the medium screens. 
- i. I added a class to the appropriate container and added 30px of padding at the bottom of the chart regardless of screen size. 

#### Bug Twenty

#### Issue
It is currently possible to register for an account and use the same email address as an existing user.

#### Solution
I changed my user model to make sure that email addresses must be unique. 

## Deployment
This project was deployed to [Heroku](https://id.heroku.com/login): a hosting platform. 

These are the steps I took to set up my infrastructure and deploy my app:
1.
2.
3.
4.
5.
6.
7.
8. I created a new repository on my GitHub from the [Code Institute template](https://github.com/Code-Institute-Org/p3-template) and named it 'hitch-hound'
9. I opened this repo on my IDE and
10. 
11.
12. Next I clicked on the 'Deploy' tab and connected my github repository code to the Heroku app. I clicked 'Enable Automatic Deploys' and Heroku deployed the app for me. Once this was done, the link to the app appeared and could be clicked to go to the deployed app.

## Agile Methodology
I set this project up in GitHub projects using agile methodology. This facilitated my prioritisation and time management. I added all the user stories as issues and then divided them into 'MVP'(Minimum Viable Product) and 'Future Enhancements' to signify what I intend to complete for my assessed project and what could come later. Those MVP stories were then stack-ranked. I added three one-week sprints to the project and filled my first sprint with my intended work according to the MoSCoW prioritisation system. 

### Sprint One: 05/06 to 11/06
![Sprint One](documentation/sprint1.png)

#### Sprint Planning
Sprint planning involved taking the highest priority issues from the top of the stack and assigning them to the first sprint. I marked the first three as 'Must Have' for this sprint, the next one 'Should Have' and the last two 'Could Have'. This gave me a breakdown of 50% for must, 16.6% for should and 33.4% for could. If I achieve all of these user stories in the first sprint, I will have completed my first epic: User Management.

#### Sprint Retrospective

Sprint Overview: 
During my initial one-week sprint, I completed the user story for 'Create basic front-end'. This task involved laying much of the foundational work for my project.

Achievements: 
- Successfully created the basic front-end.
- Established the groundwork for future development.

Progress:
- Began working on 'User Registration' user story
- Completed the setup of the database schema and models
- Integrated the database with the project

Challenges: 
- Time constraints were more significant than anticipated, affecting my ability to complete all planned tasks

Action Items for Next Sprint: 
- Improve time estimation, including buffer time for unforeseen challenges
- Aim to complete the first epic

### Sprint Two: 12/06 to 18/06
![Sprint Two](documentation/sprint2.png)

#### Sprint Planning
For the second sprint, I carried over the same stories I had planned for the first sprint but not finished. I did not include any more because experience has shown me that I am unlikely to get all these stories finished. Therefore only 40% of the stories are must have, 20% should have and 40% could have. With more time this sprint, I should be able to complete the must have stories at a minimum. 

#### Sprint Retrospective
Achievements: 
- Successfully created the user registration, login and logout.

Progress:
- Began working on 'Password Reset' user story
- Continued learning about Django and how to set up different elements

Challenges: 
- Configuration was not as straightforward as I hoped, so there were a couple of times it felt like 2 steps forward, 1 step back. 

Action Items for Next Sprint: 
- Complete the first epic. Just half a user story left.
- Make a good dent in Epic 2: Issue Management.


### Sprint Three: 19/06 to 25/06
![Sprint Three](documentation/sprint3.png)

#### Sprint Planning
For the third sprint, I carried over one story and put back another story, towards the bottom of the backlog as I realised I would not be able to sort out all the permissions until I had the bulk of the reset of the development complete. 50% of my stories for sprint 3 are must have, 25% should have and 25% could have. If I manage to complete these, I can always pull in some more stories. 

#### Sprint Retrospective
I realised after the sprint had begun, that I needed a user story for creating the user profile page. I'd missed it when initially writing up my user stories. This has a list of issues assigned to the user on it however, so needs to be done later on in the project. I created it and put it further down the backlog. 

I also picked up speed this sprint and completed all four of the planned user stories by the middle of the sprint. I pulled in four more, labelling two of them 'Should Have' and the other two 'Could Have' as I had already met my sprint commitments. 

### Sprint Four: 26/06 to 02/07
![Sprint Four](documentation/sprint4.png)

#### Sprint Planning
For my fourth sprint, I carried over two of the four I pulled in half way through, and added five more stories for a total of 7. I've got 3 must haves, 2 should haves and 2 could haves. I do have quite a large issue to deal with first but I feel as though I am into the flow of how Django works and what my project should do to be able to work with this split. 

#### Sprint Retrospective
I nearly achieved all of my must haves but had to pause to add automated testing to the whole project so far, as I had not added any up to this point. I was very close to finishing the final must have but I had implemented two independent forms on the same page and they were interfering with each other. I think I'll need to split them up so they can be on different pages and not influence each other as they currently do. I also had to replace my database due to having assigned IDs to my models and not realising that Django does this automatically for you. There were significant delays this sprint. 
 
### Sprint Five: 03/07 to 09/07
![Sprint Five](documentation/sprint5.png) 

#### Sprint Planning
I have planned the remainder of my stories into sprint five with 3 must haves, 2 should haves and 2 could haves. If I need a sixth sprint, I will of course carry over any that were not completed this sprint. 

#### Sprint Retrospective
I got through a tremendous amount in this sprint, finishing all but one of my user stories. I could really see how much I had improved from the start of the project as things took me less time to figure out. 

### Sprint Six: 10/07 to 16/07
![Sprint Six](documentation/sprint6.png)

#### Sprint Planning
I have moved my final story over to this sprint, plus added one more 'Add breadcrumbs' as I realise I need them for effective navigation. I will also be refactoring my code, adding more comments and docstrings, as well as finishing off my README this sprint. The goal is to complete my project by the end of it. As such, both the stories in this sprint have been marked as must haves. 

#### Sprint Retrospective
I finished the reporting feature early in the sprint and moved onto the final story: the breadcrumbs. 

As I was implementing the breadcrumb feature, I thought about the breadcrumbs I actually wanted to implement. All top levels of the breadcrumbs could be accessed via the navigation bar, then all but one of the breacrumbs were just two pages deep. They would be mostly duplicating my existing navbar and therefore be presenting duplicate information on the page. I thought this could be confusing for the user and look messy, so I reverted my changes and decided against breadcrumbs after all. 

During this sprint I also concentrated on getting my project to be as non-repetitive as possible. This involved using the django templating more effectively, now that I understood it better. 

I also did a tidy up which included fixing bugs (see dedicated bug section above) and implementing small bits of functionality that I had missed in my main run through of the project: 

- Making the project field on the issue detail clickable to go to that project. 
- Adding a 'You don't have any issues assigned to you.' message on the Profile page. 
- Adding a 'You don't have any notifications yet.' message on the Notifications page. 
- Removing the role dropdown and making the field read-only on the Profile page. 
- Removing the status field from the Create Issue page and auto-populating this value to 'Open'. 

### Future Development
These three stories were nice to haves if I found I had enough time to implement them. They are under Epic 4: Enhanced Issue Management. In the end, I only had enough time to implement the first story in this epic: 'Provide a Change History Log'. I completed all other stories in all other epics. 

- Attach Files to Issues
- Connect 2+ Issues as Related
- Search for Issues by Keyword

I also looked into the possibility of retaining the formatting and line breaks in the Comments, as my program currently removes them upon saving. However, I decided against making any changes because my research indicated that to preserve formatting and lines breaks, the comment text would need to be rendered as HTML. Django automatically escapes HTML to prevent Cross-Site Scripting attacks as a security measure. I don't want to make changes that override Django's security protocols, especially as I don't believe preservation of formatting justifies compromising security measures. 

## Credits

### APIs and Third Party Libraries


### Sources
I referred back to the Code Institute set up videos to remind me how to set up the APIs, credentials and files before starting coding.

- I built my flowcharts using [Mermaid](https://mermaid.js.org/syntax/flowchart.html) in my readme.
- I manipulated my base colour to figure out my colour palette using [MDigi Tools](https://mdigi.tools/desaturate-color/#508072).
- I visually represented my colour palette using [Adobe Colour](https://color.adobe.com/create/color-wheel).
- I sourced my icons from [Font Awesome](https://fontawesome.com/search?q=dog&o=r&m=free)
- I created all my favicons with [Real Favicon Generator](https://realfavicongenerator.net/)
- I used [Chat GPT](https://chatgpt.com) to explain error messages and research the best way to go about my implementation.
- I used [Learn Django](https://learndjango.com/tutorials/django-login-and-logout-tutorial) to help me set up login/logout etc.
- I used [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing) to walk me through testing a Django web app.
- The image of the sad pug on the custom 404 page is from [Unsplash](https://unsplash.com/photos/fawn-pug-lying-on-floor-6x-hVXXiBxs).
- I generated a new secret key using [Djecrety](https://djecrety.ir/).

I also used the documentation of all the elements included in this project: 
- [Django](https://docs.djangoproject.com/en/4.2/)
- [Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
- [PostgreSQL](https://www.postgresql.org/docs/current/)


### General Credit
As ever, I want to thank the open source community for the great resources that teach me so much and also remind me of what I learnt in my Code Institute lessons. 

I believe I have specifically credited where I used specific items in the previous section but this is a general credit to the reference resources I looked through to teach me new elements as well as reminding me how things I'd already come across worked as I went along. 

Every effort has been made to credit everything used, but if I find anything else specific later on that needs crediting, that I missed, I will be sure to add it.