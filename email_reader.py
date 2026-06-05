def get_or_create_label(service, label_name="Task-Extracted"):
    try:
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
        for label in labels:
            if label["name"].lower() == label_name.lower():
                return label["id"]
        
        new_label = service.users().labels().create(
            userId="me",
            body={
                "name": label_name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show"
            }
        ).execute()
        return new_label["id"]
    except Exception as e:
        print(f"Failed to get or create label '{label_name}': {e}")
        return None


def get_unprocessed_emails(service):

    results = service.users().messages().list(
        userId="me",
        q="label:INBOX -label:Task-Extracted",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        snippet = message.get("snippet", "")

        emails.append({
            "id": msg["id"],
            "snippet": snippet
        })

    return emails


def mark_as_processed(service, message_id, label_id):
    if not label_id:
        return
    try:
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": [label_id]}
        ).execute()
    except Exception as e:
        print(f"Failed to mark email {message_id} as processed: {e}")
