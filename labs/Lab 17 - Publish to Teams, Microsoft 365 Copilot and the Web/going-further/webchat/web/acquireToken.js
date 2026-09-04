/**
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License.
 *
 * From microsoft/Agents samples/nodejs/copilotstudio-webclient, unmodified.
 *
 * Acquires a user token for the Copilot Studio agent: silently if the browser
 * already holds a session for this app registration, otherwise via the MSAL
 * sign-in popup. The scope is derived from the connection settings — it is the
 * Power Platform API's CopilotStudio.Copilots.Invoke delegated permission.
 */

import { CopilotStudioClient } from '@microsoft/agents-copilotstudio-client'

export async function acquireToken (settings) {
  const msalInstance = new window.msal.PublicClientApplication({
    auth: {
      clientId: settings.appClientId,
      authority: `${settings.authority}/${settings.tenantId}`,
    },
  })

  await msalInstance.initialize()
  const loginRequest = {
    scopes: [CopilotStudioClient.scopeFromSettings(settings)],
    redirectUri: window.location.origin,
  }

  // When there are no accounts or acquireTokenSilent fails,
  // fall back to loginPopup.
  try {
    const accounts = await msalInstance.getAllAccounts()
    if (accounts.length > 0) {
      const response = await msalInstance.acquireTokenSilent({
        ...loginRequest,
        account: accounts[0],
      })
      return response.accessToken
    }
  } catch (e) {
    if (!(e instanceof window.msal.InteractionRequiredAuthError)) {
      throw e
    }
  }

  const response = await msalInstance.loginPopup(loginRequest)
  return response.accessToken
}
