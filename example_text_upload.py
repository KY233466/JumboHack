from llmproxy import text_upload

if __name__ == '__main__':
    response = text_upload(text = """
        Once upon a time, in the faraway land of Citrusville, there was a man named Orange Jim.
        Now, Orange Jim wasn't your average Joe—oh no, he was really average in every sense, except for one glaring, fruit-inspired trait: he was the color orange.
        Not just a little orange but a deep, radiant orange, like a tangerine on a sunbeam, or the kind of sunset that makes you question the existence of sunsets.
        """,
        strategy = 'fixed')

    print(response)
