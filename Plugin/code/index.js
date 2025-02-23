// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// <ProgramSnippet>
import { keyInSelect } from 'readline-sync';

import settings from './appSettings.js';
import {
  initializeGraphForUserAuth,
  getUserAsync,
  getUserTokenAsync,
  getInboxAsync,
  sendMailAsync,
  makeGraphCallAsync,
  // makeDraft,
  replyToMessage,
} from "./graphHelper.js";

async function main() {
  console.log('JavaScript Graph Tutorial');

  let choice = 0;

  // Initialize Graph
  initializeGraph(settings);

  // Greet the user by name
  await greetUserAsync();

  // const choices = [
  //   'Display access token',
  //   'List my inbox',
  //   'Send mail',
  //   'Make a Graph call',
  // ];

  const choices = [
    "Display access token",
    "List my inbox",
    "Send mail",
    "Make a Graph call",
    "Make a draft",
    "Reply message",
    "Tufts",
  ];

  while (choice != -1) {
    choice = keyInSelect(choices, 'Select an option', { cancel: 'Exit' });

    switch (choice) {
      case -1:
        // Exit
        console.log("Goodbye...");
        break;
      case 0:
        // Display access token
        await displayAccessTokenAsync();
        break;
      case 1:
        await listInboxAsync();
        break;
      case 2:
        // Send an email message
        await sendMailToSelfAsync();
        break;
      case 3:
        // Run any Graph code
        await doGraphCallAsync();
        break;
      case 4:
        // Send an email message
        console.log('lol');
        // await makeDraft();
        break;
      case 5:
        // Send an email message
        await replyToMessage(
          "AQMkADAwATM3ZmYAZS0wYmNiLTY0YjgtMDACLTAwCgBGAAADF0fjCn2iZUKwYQK-G7761QcAqb-UiJel5U2FW7S7qIGi4AAAAgEMAAAAqb-UiJel5U2FW7S7qIGi4AAHBgCcdAAAAA==",
        );
        break;
      case 6:
        // Send an email message
        await lol();
        break;
      default:
        console.log("Invalid choice! Please try again.");
    }
  }
}

main();

async function lol() {
  try {
    const emailsPage = await getInboxAsync();
    const emails = emailsPage.value;
    const filteredEmails = [];

    // emails.forEach((e) => {
    //   if (
    //     e.from?.emailAddress?.address.endsWith("@tufts.edu") &&
    //     !e.isRead
    //   ) {
    //     filteredEmails.push(e);
    //   }
    // });

    emails.forEach((e) => {
      if (
        e.from?.emailAddress?.address === "Zihan.Yang@tufts.edu" &&
        !e.isRead
      ) {
        filteredEmails.push(e);
      }
    });

    console.log(filteredEmails.length);

    if (filteredEmails.length != 0) {
      const id = filteredEmails[0].id;

      if (id) {
        console.log("send reply");
        await replyToMessage(id);
      } else {
        console.log("no id");
      }
    }
    else {
      console.log("no emails");
    }
  } catch (err) {
    console.log(`Error getting user's inbox: ${err}`);
  }
}
// </ProgramSnippet>

// <InitializeGraphSnippet>
function initializeGraph(settings) {
  initializeGraphForUserAuth(settings, (info) => {
    // Display the device code message to
    // the user. This tells them
    // where to go to sign in and provides the
    // code to use.
    console.log(info.message);
  });
}
// </InitializeGraphSnippet>

// <GreetUserSnippet>
async function greetUserAsync() {
  try {
    const user = await getUserAsync();
    console.log(`Hello, ${user?.displayName}!`);
    // For Work/school accounts, email is in mail property
    // Personal accounts, email is in userPrincipalName
    console.log(`Email: ${user?.mail ?? user?.userPrincipalName ?? ''}`);
  } catch (err) {
    console.log(`Error getting user: ${err}`);
  }
}
// </GreetUserSnippet>

// <DisplayAccessTokenSnippet>
async function displayAccessTokenAsync() {
  try {
    const userToken = await getUserTokenAsync();
    console.log(`User token: ${userToken}`);
  } catch (err) {
    console.log(`Error getting user access token: ${err}`);
  }
}
// </DisplayAccessTokenSnippet>

// <ListInboxSnippet>
async function listInboxAsync() {
  try {
    const messagePage = await getInboxAsync();
    const messages = messagePage.value;

    // Output each message's details
    for (const message of messages) {
      // console.log(`Message: ${message.subject ?? 'NO SUBJECT'}`);
      console.log(`  message: ${JSON.stringify(message)}`);
      // console.log(`  From: ${message.from?.emailAddress?.name ?? 'UNKNOWN'}`);
      // console.log(`  Status: ${message.isRead ? 'Read' : 'Unread'}`);
      // console.log(`  Received: ${message.receivedDateTime}`);
    }

    // If @odata.nextLink is not undefined, there are more messages
    // available on the server
    const moreAvailable = messagePage['@odata.nextLink'] != undefined;
    console.log(`\nMore messages available? ${moreAvailable}`);
  } catch (err) {
    console.log(`Error getting user's inbox: ${err}`);
  }
}
// </ListInboxSnippet>

// <SendMailSnippet>
async function sendMailToSelfAsync() {
  try {
    // Send mail to the signed-in user
    // Get the user for their email address
    const user = await getUserAsync();
    const userEmail = user?.mail ?? user?.userPrincipalName;

    if (!userEmail) {
      console.log("Couldn't get your email address, canceling...");
      return;
    }

    await sendMailAsync('Testing Microsoft Graph', 'Hello world!', userEmail);
    console.log('Mail sent.');
  } catch (err) {
    console.log(`Error sending mail: ${err}`);
  }
}
// </SendMailSnippet>

// <MakeGraphCallSnippet>
async function doGraphCallAsync() {
  try {
    await makeGraphCallAsync();
  } catch (err) {
    console.log(`Error making Graph call: ${err}`);
  }
}
// </MakeGraphCallSnippet>
