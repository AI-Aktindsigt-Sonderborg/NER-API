def remove_inner_annotations(match_list):
    # Sort the match_list by the length of annotations, longest annotations first.
    match_list = sort_annotations_by_length(match_list)
    # Create a list to keep track of matches that are considered illegal (inner annotations).
    illegal_matches = []
    
    # Iterate over the sorted list to find inner annotations.
    for outer_match in match_list:
        # Only consider this outer_match if it's not already marked as illegal.
        if outer_match not in illegal_matches:
            for inner_match in match_list:
                # Check that we are not comparing the same match and it's not already illegal.
                if outer_match is not inner_match and inner_match not in illegal_matches:
                    # Check if the inner_match is within the bounds of the outer_match.
                    if (outer_match['offset'][0] <= inner_match['offset'][0] and
                        outer_match['offset'][1] >= inner_match['offset'][0]) or \
                       (outer_match['offset'][0] <= inner_match['offset'][1] and
                        outer_match['offset'][1] >= inner_match['offset'][1]):
                        # If it is within bounds, add it to the list of illegal matches.
                        illegal_matches.append(inner_match)
    
    # Remove all illegal matches from the match list.
    for illegal_match in illegal_matches:
        match_list.remove(illegal_match)
    # Return the cleaned list of matches.
    return match_list


def sort_annotations_by_length(match_list):
    # Sort the matches by the length of the match, from longest to shortest.
    sorted_list = sorted(match_list, key=lambda x: abs(x['offset'][1] - x['offset'][0]), reverse=True)
    return sorted_list
