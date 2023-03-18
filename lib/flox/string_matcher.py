from dataclasses import dataclass, field
from typing import List

SPACE_CHAR: str = ' '
QUERY_SEARCH_PRECISION = {
    'Regular': 50,
    'Low': 20,
    'None': 0
}
DEFAULT_QUERY_SEARCH_PRECISION = QUERY_SEARCH_PRECISION['Regular']

"""
This is a python copy of Flow Launcher's string matcher.
I take no credit for the algorithm, I just translated it to python.
"""


@dataclass
class MatchData:
    """Match data"""
    matched: bool
    score_cutoff: int
    index_list: List[int] = field(default_factory=list)
    score: int = 0


def string_matcher(query: str, text: str, ignore_case: bool = True, query_search_precision: int = DEFAULT_QUERY_SEARCH_PRECISION) -> MatchData:
    """Compare query to text"""
    if not text or not query:
        return MatchData(False, query_search_precision)

    query = query.strip()

    current_acronym_query_index = 0
    acronym_match_data: List[int] = []
    acronyms_total_count: int = 0
    acronyms_matched: int = 0

    full_text_lower: str = text.lower() if ignore_case else text
    query_lower: str = query.lower() if ignore_case else query

    query_substrings: List[str] = query_lower.split(' ')
    current_query_substring_index: int = 0
    current_query_substring = query_substrings[current_query_substring_index]
    current_query_substring_char_index = 0

    first_match_index = -1
    first_match_index_in_word = -1
    last_match_index = 0
    all_query_substrings_matched: bool = False
    match_found_in_previous_loop: bool = False
    all_substrings_contained_in_text: bool = True

    index_list: List[int] = []
    space_indices: List[int] = []
    for text_index in range(len(full_text_lower)):
        if current_acronym_query_index >= len(query_lower) and acronyms_matched == len(query_lower):

            if is_acronym_count(full_text_lower, text_index):
                acronyms_total_count += 1
                continue

        if current_acronym_query_index >= len(query_lower) or current_acronym_query_index >= len(query_lower) and all_query_substrings_matched:
            break

        if full_text_lower[text_index] == SPACE_CHAR and current_query_substring_char_index == 0:
            space_indices.append(text_index)

        if is_acronym(text, text_index):
            if full_text_lower[text_index] == query_lower[current_acronym_query_index]:
                acronym_match_data.append(text_index)
                acronyms_matched += 1
                current_acronym_query_index += 1

        if is_acronym_count(text, text_index):
            acronyms_total_count += 1

        if all_query_substrings_matched or full_text_lower[text_index] != current_query_substring[current_query_substring_char_index]:
            match_found_in_previous_loop = False
            continue

        if first_match_index < 0:
            first_match_index = text_index

        if current_query_substring_char_index == 0:
            match_found_in_previous_loop = True
            first_match_index_in_word = text_index
        elif not match_found_in_previous_loop:
            start_index_to_verify = text_index - current_query_substring_char_index

            if all_previous_chars_matched(start_index_to_verify, current_query_substring_char_index, full_text_lower, current_query_substring):
                match_found_in_previous_loop = True
                first_match_index_in_word = start_index_to_verify if current_query_substring_index == 0 else first_match_index

                index_list = get_updated_index_list(
                    start_index_to_verify, current_query_substring_char_index, first_match_index_in_word, index_list)

        last_match_index = text_index + 1
        index_list.append(text_index)

        current_query_substring_char_index += 1

        if current_query_substring_char_index == len(current_query_substring):
            all_substrings_contained_in_text = match_found_in_previous_loop and all_substrings_contained_in_text

            current_query_substring_index += 1

            all_query_substrings_matched = all_query_substrings_matched_func(
                current_query_substring_index, len(query_substrings))

            if all_query_substrings_matched:
                continue

            current_query_substring = query_substrings[current_query_substring_index]
            current_query_substring_char_index = 0

    if acronyms_matched > 0 and acronyms_matched == len(query):
        acronyms_score: int = acronyms_matched * 100 / acronyms_total_count

        if acronyms_score >= query_search_precision:
            return MatchData(True, query_search_precision, acronym_match_data, acronyms_score)

    if all_query_substrings_matched:

        nearest_space_index = calculate_closest_space_index(
            space_indices, first_match_index)

        score = calculate_search_score(query, text, first_match_index - nearest_space_index - 1,
                                       space_indices, last_match_index - first_match_index, all_substrings_contained_in_text)

        return MatchData(True, query_search_precision, index_list, score)

    return MatchData(False, query_search_precision)


def calculate_search_score(query: str, text: str, first_index: int, space_indices: List[int], match_length: int, all_substrings_contained_in_text: bool):
    score = 100 * (len(query) + 1) / ((1 + first_index) + (match_length + 1))

    if first_index == 0 and all_substrings_contained_in_text:
        score -= len(space_indices)

    if (len(text) - len(query)) < 5:
        score += 20
    elif (len(text) - len(query)) < 10:
        score += 10

    if all_substrings_contained_in_text:
        count: int = len(query.replace(' ', ''))
        threshold: int = 4
        if count <= threshold:
            score += count * 10
        else:
            score += threshold * 10 + (count - threshold) * 5

    return score


def get_updated_index_list(start_index_to_verify: int, current_query_substring_char_index: int, first_matched_index_in_word: int, index_list: List[int]):
    updated_list: List[int] = []

    for idx, item in enumerate(index_list):
        if item >= first_matched_index_in_word:
            index_list.pop(idx)

    updated_list.extend(index_list)

    for i in range(current_query_substring_char_index):
        updated_list.append(start_index_to_verify + i)

    return updated_list


def all_query_substrings_matched_func(current_query_substring_index: int, query_substrings_length: int) -> bool:
    return current_query_substring_index >= query_substrings_length


def all_previous_chars_matched(start_index_to_verify: int, current_query_substring_char_index: int, full_text_lower: str, current_query_substring: str) -> bool:
    all_match = True
    for i in range(current_query_substring_char_index):
        if full_text_lower[start_index_to_verify + i] != current_query_substring[i]:
            all_match = False

    return all_match


def is_acronym(text: str, text_index: int) -> bool:
    if is_acronym_char(text, text_index) or is_acronym_number(text, text_index):
        return True
    return False


def is_acronym_count(text: str, text_index: int) -> bool:
    if is_acronym_char(text, text_index):
        return True
    if is_acronym_number(text, text_index):
        return text_index == 0 or text[text_index - 1] == SPACE_CHAR

    return False


def is_acronym_char(text: str, text_index: int) -> bool:
    return text[text_index].isupper() or text_index == 0 or text[text_index - 1] == SPACE_CHAR


def is_acronym_number(text: str, text_index: int) -> bool:
    return text[text_index].isdigit()


def calculate_closest_space_index(space_indices: List[int], first_match_index: int) -> int:

    closest_space_index = -1

    for i in space_indices:
        if i < first_match_index:
            closest_space_index = i
        else:
            break

    return closest_space_index
