def get_mood_stats(entries):
    """Return dict % of moods in user's entries for bar width in profile page."""
    entries_count = entries.count()

    if entries_count == 0:
        """Pervent zero division error."""
        entries_count = 1

    mood_stats = {}

    great = entries.filter(mood="great").count()
    mood_stats['great'] = 100 * great / entries_count

    good = entries.filter(mood="good").count()
    mood_stats['good'] = 100 * good / entries_count

    usual = entries.filter(mood="usual").count()
    mood_stats['usual'] = 100 * usual / entries_count

    bad = entries.filter(mood="bad").count()
    mood_stats['bad'] = 100 * bad / entries_count

    terrible = entries.filter(mood="terrible").count()
    mood_stats['terrible'] = 100 * terrible / entries_count

    return mood_stats
