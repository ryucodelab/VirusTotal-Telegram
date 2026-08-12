from modules.language import get_text



# ==================================
# FORMAT SCAN RESULT
# ==================================


def format_scan(
    result,
    language="en"
):


    filename = result.get(
        "file_name",
        get_text(
            language,
            "unknown"
        )
    )


    file_type = result.get(
        "file_type",
        get_text(
            language,
            "unknown"
        )
    )


    sha256 = result.get(
        "sha256",
        "-"
    )


    detected = result.get(
        "detected",
        0
    )


    total = result.get(
        "total",
        0
    )


    message_key = result.get(
        "message_key",
        "safe"
    )


    threats = result.get(
        "threats",
        []
    )


    report = result.get(
        "report_url",
        "-"
    )





    text = f"""

📚 <b>{get_text(language, "filename")}:</b>
<i>{filename}</i>


📦 <b>{get_text(language, "type")}:</b>
<i>{file_type}</i>


🔐 <b>{get_text(language, "hash")}:</b>
<code>{sha256}</code>


🧪 <b>{get_text(language, "detected")}:</b>
<i>{detected}/{total}</i>


{get_text(language, message_key)}

"""





    if threats:


        text += f"""

⚠️ <b>{get_text(language, "detected_as")}:</b>

<i>{", ".join(threats)}</i>

"""





    text += f"""

🔗 <b>{get_text(language, "report")}</b>

"""



    return (

        text.strip(),

        report

    )









# ==================================
# FORMAT URL SCAN RESULT
# ==================================


def format_url_scan(
    result,
    language="en"
):


    url = result.get(
        "url",
        "-"
    )


    detected = result.get(
        "detected",
        0
    )


    total = result.get(
        "total",
        0
    )


    message_key = result.get(
        "message_key",
        "safe"
    )


    threats = result.get(
        "threats",
        []
    )


    report = result.get(
        "report_url",
        "-"
    )




    text = f"""

🔗 <b>{get_text(language, "url")}:</b>
<i>{url}</i>


🧪 <b>{get_text(language, "detected")}:</b>
<i>{detected}/{total}</i>


{get_text(language, message_key)}

"""




    if threats:


        text += f"""

⚠️ <b>{get_text(language, "detected_as")}:</b>

<i>{", ".join(threats)}</i>

"""




    text += f"""

🔗 <b>{get_text(language, "report")}</b>

"""



    return (

        text.strip(),

        report

    )




# ==================================
# ERROR FORMAT
# ==================================


def format_error(
    error,
    language="en"
):


    return f"""

❌ <b>{get_text(language, "error")}</b>


<code>{error}</code>

""".strip()