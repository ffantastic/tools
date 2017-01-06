#! /usr/bin/python

import click
import redis
import sys
import json
import aop as aop
from settings import *


@click.group()
@click.pass_context
def cli(ctx):
    red_cli = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    ctx.obj['redis'] = red_cli


@click.command(name='display', help='Display all <Url pattern -> E-mail address> rules and exit')
@click.pass_context
def display(ctx):
    url_list = json.loads(ctx.obj['redis'].get(URLMAP_KEY))
    TITLE = ['INDEX', 'REGULAR EXPRESSION', 'E-MAIL']
    # set auto indent
    indent_len = list(map(lambda x: len(x), TITLE))
    for item in url_list:
        for i, key in enumerate(DICT_KEYS):
            indent_len[i + 1] = max(len(item.get(key)), indent_len[i + 1])

    indentTemplate = '{:^%d}{:^%d}{:^%d}' % tuple([indent + 10 for indent in indent_len])
    # print indentTemplate

    click.echo(click.style(indentTemplate.format(*TITLE),
                           fg='blue', bold=True))
    for i, item in enumerate(url_list):
        click.echo(indentTemplate.format(str(i), item[DICT_KEYS[0]], item[DICT_KEYS[1]]))


@click.command(name='add', help='Add a new rule in the tail')
@click.argument('regex', nargs=1)
@click.argument('email', nargs=1)
@click.pass_context
@aop.check(check_callback=aop.add_check)
@aop.flush
def add(ctx, regex, email):
    url_list = ctx.obj['url_list']
    url_list.append({
        'regex': regex,
        'email': email
    })


@click.command(name='del', help='Delete a rule by a given index')
@click.argument('index', nargs=1, type=int)
@click.pass_context
@aop.check(check_callback=aop.delete_check)
@aop.flush
def delete(ctx, index):
    url_list = ctx.obj['url_list']
    url_list.pop(index)


@click.command(name='update', help='Update a url pattern or E-mail of rule by a given index')
@click.argument('index', nargs=1, type=int)
@click.option('--url', '-u', help='update url pattern')
@click.option('--email', '-e', help='update E-mail address')
@click.pass_context
@aop.check(check_callback=aop.update_check)
@aop.flush
def update(ctx, index, url, email):
    url_list = ctx.obj['url_list']

    if url:
        url_list[index][DICT_KEYS[0]] = url
    if email:
        url_list[index][DICT_KEYS[1]] = email


map(lambda command: cli.add_command(getattr(sys.modules[__name__], command)),
    ['display', 'add', 'delete', 'update'])


def main():
    cli(obj={})
