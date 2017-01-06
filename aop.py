import click
import json
from settings import *


def check(check_callback):
    def decorator(func):
        def wrap(*args, **kwargs):
            ctx = args[0]
            if ctx != None:
                red_cli = ctx.obj['redis']
                url_list = json.loads(red_cli.get(URLMAP_KEY))
                # cache url_list
                ctx.obj['url_list'] = url_list

            status, msg = check_callback(*args, **kwargs)
            if status:
                func(*args, **kwargs)
            else:
                click.secho(msg, fg='red')

        return wrap

    return decorator


def flush(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        ctx = args[0]
        if ctx != None:
            red_cli = ctx.obj['redis']
            url_list = ctx.obj['url_list'];
            try:
                red_cli.set(URLMAP_KEY, json.dumps(url_list))
            except Exception:
                click.secho(Exception.message, fg='red')
            else:
                click.secho('OK', fg='green')

    return wrap


def add_check(ctx, regex, email):
    if regex and email:
        return True, ''
    return False, 'Invalid url or E-mail'


def delete_check(ctx, index):
    if 0 <= int(index) < len(ctx.obj['url_list']):
        return True, ''
    return False, 'Invalid index'


def update_check(ctx, index, url, email):
    s, m = delete_check(ctx, index);
    if not s:
        return s, m
    if not url and not email:
        return False, 'You have to assign at least one option of --url or --email'
    return True, ''
