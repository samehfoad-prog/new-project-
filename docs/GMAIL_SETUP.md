# Gmail + Google Pub/Sub setup (Step 8)

This guide sets up the email agent: when a new email arrives, Gmail notifies
Google Pub/Sub, the agent fetches the email, and Claude summarizes it.

← Back to the [README](../README.md)

```
New email ─▶ Gmail ─"inbox changed"─▶ Pub/Sub topic ─▶ subscription ─▶ step8_gmail_agent.py
                                                                        │ fetches the email
                                                                        ▼
                                                            Claude: summary + importance
```

- **Pub/Sub** is Google's message delivery service. Gmail publishes a
  message to a **topic** whenever your inbox changes, and your program reads
  those messages from a **subscription**.
- This project uses a **pull** subscription: the program keeps a connection
  open and messages arrive as they happen. It needs no public web address, so
  it works in a Codespace. (A **push** subscription, where Pub/Sub POSTs to your
  URL like a webhook, is for when you deploy to a server such as Cloud Run.)
- The notification only says *"something changed, historyId=12345"*. The agent
  then asks Gmail's history API what was added, and fetches those emails.

## 1. Create a Google Cloud project

1. Open [console.cloud.google.com](https://console.cloud.google.com) and log in
   with your Gmail account.
2. Use an existing project, or click the project picker → **New Project**.
3. Copy the **Project ID** (for example `gmail-agent-123456`).

## 2. Turn on the two APIs

In the search bar, open each of these and click **Enable**:
- **Gmail API**
- **Cloud Pub/Sub API**

## 3. Create the Pub/Sub topic and subscription

1. **Pub/Sub** → **Topics** → **Create topic**.
   - Topic ID: `gmail-notifications`
   - **Untick** "Add a default subscription" → **Create**.
2. On the topic's page, open **Permissions** → **Add principal**:
   - New principal: `gmail-api-push@system.gserviceaccount.com`
   - Role: **Pub/Sub Publisher** → **Save**. This lets Gmail post into your topic.
3. **Subscriptions** → **Create subscription** (or "Add a subscription" on the topic page):
   - Subscription ID: `gmail-notifications-sub`
   - Topic: `gmail-notifications`
   - Delivery type: **Pull** → **Create**.

## 4. Create your login keys (OAuth)

1. Search **Google Auth Platform** (or **OAuth consent screen**) → **Get started**.
   - App name: `gmail-agent`. Support email: your email.
   - Audience: **External** → finish and **Create**.
2. **Audience** → **Test users** → add **your own Gmail address**.
3. **Clients** → **Create client**:
   - Application type: **Desktop app** → **Create** → **Download JSON**.
4. Upload the file into the project folder (in a Codespace, right-click the
   Explorer → **Upload...**) and rename it:

   ```bash
   mv client_secret_*.json credentials.json
   ```

   `credentials.json` is in `.gitignore`, so it is never uploaded to GitHub.

## 5. Run it

1. Set your Project ID in `step8_gmail_agent.py`:

   ```bash
   sed -i 's/your-project-id/YOUR-PROJECT-ID/' step8_gmail_agent.py
   ```

2. Install the libraries and log in once:

   ```bash
   pip install -r requirements.txt
   python step8_gmail_auth.py
   ```

   Open the link, choose your account, and click **Continue**. Google may warn
   that the app isn't verified; that's expected for your own test app. The
   browser then shows "This site can't be reached" at `localhost:8080`, which
   is also expected. Copy that page's **full address** and paste it into the terminal.

3. Start the agent:

   ```bash
   python step8_gmail_agent.py
   ```

4. **Send yourself an email** from another account or your phone. Within a few
   seconds you'll see:

   ```
   📬 Notification for you@gmail.com
   ✉️  Lunch tomorrow?  —  Friend <friend@example.com>
   🤖 Summary: ...
      Importance: medium
      Suggested action: ...
   ```

Press **Ctrl + C** to stop.

## Good to know

- The agent only **reads** email (`gmail.readonly`). It can't send or delete.
- Email content comes from strangers, so the system prompt tells Claude to
  treat it as data and never follow instructions written inside an email.
- Gmail's watch expires after 7 days. The agent renews it every 24 hours while it runs.
- While your OAuth app is in **Testing** mode, Google logs you out after
  7 days. If you see an `invalid_grant` error, run `python step8_gmail_auth.py` again.
- Private files (`credentials.json`, `token.json`, `gmail_state.json`) are in
  `.gitignore`. Never share them or show them in screenshots.
