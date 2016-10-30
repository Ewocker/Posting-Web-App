# These are the controllers for your ajax api.


#----------------------HELPER-----------------------

def convertTime(t):
    return t.strftime('%b %d, %I:%M %p')

def updateTime(p):
    if (p.updated_on == p.created_on):
        return ''
    else:
        return convertTime(p.updated_on)

def isEdited(p):
    if (p.updated_on == p.created_on):
        return False
    else:
        return True

def timeCompare(p):
    if not isEdited(p): return ''
    t = p.updated_on
    delta = datetime.datetime.utcnow() - t
    time = 'Edited '
    year = delta.days // 365
    month = delta.days // 30
    week = delta.days // 7
    minute = delta.seconds // 60
    hour = minute // 60
    if year > 0:
        time += str(year)
        time +- 'year ' if year == 1 else 'years '
    elif month > 0:
        time += str(month)
        time += 'month ' if month == 1 else 'months '
    elif week > 0:
        time += str(week)
        time += 'week ' if week == 1 else 'weeks '
    elif delta.days is not 0:
        time += str(delta.days)
        time += 'day ' if delta.days==1 else 'days '
    elif hour > 0:
        time += str(hour)
        time += 'hour ' if hour==1 else 'hours '
    elif minute > 0:
        time += str(minute)
        time += 'minute ' if minute==1 else 'minutes '
    elif delta.seconds is not 0:
        time += str(delta.seconds)
        time += 'second ' if delta.seconds==1 else 'seconds '
    return time + ' ago'

def post_response(post_obj):
    p = dict(
        id=post_obj.id,
        title=post_obj.post_title,
        content=post_obj.post_content,
        auther=post_obj.user_email,
        date_created=convertTime(post_obj.created_on),
        date_updated=timeCompare(post_obj)
    )
    return p

#---------------------------------------------------

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
    rows = db().select(db.post.ALL, orderby=~db.post.created_on , limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            p = dict(
                id=r.id,
                title=r.post_title,
                content=r.post_content,
                auther=r.user_email,
                date_created=convertTime(r.created_on),
                date_updated=timeCompare(r)
            )
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
    """Here you get a new post and add it.  Return what you want."""
    # Implement me!
    p_id = db.post.insert(
        post_title = request.post_vars.title,
        post_content = request.post_vars.content
    )
    inserted_post = db.post(p_id)
    return response.json(dict(post=post_response(inserted_post)))


@auth.requires_signature()
def del_post():
    """Used to delete a post."""
    # Implement me!
    return response.json(dict())

