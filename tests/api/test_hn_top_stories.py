import pytest
from core.api.helpers.hacker_news_helpers import (
    assert_top_stories_response,
    assert_item_top_story_response,
    assert_item_comment_response,
    get_first_story_comments,
    get_first_deleted_comment,
    top_stories

)

from core.logconfig import get_logger



logger = get_logger(__name__)

@pytest.mark.hacker_news
class TestTopStories:
    def test_top_stories(self, hn_client):
        assert_top_stories_response(top_stories(hn_client))

    def test_current_top_story(self, hn_client):
        first_top_story = top_stories(hn_client, top_story=True)
        first_top_story = hn_client.get_item(item_id=first_top_story).json()
        assert first_top_story['type'] == 'story', 'not type story'
        assert_item_top_story_response(first_top_story)

    def test_current_top_story_first_comment(self, hn_client):
        all_top_stories = top_stories(hn_client)
        story_with_comments = get_first_story_comments(client=hn_client, item_ids=all_top_stories)
        first_comment = hn_client.get_item(item_id=story_with_comments['kids'][0]).json()
        assert first_comment['type'] == 'comment', 'not type comment'
        assert_item_comment_response(first_comment)

# Had to timebox edge cases, would spend more time otherwise.
    def test_deleted_top_level_comment(self, hn_client):
        """
        Test handling of deleted top-level comments.
        Validates that deleted comments have correct structure even when optional fields are missing.
        """
        all_top_stories = top_stories(hn_client)
        assert len(all_top_stories) > 0, "top stories response is empty"
        story_with_comments = get_first_story_comments(client=hn_client, item_ids=all_top_stories)
        deleted_comment = get_first_deleted_comment(client=hn_client, comment_ids=story_with_comments['kids'])

        if deleted_comment is None:
            pytest.skip("No deleted comment found in top stories - this is expected as deleted comments are rare")

        # Validate deleted comment structure (handles missing optional fields like 'text' or 'by')
        assert_item_comment_response(deleted_comment)
        assert deleted_comment.get('deleted') is True, "Comment should have deleted=True"

    def test_top_story_with_no_comments(self, hn_client):
        all_top_stories = top_stories(hn_client)
        no_comments_story = get_first_story_comments(client=hn_client, item_ids=all_top_stories, comments=False)
        for filed in no_comments_story:
            assert filed != "kids", "story has comments"

    def test_invalid_item_id(self, hn_client):
        invalid_story_id_response = hn_client.get_item(item_id=999999999, validate=False)
        assert invalid_story_id_response.status_code() == 200, "status code is not 200" # ideally should return 4xx
        assert invalid_story_id_response.content() == 'null', "content is not null"
