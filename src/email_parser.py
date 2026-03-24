def parse_email(email_text):
    if not email_text:
        return {
            "subject": None,
            "body": ""
        }

    email_text = email_text.strip()

    return {
        "subject": None,
        "body": email_text
    }


# -----------------------------
# Empty functions that needs to work on
# -----------------------------

def clean_email_text(email_text):
    #Add logic
    pass


def extract_links(email_text):
     #Add logic
    pass


def extract_email_addresses(email_text):
     #Add logic
    pass


def extract_subject(email_text):
   #Add logic
    pass