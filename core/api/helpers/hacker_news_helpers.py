import random
from core.logconfig import get_logger

logger = get_logger(__name__)


def get_first_story_comments(client, item_ids: list, comments: bool = True):
    """
    Iterate through top stories list and find the first available story.
    
    Args:
        client: HackerNewsClient instance to fetch items
        item_ids: List of integer story IDs (e.g., from get_top_stories().json())
        comments: If True, return first story with comments. If False, return first story without comments.
    
    Returns:
        dict: The first story matching the comments criteria
    
    Raises:
        RuntimeError: If no story matching the criteria is found
    """
    for item_id in item_ids:
        story = client.get_item(item_id=item_id).json()

        # Skip if story is None (non-existent item)
        if story is None:
            continue

        # Check if story has comments
        has_comments = 'kids' in story and story.get('kids')
        
        # Return story based on comments parameter
        if comments and has_comments:
            logger.info(f"Found story with comments id: {item_id}")
            return story
        elif not comments and not has_comments:
            logger.info(f"Found story without comments id: {item_id}")
            return story

    error_msg = (
        "No story with comments found in the provided list of top stories"
        if comments
        else "No story without comments found in the provided list of top stories"
    )
    raise RuntimeError(error_msg)


def get_first_deleted_comment(client, comment_ids: list) -> dict:
    """
    Find the first deleted comment from a list of comment IDs.

    Returns:
        dict: The first deleted comment found, or None if not found
    """
    for comment_id in comment_ids:
        comment = client.get_item(item_id=comment_id).json()

        # Skip if comment is None (non-existent item)
        if comment is None:
            continue

        # Check if comment is deleted
        if comment.get('deleted') is True:
            logger.info(f"Found deleted comment id: {comment_id}")
            return comment

    return None

def assert_top_stories_response(response: list):
    """
    Validate that the top stories response is a list of integers.
    
    """
    assert len(response) > 0, "Response list cannot be empty"
    assert len(response) <= 500, f"Response list length {len(response)} exceeds maximum of 500"
    
    # Sample 3 random items (or all items if list has fewer than 3)
    sample_size = min(3, len(response))
    sampled_items = random.sample(response, sample_size)
    
    for item in sampled_items:
        assert isinstance(item, int), (
            f"Item is not an integer: "
            f"got {type(item).__name__} ({item})"
        )


