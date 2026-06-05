def get_unread_emails(service):

    results = service.users().messages().list(
        userId="me",
        q="is:unread label:INBOX",
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


def mark_as_read(service, message_id):

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()