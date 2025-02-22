from llmproxy import text_upload

if __name__ == '__main__':
    response = text_upload(text = """

Advising Deans (All Students)

Arts and Sciences BA/BS Students, A–D
Tanesha Leathers, Advising Dean (contact for faculty and parents)

Arts and Sciences BA/BS Students, E–K
Matthew Bellof, Advising Dean (contact for faculty and parents)

Arts and Sciences BA/BS Students, L-Q
Jarvis Chen, Advising Dean (contact for faculty and parents)

Arts and Sciences BA/BS Students, R-Z
Caitlin Casey, Advising Dean (contact for faculty and parents)

Arts and Sciences BFA Students and Combined Degree BA/BFA students
Leah Gadd, Advising Dean (contact for faculty and parents)

Engineering Students, A-Z
Jennifer Stephan, Dean of Academic Advising and Undergraduate Studies (contact for faculty and parents)
Pre-Major Advisor (Arts and Sciences BA/BS and Engineering Students)

You were assigned a Pre-major advisor when you matriculated. If you don't know your advisor, log in to SIS and look under "Academics" on your homepage. You'll find their name and a link to email them directly.
Advising Staff (All Students)

All Arts and Sciences BA/BS Students, A-Z
Ericka Miranda, Senior Academic Advisor
Allison Vander Broek, Senior Academic Advisor

First-Year Engineering Students and All Arts and Sciences to Engineering Internal Transfers
John Gearin, Senior Academic Advisor - Book an Appointment with John!

Upper Class Engineering Students
John O’Keefe, Senior Academic Advisor - Book an Appointment

Arts and Sciences BFA Students
Tobias Bennett, Senior Academic Advisor - Book an Appointment
Stephanie Lam, Senior Academic Advisor - Book an Appointment
Theodore Ogaldez, Senior Academic Advisor - Book an Appointment
        """,
        strategy = 'fixed')

    print(response)
