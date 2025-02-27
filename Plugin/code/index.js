// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// <ProgramSnippet>
// import { keyInSelect } from "readline-sync";

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
} from './graphHelper.js';

async function main() {
  console.log('JavaScript Graph Tutorial');

  // Initialize Graph
  initializeGraph(settings);

  // Greet the user by name
  await greetUserAsync();

  // Instead of showing a menu, call `lol()` every 3 seconds
  setInterval(async () => {
    try {
      await lol();
    } catch (error) {
      console.error('Error in periodic execution:', error);
    }
  }, 3000);
}

main();

// <lolFunction>
// This function filters unread emails from @tufts.edu and replies to the first one found.
async function lol() {
  try {
    const emailsPage = await getInboxAsync();
    const emails = emailsPage.value;
    const filteredEmails = [];

    emails.forEach((e) => {
      if (e.from?.emailAddress?.address.endsWith('@tufts.edu') && !e.isRead) {
        filteredEmails.push(e);
      }
    });

    console.log(`Found ${filteredEmails.length} matching email(s).`);

    if (filteredEmails.length !== 0) {
      const id = filteredEmails[0].id;
      const content = filteredEmails[0].bodyPreview;

      if (id) {
        console.log('Sending reply...');
        await replyToMessage(id, content);
      } else {
        console.log('No valid email ID found.');
      }
    } else {
      console.log('No matching emails to reply to.');
    }
  } catch (err) {
    console.log(`Error getting user's inbox: ${err}`);
  }
}
// </lolFunction>

// <InitializeGraphSnippet>
function initializeGraph(settings) {
  initializeGraphForUserAuth(settings, (info) => {
    // Display the device code message to
    // the user. This tells them
    // where to go to sign in and provides the code to use.
    console.log(info.message);
  });
}
// </InitializeGraphSnippet>

// <GreetUserSnippet>
async function greetUserAsync() {
  try {
    const user = await getUserAsync();
    console.log(`Hello, ${user?.displayName}!`);
    // For work/school accounts, email is in mail property
    // Personal accounts, email is in userPrincipalName
    console.log(`Email: ${user?.mail ?? user?.userPrincipalName ?? ''}`);
  } catch (err) {
    console.log(`Error getting user: ${err}`);
  }
}
// </GreetUserSnippet>

// // <DisplayAccessTokenSnippet>
// async function displayAccessTokenAsync() {
//   try {
//     const userToken = await getUserTokenAsync();
//     console.log(`User token: ${userToken}`);
//   } catch (err) {
//     console.log(`Error getting user access token: ${err}`);
//   }
// }
// // </DisplayAccessTokenSnippet>

// // <ListInboxSnippet>
// async function listInboxAsync() {
//   try {
//     const messagePage = await getInboxAsync();
//     const messages = messagePage.value;

//     // Output each message's details
//     for (const message of messages) {
//       // console.log(`Message: ${message.subject ?? 'NO SUBJECT'}`);
//       console.log(`  message: ${JSON.stringify(message)}`);
//       // console.log(`  From: ${message.from?.emailAddress?.name ?? 'UNKNOWN'}`);
//       // console.log(`  Status: ${message.isRead ? 'Read' : 'Unread'}`);
//       // console.log(`  Received: ${message.receivedDateTime}`);
//     }

//     // If @odata.nextLink is not undefined, there are more messages
//     // available on the server
//     const moreAvailable = messagePage["@odata.nextLink"] != undefined;
//     console.log(`\nMore messages available? ${moreAvailable}`);
//   } catch (err) {
//     console.log(`Error getting user's inbox: ${err}`);
//   }
// }
// // </ListInboxSnippet>

// // <SendMailSnippet>
// async function sendMailToSelfAsync() {
//   try {
//     // Send mail to the signed-in user
//     // Get the user for their email address
//     const user = await getUserAsync();
//     const userEmail = user?.mail ?? user?.userPrincipalName;

//     if (!userEmail) {
//       console.log("Couldn't get your email address, canceling...");
//       return;
//     }

//     await sendMailAsync("Testing Microsoft Graph", "Hello world!", userEmail);
//     console.log("Mail sent.");
//   } catch (err) {
//     console.log(`Error sending mail: ${err}`);
//   }
// }
// // </SendMailSnippet>

// // <MakeGraphCallSnippet>
// async function doGraphCallAsync() {
//   try {
//     await makeGraphCallAsync();
//   } catch (err) {
//     console.log(`Error making Graph call: ${err}`);
//   }
// }
// // </MakeGraphCallSnippet>
