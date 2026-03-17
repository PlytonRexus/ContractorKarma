"""
Fuzzy string matching utilities for contractor and road name matching.
Wraps thefuzz for consistent usage across the pipeline.
"""

import logging

from thefuzz import fuzz

logger = logging.getLogger(__name__)


def fuzzy_match(query, candidates, threshold=85, key=None):
    """
    Find the best fuzzy match for `query` among `candidates`.

    Args:
        query: The string to match.
        candidates: A list of strings or dicts to match against.
        key: If candidates are dicts, the key to extract the string from.
        threshold: Minimum fuzz ratio to accept (0-100). Default 85.

    Returns:
        A tuple of (best_match, score) where best_match is the matching
        candidate (string or dict) and score is the fuzz ratio. Returns
        (None, 0) if no match meets the threshold.
    """
    if not query or not candidates:
        return None, 0

    query_lower = query.strip().lower()
    best_match = None
    best_score = 0

    for candidate in candidates:
        if key is not None:
            candidate_str = candidate.get(key, "")
        else:
            candidate_str = candidate

        if not candidate_str:
            continue

        candidate_lower = candidate_str.strip().lower()

        # Try both token_sort_ratio (handles word reordering) and
        # plain ratio (handles simple typos), take the higher score
        score_plain = fuzz.ratio(query_lower, candidate_lower)
        score_sort = fuzz.token_sort_ratio(query_lower, candidate_lower)
        score = max(score_plain, score_sort)

        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        logger.debug("Fuzzy matched '%s' -> '%s' (score=%d)", query, best_match, best_score)
        return best_match, best_score

    logger.debug("No fuzzy match for '%s' above threshold %d (best=%d)", query, threshold, best_score)
    return None, 0


def fuzzy_match_all(query, candidates, threshold=85, key=None, max_results=5):
    """
    Find all fuzzy matches for `query` above the threshold, sorted by score descending.

    Args:
        query: The string to match.
        candidates: A list of strings or dicts.
        key: If candidates are dicts, the key to extract the string from.
        threshold: Minimum fuzz ratio (0-100).
        max_results: Maximum number of results to return.

    Returns:
        A list of (candidate, score) tuples, sorted by score descending.
    """
    if not query or not candidates:
        return []

    query_lower = query.strip().lower()
    results = []

    for candidate in candidates:
        if key is not None:
            candidate_str = candidate.get(key, "")
        else:
            candidate_str = candidate

        if not candidate_str:
            continue

        candidate_lower = candidate_str.strip().lower()

        score_plain = fuzz.ratio(query_lower, candidate_lower)
        score_sort = fuzz.token_sort_ratio(query_lower, candidate_lower)
        score = max(score_plain, score_sort)

        if score >= threshold:
            results.append((candidate, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:max_results]
