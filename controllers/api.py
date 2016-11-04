# These are the controllers for your ajax api.


# ----------------------HELPER-----------------------
import datetime

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def convertTime(t):
    return t.strftime('%b %d, %I:%M %p')

def isEdited(p):
    print(not (p.updated_on == p.created_on))
    print(p.updated_on)
    print(p.created_on)
    if (p.updated_on == p.created_on):
        return False
    else:
        return True


def post_response(post_obj):
    p = dict(
        id=post_obj.id,
        title=post_obj.post_title,
        content=post_obj.post_content,
        author=get_user_name_from_email(post_obj.user_email),
        date_created=convertTime(post_obj.created_on),
        # date_updated=timeCompare(post_obj),
        date_updated='Edit: '+convertTime(post_obj.updated_on) if isEdited(post_obj) else '',
        author_email=post_obj.user_email
    )
    return p


# ---------------------------------------------------

@auth.requires_signature()
def get_author_and_email():
    user_email = auth.user.email
    user_name = get_user_name_from_email(user_email)
    return response.json(dict(
        user_email=user_email,
        user_name=user_name
    ))


def get_posts():
    start_idx = int(request.vars.start_idx) if request.get_vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.get_vars.end_idx is not None else 0
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, orderby=~db.post.created_on,
                       limitby=(start_idx, end_idx + 1))  # + 1 for checking has_more
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            p = post_response(r)
            posts.append(p)
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
    p_id = db.post.insert(
        post_title=request.post_vars.title,
        post_content=request.post_vars.content
    )
    inserted_post = db.post(p_id)
    print(inserted_post.user_email)
    return response.json(dict(post=post_response(inserted_post)))

@auth.requires_signature()
def update_post():
    action_post = db.post(request.post_vars.id)
    action_post.post_title = request.post_vars.title
    action_post.post_content= request.post_vars.content
    action_post.updated_on = datetime.datetime.utcnow()
    action_post.update_record()

    print('Post:' + request.post_vars.id + ' has been updated' + str(action_post.updated_on))
    return response.json(dict(post=post_response(action_post)))


@auth.requires_signature()
def del_post():
    row = db(db.post.id == request.post_vars.id).select().first()
    row.delete_record()
    return response.json(dict())
