================================================================================
TuftsAdvisor
================================================================================
Created by: Jumbos: Into the Hackerverse (Katie Yang, Spencer Anderson,
                                          Hanah Kim, Emily Li, Madeline Lei,
                                          Tomas Maranga)
Presented at JumboHack 2025 under the Down the Rabbit Hole track.

Our project is a two-fold solution designed to modernize academic advising.
On one side, we've developed an advising chatbot interface that both students
and advisors can use to get quick, informed responses to academic policy
questions. On the other, we've built an Outlook plugin that leverages our API
and retrieval-augmented generation (RAG) system to automatically generate draft
responses from advisor emails, saving time and ensuring consistency in
communication.

Team Member Contributions:

Katie Yang: 
Spencer Anderson: Worked on retrieveing and sending emails.
Hanah Kim: Chatbot interface.
Emily Li: Lead Designer, created presentation.
Madeline Lei: Working on generating responses for the chatbot
Tomas Maranga: Working on integrating APIs, making our own api routes.

ACKNOWLEDGEMENTS
React & Flask: Robust frameworks, made our frontend/backend development smooth
Microsoft Graph: Providing seamless email integration capabilities
RAG: Used existing RAG model

REFLECTION
From lengthy, confusing degree audits to lists of major requirements, making 
sure you are on the right path to graduate can be confusing. This leads to an
influx of repetitive emails for academic advisors and distress for students. We
wanted to create a solution to help students and advisors navigate their
academic journey here at Tufts.

In the future, we'd like to integrate it into an Outlook add-in with a 
Microsoft Graph API webhook to automatically detect new emails rather than
using a script to continuously check.

Some challenges we faced:
- Figuring out how to train the model so it consistently replies professionally
  but not too bot like
- Separating each question to generate a response to, and recombining the
  responses into one email.
- Working with unfamiliar tools
- Setting up the environment
- Navigating Microsoft tools / documentation 