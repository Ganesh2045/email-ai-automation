# ⚡ EmailTask AI Automation & Dashboard

An intelligent, AI-powered automation pipeline that periodically checks your Gmail inbox, uses **Gemini 2.5 Flash** to extract actionable tasks, logs them to a **Google Sheet** database, and serves a **premium glassmorphic web dashboard** for real-time task management.

---

## 📐 System Architecture

This system operates in two core cycles: the **AI Ingestion Pipeline** (GitHub Actions cron job) and the **Task Management Dashboard** (local Flask web app).

```mermaid
graph TD
    %% Ingestion Pipeline %%
    subgraph Ingestion Pipeline (Every 10 Mins)
        G[Gmail Inbox] -->|1. Fetch INBOX -label:Task-Extracted| P(main.py)
        P -->|2. Extract actionable tasks| GEM[Gemini 2.5 Flash API]
        GEM -->|3. Clean bullet items & format| P
        P -->|4. Log new tasks as 'Pending'| GS[Google Sheets Database]
        P -->|5. Tag email with 'Task-Extracted'| G
    end

    %% Web App Dashboard %%
    subgraph Task Management Dashboard
        U[User Browser] <-->|Rest API requests| FA[Flask app.py Server]
        FA <-->|gspread reads/writes| GS
    end

    %% Styles %%
    classDef blue fill:#1e1b4b,stroke:#4f46e5,stroke-width:2px,color:#f8fafc;
    classDef purple fill:#311042,stroke:#8b5cf6,stroke-width:2px,color:#f8fafc;
    classDef green fill:#062f22,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    
    class G,GEM,GS blue;
    class P,FA purple;
    class U green;
```

---

## ✨ Core Features

*   **Intelligent AI Extraction:** Powered by `gemini-2.5-flash` to extract high, medium, and low priority tasks from incoming emails.
*   **Inbox-State Tracking:** Transitioned from read/unread status to Gmail labels. Processing applies a `Task-Extracted` label so that read/unread emails are both evaluated while preventing duplicate processing.
*   **Prevent Duplicate Insertions:** The Google Sheet writer verifies the task text before writing to prevent duplicate rows.
*   **Premium Web Dashboard:** A beautiful glassmorphic dark-theme UI with:
    *   **Live Metrics:** Total, pending, and completed task counters.
    *   **Filter & Search:** Real-time search matching and priority level sorting (High 🔴, Medium 🟡, Low 🟢).
    *   **Full CRUD Actions:** Click checkboxes to toggle status, delete tasks, or manually append new ones. All changes sync with Google Sheets.

---

## 📁 File Structure

```text
email-ai-automation/
├── .github/workflows/
│   └── automation.yml       # Scheduled GitHub Action pipeline
├── static/
│   ├── css/style.css        # Dashboard Glassmorphic CSS styling
│   └── js/script.js         # Frontend UI & API controller logic
├── templates/
│   └── index.html           # Main HTML Dashboard Layout
├── app.py                   # Flask server exposing REST API endpoints
├── main.py                  # Core automation script triggered by Actions
├── email_reader.py          # Gmail client functions (fetching & labeling)
├── task_extractor.py        # Gemini client tasks extraction & text cleaning
├── sheet_writer.py          # Google Sheets logging database writer
├── config.py                # Environment configuration constants
├── generate_token.py        # Desktop helper to authorize user scopes
├── requirements.txt         # Project package dependencies
└── .gitignore               # Protects API keys and JSON credentials
```

---

## 🚀 Getting Started (Local Setup)

### 1. Prerequisites & GCP Setup
1.  **Google Cloud Project:** Create a project, enable the **Gmail API**, **Google Sheets API**, and **Google Drive API**.
2.  **OAuth Credentials:** Generate a Desktop OAuth Client ID credential, download the JSON, rename it to `credentials.json`, and place it in the root folder.
3.  **Service Account:** Create a Service Account, generate a JSON Key, rename it to `service_account.json`, and place it in the root folder. 
4.  **Google Sheet:** Create a Google Sheet named `EmailTasks` and share it with the service account email client address as an Editor.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/Ganesh2045/email-ai-automation.git
cd email-ai-automation
pip install -r requirements.txt
```

### 3. Generate OAuth User Token
Run the authentication script to authorize your user email for reading and modifying labels:
```bash
python generate_token.py
```
This launches a browser consent flow and generates `token.json`.

### 4. Running the Web Dashboard
Start the local server:
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

---

## 🤖 GitHub Actions Workflow Configuration

To run the ingestion pipeline continuously in the cloud, you need to configure the following Secrets in your GitHub Repository settings (**Settings > Secrets and variables > Actions**):

| Secret Name | Value Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key |
| `GOOGLE_CREDENTIALS` | The content of your `credentials.json` |
| `TOKEN_JSON` | The content of your generated `token.json` |
| `SERVICE_ACCOUNT` | The content of your `service_account.json` |

---

## 🛠️ Built With
*   **Backend:** Python 3, Flask, `gspread` (Google Sheets client), Google APIs client.
*   **AI:** Google GenAI SDK (`gemini-2.5-flash`).
*   **Frontend:** Semantic HTML5, Vanilla CSS (Glassmorphism design system), Vanilla Javascript (ES6).
