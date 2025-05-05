
<h1>Brief description of the system and its purpose</h1>

  

Unisupport aims to reduce the impact of mental health challenges and improve overall well-being of the student population, to provide the best opportunity for success. This project aims to establish a resource for university students that will act as a comprehensive mental health support system throughout their academic journey.

  

The system that has been implemented includes:

1. Messaging system - Student-to-Professional messaging, student chatroom and and AI chatbot assistance: A multi-channel communication system including an AI-powered chatbot for when professionals are unavailable and if students are uncomfortable speaking to a professional, chatrooms for peer support and direct communication with university mental health staff.
    

  

2. Survey and data collection system: Students complete a weekly mental health assessment survey, and data is stored in a database. Each student has a personalised wellbeing profile, and their weekly survey data is analysed and used to provide suggestions that can improve their mental health.
    

  

3. Student-Professional Matching system: Students will be able to connect with qualified mental health professionals, physical health coaches or university staff based on their specific needs and preferences. Students will match with a professional by either manually searching the database or being automatically matched (default).
    

  

<h1>Step-by-step instructions on how to run the project:</h1>

1. Unzip the source code package.
    
2. Create virtual environment
    
3. Install dependencies in requirements.txt
    
4. Create run configuration for Flask, according to the following screenshot:
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfAJYes_zXqwOifDqqXppV-XDbthalVTcw2xFj9fD-39wr7AEVRlfre3c8TDuNrCIXlL_qwQcP0punJkkmvTxV2L-7uXY260MB9Vmhn4IY-77DI3Jp6BMpsB2Gm8tIpbssaKw273Q?key=Qb2wGjcNIQ6pfdgr1ehTenc6)

5. Type “flask shell” in the terminal
    
6. Type “reset_db()” in the terminal
    
7. Click run
    

  

<h1>List of programming languages, frameworks, or tools used:</h1>

  

- Python 3
    
- Flask
    
- SQLAlchemy
    
- HTML,CSS, Javascript
    
- Pytest
    
- Pytest-bdd
    

  
  

<h1>A summary of implemented functionalities;</h1>

  

<h2>Matching System:</h2>

Two key functionalities are implemented, automatic matching and manual matching, both of them are coded following the original requirement. One change was made in automatic matching that is calculating and demonstrating the relevance between students and professionals by taking advantage of a new algorithm. This enhancement improves the system to be more transparent and friendly.

<h2>Messaging system:</h2>
  
The messaging system has two parts: student-to-professional messaging and student chatrooms, as well as an AI-powered chatbot. To facilitate communication between students and professionals, the chat_with_user() function retrieves older messages (if any) and renders them on the frontend, while the send_message() function handles sending messages between users. The student chatroom enables peer-to-peer interaction by allowing all student users to see and send messages in an open space, handled by the student_chat_room() function, which manages both message posting and fetching recent conversations. Implemented test cases cover positive and negative scenarios, including successful chat between existing users and error handling when attempting to chat with non-existent users.

  

The AI-powered chatbot uses a composition relationship as instances of the classes are created each time a user attempts to talk to AI. The chatbot uses a simple keyword-based matching system to provide a response depending on the words detected in the user’s messages. It offers information on how to navigate around the website, how to access other functionalities and provides wellbeing advice to the user. The negative test case results illustrate that the chatbot is capable of handling empty, None and non- string format queries by providing the set response for such scenarios and these three tests are combined into one big test that pytest showed the chatbot passed by 100%. Another functionality that has been implemented is: the chatbot and users chat history is stored both in the live session and the database so the user can see the whole chat history, another functionality relating to this is the new message functionality which deletes the chat history from the both database and live session for the users privacy.

  
<h2>Survey and data collection system:</h2>
The survey system has a weekly survey for students to complete. When a student completes the survey, their wellbeing profile will update with relevant advice for them in order to take better care of their mental health. This works through 4 classes - the student class (which inherits from a general user class); the wellbeing_profile class, which holds information about their wellbeing; and the survey class, which enables the survey feature, and the database accessor class.

  

The pop_up_survey() function creates a pop_up to remind students to complete the survey.

Students then fill out the survey form, which calculates their wellbeing score and generates recommendations. The survey is then added to the database using the db_accessor’s record_student_survey() function, and the student’s wellbeing profile is updated. There is a negative test, test_record_student_survey, which tries to create a survey with incorrect datatypes in the parameters, showing our system can handle this; and a positive test, showing that given parameters that should result in a ‘good’ wellbeing score, a ‘good’ wellbeing score is calculated.

  

<h1>The contribution percentages and the specific work done:</h1>

  

|   |   |   |   |
|---|---|---|---|
|Student name and ID|Contribution as percentage|Specific work done:|Signature|
|Jianfeng Zhai - 2744414|20|Implemented matching system including automatic and manual matching and developed both the positive and negative test cases for this feature..|![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcGtXbM85jShQVu1jczB3J47GKCYROPktKEQjkHJJtqzSH6uuYPJwzDUEOgFluA6DpQsg37iAECKLtzklOz0-fM5pVzIEyF1jVkEDU8xRQh2zEs2ROu4-5eFlzbklqxpdOYNmIZxA?key=Qb2wGjcNIQ6pfdgr1ehTenc6)|
|Brandon Isidro - 2789494|20|Implemented the part of the messaging system responsible for messages sent between users and developed a positive and negative test case for the messaging system.|![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfffhAkMP9rxwJR7AAUdd0a2MsW5nfcEB6N1JlL9EbS7R3V57wT_EwGl7byg5uEtODTu66aPtMaUgq9DQ0d0j1npt02iyKKLfitKQfFZvIJDzzmEakSudd-eFXTnHNOq_E2g9yT?key=Qb2wGjcNIQ6pfdgr1ehTenc6)|
|Davis Gurung - 2878511|20|Developed functionality and calculations of the survey system, wellbeing profile frontend, positive test case for the survey system. Demo video|![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXczYNTqZLKA-8UP-fnfj1Vy8gl8RqrLALorRCndfQ5OepwWCi9YymSPrgW7J0ZPyOZzY1bWfNfhqjTceF9iVWYB6283BQkkqW_goHvmptL1duQn60wiAOgP_lx_q1wUHHGsiOaP?key=Qb2wGjcNIQ6pfdgr1ehTenc6)|
|Matthew Perrett - 19995948|20|Developed database related parts of the survey system and the negative test case for the survey system.|![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeuO5SvW_9BRqayM3sobTJWPm9g5k8hr8igU-fTHNgao5MxuOdSkk0hVk3mojwnExncTk2WrN1RGqeeVMl-Puqvx531drYUyizao0RjND3c8KM8Y4PyWvAduNAPRPmCGU9YWo2_TA?key=Qb2wGjcNIQ6pfdgr1ehTenc6)|
|Rikitha Grewal - 2263797|20|Implemented the ai chatbot feature of the messaging system and developed the negative test case for the messaging system.|![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdQgYYyhtLYGO_rTLuQQ7XaQdUJkIBYWT03uKfpvOxzVW35AQctRPWhuhFsG2z6oPF8KWWWBAbMXbVN5nG6SoUGblkoXyj21Vr_a0iYObzsYzYt5XlERuys5NYyTD_pz7fO04ym2w?key=Qb2wGjcNIQ6pfdgr1ehTenc6)|
