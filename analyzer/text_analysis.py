import string


def print_repeated_words(headers, logger, min_repeats=2 ):
    """
    Prints words that occur more than 'min_repeats' times across the list of headers.
    """
    # We'll convert to lowercase and remove punctuation manually, then count words
    
    all_words = []

    # Prepare a translation table for stripping punctuation
    table = str.maketrans('', '', string.punctuation)

    for header in headers:
        header_lower = header.lower()
        header_clean = header_lower.translate(table)
        words = header_clean.split()
        all_words.extend(words)

    word_counts = {}
    for word in all_words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Print words that appear more than 'min_repeats' times
    found = False
    for word, count in word_counts.items():
        if count > min_repeats:
            logger.info(f"'{word}' occurs {count} times.")
            found = True
    if not found:
        logger.info("No words repeated more than twice.")