def assert_item_top_story_response(response: dict):
    """
    Validate that the item response has correct structure and data types.
    
    Based on the official Hacker News API specification:
    https://github.com/HackerNews/API#items
    """
    
    # Required fields (per Hacker News API spec: https://github.com/HackerNews/API#items)
    assert 'id' in response, "Missing required field 'id'"
    assert isinstance(response['id'], int), f"Field 'id' must be int, got {type(response['id']).__name__}"
    
    assert 'type' in response, "Missing required field 'type'"
    assert isinstance(response['type'], str), f"Field 'type' must be str, got {type(response['type']).__name__}"
    
    assert 'time' in response, "Missing required field 'time'"
    assert isinstance(response['time'], int), f"Field 'time' must be int, got {type(response['time']).__name__}"
    
    # Optional fields (validate type if present)
    if 'by' in response:
        assert isinstance(response['by'], str), f"Field 'by' must be str, got {type(response['by']).__name__}"
    
    if 'title' in response:
        assert isinstance(response['title'], str), f"Field 'title' must be str, got {type(response['title']).__name__}"
    
    if 'score' in response:
        assert isinstance(response['score'], int), f"Field 'score' must be int, got {type(response['score']).__name__}"
    
    if 'descendants' in response:
        assert isinstance(response['descendants'], int), f"Field 'descendants' must be int, got {type(response['descendants']).__name__}"
    
    # Optional field: kids (list of integers)
    if 'kids' in response:
        kids = response['kids']
        assert isinstance(kids, list), f"Field 'kids' must be list, got {type(kids).__name__}"
        if kids:
            # Sample 3 random items (or all items if list has fewer than 3)
            sample_size = min(3, len(kids))
            sampled_items = random.sample(kids, sample_size)
            for item in sampled_items:
                assert isinstance(item, int), (
                    f"Field 'kids' item is not an integer: "
                    f"got {type(item).__name__} ({item})"
                )
    
    # Optional field: text
    if 'text' in response:
        assert isinstance(response['text'], str), f"Field 'text' must be str, got {type(response['text']).__name__}"
    
    # Optional field: url
    if 'url' in response:
        assert isinstance(response['url'], str), f"Field 'url' must be str, got {type(response['url']).__name__}"
    
    # Optional field: dead (boolean)
    if 'dead' in response:
        assert isinstance(response['dead'], bool), f"Field 'dead' must be bool, got {type(response['dead']).__name__}"
    
    # Optional field: parent (integer)
    if 'parent' in response:
        assert isinstance(response['parent'], int), f"Field 'parent' must be int, got {type(response['parent']).__name__}"
    
    # Optional field: poll (integer)
    if 'poll' in response:
        assert isinstance(response['poll'], int), f"Field 'poll' must be int, got {type(response['poll']).__name__}"
    
    # Optional field: parts (list of integers)
    if 'parts' in response:
        parts = response['parts']
        assert isinstance(parts, list), f"Field 'parts' must be list, got {type(parts).__name__}"
        if parts:
            # Sample 3 random items (or all items if list has fewer than 3)
            sample_size = min(3, len(parts))
            sampled_items = random.sample(parts, sample_size)
            for item in sampled_items:
                assert isinstance(item, int), (
                    f"Field 'parts' item is not an integer: "
                    f"got {type(item).__name__} ({item})"
                )

def assert_item_comment_response(response: dict):
    """
    Validate that the comment response has correct structure and data types.
    
    Based on the official Hacker News API specification:
    https://github.com/HackerNews/API#items
    
    Required fields: id, type (must be 'comment'), time
    Common optional fields for comments: by, text, parent, kids
    """
    assert 'id' in response, "Missing required field 'id'"
    assert isinstance(response['id'], int), f"Field 'id' must be int, got {type(response['id']).__name__}"
    
    assert 'type' in response, "Missing required field 'type'"
    assert isinstance(response['type'], str), f"Field 'type' must be str, got {type(response['type']).__name__}"
    assert response['type'] == 'comment', f"Expected type 'comment', got '{response['type']}'"
    
    assert 'time' in response, "Missing required field 'time'"
    assert isinstance(response['time'], int), f"Field 'time' must be int, got {type(response['time']).__name__}"
    
    # Optional fields common for comments (validate type if present)
    if 'by' in response:
        assert isinstance(response['by'], str), f"Field 'by' must be str, got {type(response['by']).__name__}"
    
    if 'text' in response:
        assert isinstance(response['text'], str), f"Field 'text' must be str, got {type(response['text']).__name__}"
    
    if 'parent' in response:
        assert isinstance(response['parent'], int), f"Field 'parent' must be int, got {type(response['parent']).__name__}"
    
    # Optional field: kids (list of integers - child comments)
    if 'kids' in response:
        kids = response['kids']
        assert isinstance(kids, list), f"Field 'kids' must be list, got {type(kids).__name__}"
        if kids:
            # Sample 3 random items (or all items if list has fewer than 3)
            sample_size = min(3, len(kids))
            sampled_items = random.sample(kids, sample_size)
            for item in sampled_items:
                assert isinstance(item, int), (
                    f"Field 'kids' item is not an integer: "
                    f"got {type(item).__name__} ({item})"
                )
    
    # Optional field: dead (boolean)
    if 'dead' in response:
        assert isinstance(response['dead'], bool), f"Field 'dead' must be bool, got {type(response['dead']).__name__}"
    
    # Optional field: deleted (boolean)
    if 'deleted' in response:
        assert isinstance(response['deleted'], bool), f"Field 'deleted' must be bool, got {type(response['deleted']).__name__}"
