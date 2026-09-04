/**
 * HR landing page — chat widget wired to the Copilot Studio HR Agent through the
 * Microsoft 365 Agents SDK Copilot Studio client.
 *
 * Adapted from microsoft/Agents samples/nodejs/copilotstudio-webclient (MIT).
 *
 * The chat is initialised on the FIRST click of the launcher, not on page load:
 * the MSAL sign-in popup must be opened from a user gesture or the browser's
 * popup blocker eats it, and the failure looks like "the widget does nothing".
 */

import {
  CopilotStudioClient,
  CopilotStudioWebChat,
} from '@microsoft/agents-copilotstudio-client'

import { acquireToken } from './acquireToken.js'

const launcher = document.getElementById('chatLauncher')
const panel = document.getElementById('chatPanel')
const closeBtn = document.getElementById('chatClose')
const statusEl = document.getElementById('chatStatus')

let started = false

function setStatus (text) {
  statusEl.textContent = text
  statusEl.hidden = false
}

function clearStatus () {
  statusEl.hidden = true
}

async function startChat () {
  // settings.js is created by each learner from settings.TEMPLATE.js and is not
  // committed. Import it dynamically so a missing file produces a readable
  // message in the widget instead of a dead page.
  let SampleConnectionSettings
  try {
    ({ SampleConnectionSettings } = await import('./settings.js'))
  } catch {
    setStatus(
      'settings.js not found.\n\n' +
      'Copy settings.TEMPLATE.js to settings.js and fill in your ' +
      'environmentId, schemaName, tenantId and appClientId.'
    )
    return
  }

  const settings = new SampleConnectionSettings()

  if (!settings.appClientId || !settings.tenantId) {
    setStatus('settings.js is incomplete — appClientId and tenantId are required.')
    return
  }
  if (!settings.directConnectUrl && (!settings.environmentId || !settings.schemaName)) {
    setStatus(
      'settings.js is incomplete — fill in environmentId and schemaName ' +
      '(Copilot Studio → Settings → Advanced → Metadata), or a directConnectUrl.'
    )
    return
  }
  if (!settings.authority) {
    settings.authority = 'https://login.microsoftonline.com'
  }

  setStatus('Signing you in…')
  const token = await acquireToken(settings)

  setStatus('Connecting to the HR Agent…')
  const client = new CopilotStudioClient(settings, token)

  window.WebChat.renderWebChat(
    {
      directLine: CopilotStudioWebChat.createConnection(client, {
        showTyping: true,
      }),
      styleOptions: {
        accent: '#0f3d5c',
        bubbleFromUserBackground: '#0f3d5c',
        bubbleFromUserTextColor: '#ffffff',
        bubbleBorderRadius: 8,
        bubbleFromUserBorderRadius: 8,
        botAvatarInitials: 'HR',
        hideUploadButton: true,
        sendBoxButtonColor: '#0f3d5c',
      },
    },
    document.getElementById('webchat')
  )

  clearStatus()
  document.querySelector('#webchat > *').focus()
}

launcher.addEventListener('click', () => {
  const opening = panel.hidden
  panel.hidden = !panel.hidden
  if (opening && !started) {
    started = true
    startChat().catch(err => {
      console.error('Failed to initialize:', err)
      started = false // allow a retry on the next open
      setStatus(
        'Could not connect to the HR Agent.\n\n' +
        (err && err.message ? err.message : String(err)) +
        '\n\nClose and reopen the chat to try again. Details are in the browser console.'
      )
    })
  }
})

closeBtn.addEventListener('click', () => {
  panel.hidden = true
})
