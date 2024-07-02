import Levenshtein

def get_likely_titles(user_input, title_list, threshold=0.5, max_suggestions=5):
    """
    Get the closest titles from the list based on the user's input using Levenshtein distance.

    Parameters:
    - user_input (str): The title input by the user.
    - title_list (list of str): The list of available titles.
    - threshold (float): The similarity threshold to consider for suggestions.
    - max_suggestions (int): The maximum number of suggestions to return.

    Returns:
    - list of str: The list of suggested titles.
    """
    suggestions = []
    
    for title in title_list:
        similarity = Levenshtein.ratio(user_input, title)
        if similarity >= threshold:
            suggestions.append((title, similarity))
    
    # Sort suggestions based on similarity
    suggestions.sort(key=lambda x: x[1], reverse=True)
    
    # Return only the titles, limited by max_suggestions
    return [title for title, _ in suggestions[:max_suggestions]]

