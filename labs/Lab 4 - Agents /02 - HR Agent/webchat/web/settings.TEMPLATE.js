/**
 * Copy this file to settings.js, then fill in the four values below.
 * settings.js is gitignored — every learner's values are their own tenant's.
 *
 * Where each value comes from:
 *   environmentId, schemaName, tenantId — Copilot Studio → HR Agent →
 *     Settings → Advanced → Metadata
 *   appClientId — Microsoft Entra admin center → App registrations →
 *     HR Agent Web Client → Application (client) ID
 */
import { ConnectionSettings } from '@microsoft/agents-copilotstudio-client'

// Stores Copilot Studio client debug logs in localStorage (debug-js format).
window.localStorage.debug = 'copilot-studio-client'

export class SampleConnectionSettings extends ConnectionSettings {
  constructor () {
    super({
      // Environment ID of the Copilot Studio agent (required if directConnectUrl is empty).
      environmentId: '',
      // Schema name of the Copilot Studio agent (required if directConnectUrl is empty).
      schemaName: '',
      // Connection string from Channels → Web app (use this OR environmentId + schemaName).
      directConnectUrl: '',
      // Cloud hosting the Power Platform services. Default "Prod".
      cloud: '',
      // Power Platform API endpoint to use if cloud is "Other".
      customPowerPlatformCloud: '',
      // Type of Copilot Studio agent (Published or Prebuilt). Default "Published".
      copilotAgentType: '',
      // Experimental endpoint header — leave false.
      useExperimentalEndpoint: false
    })
    // Application (client) ID of the Entra app registration used to sign in.
    // Must be in the SAME tenant as the Copilot Studio agent.
    this.appClientId = ''
    // Directory (tenant) ID — must match the agent's tenant.
    this.tenantId = ''
    // Entra login endpoint. Default 'https://login.microsoftonline.com'.
    this.authority = ''
  }
}
