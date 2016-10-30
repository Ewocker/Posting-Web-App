# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime


# ----------helper-----------
# -------------------------------------------------------------------------
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

def isAuther(p):
    try:
        if(p.user_email == auth.user.email):
            return A(XML('<i class="fa fa-pencil-square-o fa-2x edit_icon" aria-hidden="true"></i>')
                     , _href=URL('default', 'edit', args=['edit', p.id]))
        else:
            return ''
    except:
        return ''

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
# -------------------------------------------------------------------------




def index():
    """
    This is your main controller.
    """
    # I am creating a bogus list here, just to have some divs appear in the
    # view.  You need to read at most 20 posts from the database, in order of
    # most recent first, and you need to return that list here.
    # Note that posts is NOT a list of strings in your actual code; it is
    # what you get from a db(...).select(...).
    db.post.truncate()
    db.post.insert(post_title="DUMMY TITLE1", post_content="dummy content!")
    db.post.insert(post_title="DUMMY TITLE2", post_content="dummy content!")
    db.post.insert(post_title="DUMMY TITLE3", post_content="dummy content!")
    db.post.insert(post_title="DUMMY TITLE4", post_content="dummy content!")
    db.post.insert(post_title="DUMMY TITLE5", post_content="dummy content!")
    db.post.insert(post_title="DUMMY TITLE6", post_content="dummy content!")
    posts = db(db.post).select()

    return dict(posts=posts,
                user_name=get_user_name_from_email,
                convertTime=convertTime,
                isAuther= isAuther,
                updateTime=updateTime,
                timeCompare=timeCompare)


@auth.requires_login()
def edit():
    """
    This is the page to create / edit / delete a post.
    """
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
