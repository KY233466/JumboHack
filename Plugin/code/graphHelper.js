// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// <UserAuthConfigSnippet>
import 'isomorphic-fetch';
import { DeviceCodeCredential } from '@azure/identity';
import { Client } from '@microsoft/microsoft-graph-client';
import axios from 'axios';
import { TokenCredentialAuthenticationProvider } from '@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials/index.js';

let _settings = undefined;
let _deviceCodeCredential = undefined;
let _userClient = undefined;

export function initializeGraphForUserAuth(settings, deviceCodePrompt) {
  // Ensure settings isn't null
  if (!settings) {
    throw new Error('Settings cannot be undefined');
  }

  _settings = settings;

  _deviceCodeCredential = new DeviceCodeCredential({
    clientId: settings.clientId,
    tenantId: settings.tenantId,
    userPromptCallback: deviceCodePrompt,
  });

  const authProvider = new TokenCredentialAuthenticationProvider(
    _deviceCodeCredential,
    {
      scopes: settings.graphUserScopes,
    },
  );

  _userClient = Client.initWithMiddleware({
    authProvider: authProvider,
  });
}
// </UserAuthConfigSnippet>

// <GetUserTokenSnippet>
export async function getUserTokenAsync() {
  // Ensure credential isn't undefined
  if (!_deviceCodeCredential) {
    throw new Error('Graph has not been initialized for user auth');
  }

  // Ensure scopes isn't undefined
  if (!_settings?.graphUserScopes) {
    throw new Error('Setting "scopes" cannot be undefined');
  }

  // Request token with given scopes
  const response = await _deviceCodeCredential.getToken(
    _settings?.graphUserScopes,
  );
  return response.token;
}
// </GetUserTokenSnippet>

// <GetUserSnippet>
export async function getUserAsync() {
  // Ensure client isn't undefined
  if (!_userClient) {
    throw new Error('Graph has not been initialized for user auth');
  }

  // Only request specific properties with .select()
  return _userClient
    .api('/me')
    .select(['displayName', 'mail', 'userPrincipalName'])
    .get();
}
// </GetUserSnippet>

// <GetInboxSnippet>
export async function getInboxAsync() {
  // Ensure client isn't undefined
  if (!_userClient) {
    throw new Error('Graph has not been initialized for user auth');
  }

  return (
    _userClient
      .api('/me/mailFolders/inbox/messages')
      // .select(['from', 'isRead', 'receivedDateTime', 'subject'])
      // .filter("startsWith(subject,'Test')")
      .top(6)
      .orderby('receivedDateTime DESC')
      .get()
  );
}

export async function sendMailAsync(subject, body, recipient) {
  // Ensure client isn't undefined
  if (!_userClient) {
    throw new Error('Graph has not been initialized for user auth');
  }

  // Create a new message
  const message = {
    //   subject: subject,
    //   body: {
    //     content: body,
    //     contentType: 'text',
    //   },
    //   toRecipients: [
    //     {
    //       emailAddress: {
    //         address: recipient,
    //       },
    //     },
    //   ],
    // };
    // {
    subject: 'Test Email',
    body: {
      contentType: 'Text',
      content: 'Hello, this is a test email.',
    },
    toRecipients: [
      {
        emailAddress: {
          address: recipient,
        },
      },
    ],
  };

  // Send the message
  return _userClient.api('me/sendMail').post({
    message: message,
  });
}

export async function editDraftEmail(id, reply) {
  // Ensure client isn't undefined
  if (!_userClient) {
    throw new Error('Graph has not been initialized for user auth');
  }

  const header = 'Hi Katie,\n\n';
  const ender = '\n\nBest,\nGwen';
  const finalReply = header + reply + ender;

  const message = {
    body: {
      contentType: 'Text',
      content: finalReply,
    },
  };

  const path = '/me/messages/' + id;

  await _userClient.api(path).update(message);
}

export async function replyToMessage(id, content) {
  // Ensure client isn't undefined
  if (!_userClient) {
    throw new Error('Graph has not been initialized for user auth');
  }

  const path = '/me/messages/' + id + '/createReply';

  // Send the message
  const result = await _userClient
    .api(path)
    .post({ comment: 'Generating reply...' });
  let finalReply = '';

  try {
    console.log('start to get reply');
    const response = await axios.post(
      'http://127.0.0.1:5000/api/advising/batch',
      { email: content },
      { timeout: 60000 },
    );
    let finalResponse = response.data.final_response;
    if (!finalResponse || finalResponse.includes('An error occurred')) {
      finalResponse =
        'An error occurred processing your query. Please try again.';
    }
    finalReply = finalResponse;

    console.log('reply fetched');

    return editDraftEmail(result.id, finalReply);
  } catch (error) {
    console.error('Error processing query:', error);
    return false;
  }
}
// </SendMailSnippet>

// <MakeGraphCallSnippet>
// This function serves as a playground for testing Graph snippets
// or other code
export async function makeGraphCallAsync() {
  // INSERT YOUR CODE HERE
}
// </MakeGraphCallSnippet>
