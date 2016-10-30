# These are the controllers for your ajax api.

def get_posts():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    start_idx = int(request.vars.start_idx) if request.get_vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.get_vars.end_idx is not None else 0
    posts = []
    has_more = False
    # + 1 for checking has_more
    rows = db().select(db.post.ALL, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            t = dict(
                id=r.id,
                title=r.post_title,
                content=r.post_content,
                auther=r.user_email,
                date_created=r.created_on,
                date_updated=r.updated_on
            )
            posts.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None

    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
    ))



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

