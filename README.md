![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Hitch Hound: a lightweight issue-tracker

'Hitch Hound' is built using Django, Python, Bootstrap, JavaScript and PostgreSQL. It is hosted on Heroku.
Automated testing is done with Jest (JavaScript) and Unittest (Python).

(Add responsive screenshot here)

# Table of Contents
1. [Purpose](#purpose)
2. [Requirement Gathering and Planning](#requirement-gathering-and-planning)
    a. [Brief Competitor Analysis and Target Demographic](#brief-competitor-analysis-and-target-demographic)
    b. [Epics and User Stories](#epics-and-user-stories)
    c. [User Journeys](#user-journeys)
3. [Data Design](#data)
    a. [Database Schema](#database-schema)
    b. [Data Manipulation](#data-manipulation)
    c. [Data Validation](#data-validation)
4. [User Interface Design](#user-interface-design)
    a. [Wireframes](#wireframes)
    b. [Colour Scheme](#colour-scheme)
    c. [Icons](#icons)
5. [Testing](#testing)
    a. [Test Plan](#test-plan)
    b. [Automated Testing](#automated-testing)
    c. [Manual Testing](#manual-testing)
    d. [Browser Compatibility and Screen Size Responsiveness](#browser-compatibility-and-screen-size-responsiveness)
    e. [Key Responsiveness Differences](#key-responsiveness-differences)
    f. [Accessibility](#accessibility)
6. [Bugs](#bugs)
7. [Deployment](#deployment)
8. [Agile Methodology](#agile-methodology)
    a. [Sprint One](#sprint-one-2705-to-0206)
    b. [Sprint Two](#sprint-two-0306-to-0906)
    c. [Sprint Three](#sprint-three-1006-to-1606)
9. [Credits](#credits)

## Purpose
The objective of this program is to streamline the process of tracking and communicating about issues and bugs arising in software development projects. It is lightweight and intuitive, providing ample functionality for small to medium enterprises who don't need an elevated level of auditing and oversight. 

## Requirement Gathering and Planning

Before starting the coding for this project, I created a detailed plan including my database schema, user journeys and wireframes.

### Brief Competitor Analysis and Target Demographic
When considering competitors in the realm of issue and bug tracking software, it's helpful to look at some well-known options. Atlassian's Jira is widely recognised for its range of features and flexibility, making it a go-to choice for companies of all sizes. Another popular option is GitHub's issue tracking system, which seamlessly integrates with its version control platform, making it a convenient choice for teams already using GitHub. Additionally, tools like Trello are valued for their user-friendly interface and adaptability, though they do lack some of the specific features tailored for issue tracking. In this landscape, my program intends to stand out by focusing on simplicity and ease of use, making it ideal for small to medium enterprises (SMEs) looking for a straightforward solution without unnecessary complexity. The goal is to provide a practical and efficient tool for managing software development issues, offering a simpler alternative in a market dominated by larger, more complex platforms.

### Epics and User Stories

My user stories can be seen in full in the associated GitHub Project on my repo. This is where all the details, including tasks and acceptance criteria can be seen. These user stories have been assigned to Epics.

I have listed them by title below to show the split between the absolutely necessary user stories for the MVP (Minimum Viable Product) and those that do improve the user experience but are not essential for the first version of my program. 

**MVP**
1. Epic: User Management 
    a. User Registration
    b. User Login and Logout
    c. View and Assign Superuser Status to Users
    d. Add Meaningful 404 Page
2. Epic: Issue Management
    a. Create Issue
    b. Edit Issue
    c. View Issues
    d. Close, Cancel or Delete Issues
    e. Comment on Issues

**Future Enhancements**
3. Epic: Enhanced User Management
    a. Password Reset
    b. Create and Edit Role-Based Permissions
    c. Receive Notifications from Other Users' Actions
4. Epic: Enhanced Issue Management
    a. Attach Files to Issues
    b. Provide a Change History Log
    c. Connect 2+ Issues as Related
    d.Search for Issues by Keyword
5. Epic: Project Management
    a. Create Project
    b. Edit Project
    c. Close, Cancel or Delete Projects
6. Epic: Reporting
    a. Add Reporting
 
### User Journeys

## Data Design

### Database Schema 

### Data Manipulation

### Data Validation

## User Interface Design

### Wireframes

### Colour Scheme 

### Icons

## Testing

### Test Plan

**Continuous Testing**
I developed this program using the 'red, green, refactor' approach

Through a combination of automated testing written using Jest for JavaScript and Unittest for Python, and manual testing from the front-end, I achieved a good coverage of test cases. The code I wrote was also passed through validators/linters at the end to ensure adherance to coding standards and best practices, ultimately aiming for robust and maintainable code.

### Automated Testing

Jest Testing:

Unittest Testing:

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
| Chrome | Mobile |   | |
| | Tablet |  |  |
| | Computer |  |  |
| | Transition Points |  |  |
| Firefox | Mobile |  |  |
| | Tablet |  |  |
| | Computer |  |  |
| | Transition Points |  |  |
| Safari | Mobile |   |   |
| | Tablet | |   |
| | Computer |   |  |
| | Transition Points | |  |
| Edge | Mobile |  |  |
| | Tablet |  |  |
| | Computer |  |  |
| | Transition Points |  |  |

#### Key Responsiveness Differences

The 

### Code Validation

| Language | Validation Method | Outcome |
|---|----|----|
| HTML | [W3C HTML Validator](https://validator.w3.org/) | X errors. All resolved.|
| CSS | [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | X errors. All resolved. |
| JavaScript | [JS Hint](https://jshint.com/) | X errors. All resolved.  |
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

Here is the list of bugs found towards the end of development when I encountered functionality not working as intended that I had previously thought did. I don't believe I have left any unresolved bugs. 

### Bug One

#### Issue

#### Solution

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

### Sprint One: 27/05 to 02/06
![Sprint One](documentation/sprint1.png)

Sprint planning involved taking the highest priority issues from the top of the stack and assigning them to the first sprint. I marked the first two as 'Must Have' for this sprint, the next one 'Should Have' and the last one 'Could Have'. This gave me a breakdown of 50% for must and 25% each for should and could. This seemed like a manageable workload for me. 

In the screenshot, those marked 'Won't Have' are the stories that were deemed to be above and beyond the requirements for an MVP and have been labelled as such to indicate that they will not be included.
### Sprint Two: 03/06 to 09/06

### Sprint Three: 10/06 to 16/06

## Credits

### APIs and Third Party Libraries


### Sources of Learning
I referred back to the Code Institute set up videos to remind me how to set up the APIs, credentials and files before starting coding.

- I built my flowcharts using [Mermaid](https://mermaid.js.org/syntax/flowchart.html) in my readme.

### General Credit
As ever, I want to thank the open source community for the great resources that teach me so much and also remind me of what I learnt in my Code Institute lessons. 

I believe I have specifically credited where I used specific items in the previous section but this is a general credit to the reference resources I looked through to teach me new elements as well as reminding me how things I'd already come across worked as I went along. 

Every effort has been made to credit everything used, but if I find anything else specific later on that needs crediting, that I missed, I will be sure to add it.