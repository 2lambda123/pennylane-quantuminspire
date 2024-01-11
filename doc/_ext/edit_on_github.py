"""
Sphinx extension to add ReadTheDocs-style "Edit on GitHub" links to the
sidebar.
Loosely based on https://github.com/astropy/astropy/pull/347
"""

import os
import warnings


__licence__ = 'BSD (3 clause)'


def get_github_url(app, view, path):
    return 'https://github.com/{project}/{view}/{branch}/{path}'.format(
        project=app.config.edit_on_github_project,
        view=view,
        branch=app.config.edit_on_github_branch,
        path=path)


def html_page_context(app, pagename, templatename, context, doctree):
    if templatename != 'page.html':
        return

    if not (app.config.edit_on_github_project and app.config.edit_on_github_branch):
        warnings.warn("edit_on_github_project not specified")
        return

    if not (doctree and len(doctree.children) > 0):
        return
    
    path = os.path.relpath(doctree.get('source'), app.builder.srcdir)
    show_url = get_github_url(app, 'tree', path)
    edit_url = get_github_url(app, 'edit', path)

    context['show_url'] = show_url
    context['edit_url'] = edit_url


def setup(app):
    app.add_config_value('edit_on_github_project', '', True)
    app.add_config_value('edit_on_github_branch', 'master', True)
    app.connect('html-page-context', html_page_context)