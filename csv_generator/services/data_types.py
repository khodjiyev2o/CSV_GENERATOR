DATA_TYPE_CHOICES = [
        ("Full name", "Full name"),
        ("Name", "Name"),
        ("Last Name", "Last Name"),
        ("Job", "Job"),
        ("Email", "Email"),
        ("Domain name", "Domain name"),
        ("Phone number", "Phone number"),
        ("Company name", "Company name"),
        ("Text", "Text"),
        ("Integer", "Integer"),
        ("Address", "Address"),
        ("Date", "Date"),
        ("Age", "Age"),
    ]

COL_SEP_CHOICES = [
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("\t", "Tab (\t)"),
        (" ", "Space ( )"),
        ("|", "Vertical bar (|)"),
    ]

QUOTE_CHOICES = [
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')"),
    ]


STATUS_CHOICES = [
    ( 'processing', ' Processing ' ),
    ( "ready", " Ready "),
    ( "error", "Error "),
]