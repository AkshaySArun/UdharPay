# UdharPay AI — Coordinator Guide

## The short explanation

UdharPay AI helps a small shop replace its handwritten credit notebook with a digital khata. The shop can keep customer balances in one place, add entries by typing, a photo, or voice, and prepare respectful payment follow-ups. AI helps read and organize information, but the shopkeeper reviews entries before they are saved. Payments can be tried through Cashfree's sandbox, and verified Cashfree payment notifications update the ledger.

## A simple explanation to say in a meeting

> “Many small shops track customer credit in a paper khata. UdharPay AI helps them move those records into a digital ledger, see what each customer owes, and prepare polite follow-ups. They can enter records manually, upload a khata page, or speak an entry in a supported language. AI suggests the details, and the shopkeeper checks them before saving. For payments, we can demonstrate either Cashfree sandbox checkout, which is a test transaction, or a separate visual demo checkout that never processes a payment. The collections preview is simulated. A separate button can place a real outbound test call through Sarvam Voice Agents.”

## What coordinators can demonstrate

### 1. Open the application

- Sign in with the shop account, or use **Try demo** if demo mode is enabled.
- The demo shop contains sample customers and balances. Treat them as sample records, not real customer accounts.

### 2. Show the customer list and digital khata

- **Customers** shows the people recorded for the shop and their current outstanding balances.
- **Digital Khata** shows credit, payment, and adjustment entries.
- To add an entry manually, choose the customer, enter the amount, select the entry type, and save.
- A credit entry increases the amount owed. A payment entry reduces it.

### 3. Demonstrate AI-assisted record entry

- Upload a clear JPG, PNG, or PDF image/page of a handwritten khata, or record/provide a voice entry from the Voice assistant area.
- Choose the correct language where prompted. Supported voice languages include Hindi, English, Kannada, Tamil, Telugu, and Marathi.
- AI returns suggested names, amounts, dates, and descriptions. Check the suggestions carefully and correct mistakes before approval.
- Nothing from an AI extraction is added to the khata until the merchant approves it.

### 4. Demonstrate collections

- **AI Collections** prioritizes accounts with outstanding balances and can preview a respectful reminder conversation.
- Coordinators can enter a sample customer reply and show how the app categorizes the response.
- Each collection row has a **Call test line** button. It starts a real outbound call to the configured test number (+91 9731914376) through Sarvam Voice Agents, with the selected customer name, shop name, outstanding balance, and preferred language passed to the agent.
- Sarvam handles the live spoken conversation. The **Preview** button remains an in-app simulator and does not call or message anyone.
- Calls are blocked for customers who opted out or have no outstanding balance. Call only numbers you are authorized to contact.
- Live calls require the Sarvam Voice Agents org, workspace, app/version, connection, and caller-number values in `backend/.env`. The deployed agent should use the variables `user_name`, `outstanding_amount`, `due_date`, `payment_link_sent`, `payment_status`, `call_summary`, `commitment_date`, and `disposition` in its conversation instructions.

### 5. Explain the two payment demonstrations

There are two different checkout experiences. Make it clear which one is being shown:

| Option | What happens | Does it move money or update the khata? |
| --- | --- | --- |
| **Open Cashfree checkout** | Creates an order using the configured Cashfree environment and opens Cashfree checkout. The current setup is in sandbox/test mode. | Sandbox testing does not collect real money. The ledger changes only after the backend receives and verifies a valid Cashfree webhook. |
| **Create demo share link → Preview demo checkout** | Opens the app’s local mock checkout screen with UPI, card, and net banking previews, plus simulated success/failure buttons. | No. It does not contact Cashfree, accept payment details, process a payment, or change a balance. |

The demo share link can also be copied or opened as a WhatsApp message draft. The coordinator reviews and sends that draft manually; the app does not send it automatically. A local `localhost` link can only be opened from the same computer unless the frontend is also made reachable to the recipient.

### 6. Show transaction tracking

- **Transactions** lists payment orders and their current statuses alongside khata activity.
- A Cashfree order may stay pending until Cashfree sends a signed webhook and the app verifies it.
- The webhook endpoint currently returns a successful response in the connected setup. Keep the backend and the ngrok tunnel running while testing; Cashfree must be able to reach the tunnel URL.
- A successful browser redirect alone is not proof of payment. Use the verified status shown by the app/Cashfree sandbox.

## Coordinator talking points

- The app is designed to make khata records easier to find and follow up on.
- AI output is a suggestion. A person checks it before it becomes a ledger entry.
- The collections **Preview** screen is only a simulator. **Call test line** places a real outbound call through Sarvam Voice Agents.
- Cashfree checkout is currently for sandbox testing. Do not describe a sandbox transaction as a real customer payment.
- The mock demo checkout is only for showing the screen and user flow. Do not enter real card or UPI details there.
- Before recording real customer data, confirm the shop has permission to use those records and enter accurate information.

## Suggested short demo sequence

1. Open the sample shop and show its dashboard balance.
2. Open a customer and show their balance and khata history.
3. Add one small sample credit entry manually.
4. Upload a sample khata page or dictate a sample entry; review and approve the AI suggestion.
5. Open AI Collections and show a simulated reminder and response. If the Sarvam Voice Agent settings are configured, demonstrate a real test call only to an authorized number.
6. Open Transactions and compare **Open Cashfree checkout** (sandbox provider checkout) with **Create demo share link → Preview demo checkout** (visual-only simulation).

End by reminding the audience that the mock payment is not real, and that a sandbox payment is only a test. A real payment setup requires production Cashfree credentials and a production-ready, publicly reachable webhook configuration.
