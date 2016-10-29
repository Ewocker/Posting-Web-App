# These are the controllers for your ajax api.

def get_posts():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    return response.json(dict())


# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_post():
    """Here you get a new post and add it.  Return what you want."""
    # Implement me!
    return response.json(dict())


@auth.requires_signature()
def del_post():
    """Used to delete a post."""
    # Implement me!
    return response.json(dict())

