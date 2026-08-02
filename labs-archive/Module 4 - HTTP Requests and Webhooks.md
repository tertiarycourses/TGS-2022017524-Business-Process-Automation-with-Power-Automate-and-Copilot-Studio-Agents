# Module 4: HTTP Requests and Webhooks

## HTTP request

HTTP is the request-and-response protocol used by web applications. A client sends a method, URL, headers and optional body; a server returns a status code, headers and body.

```text
Browser ── POST + JSON ──> Power Automate HTTP trigger
Browser <─ status + JSON ─ Response action
```

Common methods:

- **GET** reads data.
- **POST** submits data or starts work.
- **PUT/PATCH** updates data.
- **DELETE** removes data.

The course websites use POST because they submit a form or prompt.

### Request anatomy

| Part | Purpose | Course example |
|---|---|---|
| **Method** | Describes the operation | `POST` |
| **URL** | Identifies the receiving endpoint | Learner-pasted Power Automate webhook URL |
| **Headers** | Describe the message and optional credentials | Content type |
| **Body** | Carries the submitted data | JSON containing name, email, message or prompt |

### Response anatomy

The receiver returns:

- a **status code**, such as 200 for success or 400 for an invalid request;
- optional response headers; and
- a response body, commonly JSON for the course websites.

The Power Automate **Response** action completes the browser's request. Without a response action, the website may keep waiting or show a timeout even if earlier actions ran.

## Webhook

A webhook is an HTTP endpoint intended to receive event notifications. Power Automate's **When an HTTP request is received** trigger generates a URL after a valid trigger-and-action flow is saved. The website posts JSON to that URL and the flow responds.

> Treat a webhook URL like a secret. Anyone who can call an anonymous endpoint may consume runs or send unwanted data. Use only classroom data, rotate compromised URLs, and apply authentication in production.

## HTTP request versus webhook

HTTP is the general communication protocol. A webhook is a design pattern that uses an HTTP endpoint so one system can notify another when an event occurs.

| HTTP request | Webhook |
|---|---|
| Any client-to-server request | A callback endpoint for event-driven notification |
| May read, submit, update or delete | Usually receives a `POST` when something happens |
| Can be initiated by a browser, app or service | Is registered or shared in advance with the sender |

In Labs 8–10, the website is the HTTP client and the generated Power Automate URL is the webhook endpoint.

## JSON request contract

A request contract defines the property names and value types that both sides expect. For example:

```json
{
  "name": "Jane Tan",
  "email": "jane@example.com",
  "message": "Please contact me."
}
```

The website must send the same property names that the flow reads. Validate required fields and return a limited error message when the contract is not met. Do not echo secrets or internal diagnostic details.

## Course website pattern

Every Day 2 website includes a visible **Webhook URL** field. The learner:

1. Saves the Power Automate flow.
2. Copies the generated HTTP URL.
3. Pastes it into the website.
4. The page stores it locally in that browser.
5. The page sends JSON only when the learner selects Submit or Send.

No lab website contains a hard-coded tenant URL or API key.

## Cross-origin requests

A browser may send a CORS preflight request before POST. The supplied pages send a simple `text/plain` request containing JSON to reduce preflight issues. The Power Automate flow parses the body and returns JSON.

**CORS** is a browser security policy, not an authentication mechanism. Production endpoints still require appropriate identity, authorisation, input validation, throttling and monitoring.

## Minimal secure lifecycle

1. Define and validate the request schema.
2. Authenticate the caller for production use.
3. Validate and minimise input.
4. Call only approved systems.
5. Return a limited response.
6. Log failures without exposing credentials.

**Next:** [Lab 8 — Website HTTP Enquiry](Lab%208%20-%20Website%20HTTP%20Enquiry/index.md)
