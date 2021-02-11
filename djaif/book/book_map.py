from graphviz import Digraph

from djaif.book import models


def book_map(book):
    dig = Digraph('Map')

    for page in book.bookpage_set.all():
        dig.node(
            _pid(page),
            label='{page.id}:"{page.title}"\n{items}'.format(
                page=page,
                items='\n'.join(
                    '+ {id}:"{name}"'.format(
                        id=i.id, name=i.name[:10],
                    ) for i in page.items.all(),
                ),
            ),
            tooltip=page.body,
            href='/admin/book/bookpage/{0.id}/change'.format(page),
        )

    links = models.PageLink.objects.filter(from_page__book_id=book.id)
    for link in links.all():
        dig.edge(
            _pid(link.from_page),
            _pid(link.to_page),
            label='{link.id}:"{shortname}"\n{items}'.format(
                link=link,
                shortname=link.name[:10],
                items='\n'.join(
                    '? {id}:"{name}"'.format(
                        id=i.id, name=i.name[:10],
                    ) for i in link.items.all(),
                ),
            ),
            labeltooltip=link.name,
            labelhref='/admin/book/pagelink/{0.id}/change'.format(link),
        )

    dig.format = 'svg'  # noqa: WPS125
    return dig.pipe().decode('utf-8')


def _pid(page):
    return 'page_{id}'.format(id=page.id)
