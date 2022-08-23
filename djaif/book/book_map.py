from djaif.book import models


def book_map(book):
    dig = ['digraph {',
           ' node [style="filled"]'
          ]

    for page in book.bookpage_set.all():
        dig.append('{pid} [ \
                label="{label}" \
                tooltip="{tooltip}" \
                href="{href}" \
            ]'.format(
                pid = _pid(page),
                label='{page.title} ({page.id})\\n{items}'.format(
                    page=page,
                    items='\\n'.join(
                        '+ {id}: {name}'.format(
                            id=i.id, name=i.name[:10],
                        ) for i in page.items.all()
                    ),
                ),
                tooltip=page.body.replace("\r\n", " "),
                href='/admin/book/bookpage/{0.id}/change'.format(page),
            )
        )

    links = models.PageLink.objects.filter(from_page__book_id=book.id)
    for link in links.all():
        dig.append('{from_page} -> {to_page} [ \
                shape="circle" \
                label="{label}" \
                labeltooltip="{labeltooltip}" \
                labelhref="{labelhref}" \
            ]'.format(
                from_page = _pid(link.from_page),
                to_page = _pid(link.to_page),
                label='{link.id}: {shortname}\\n{items}'.format(
                    link=link,
                    shortname=link.name[:10],
                    items='\\n'.join(
                        '? {id}: {name}'.format(
                            id=i.id, name=i.name[:10],
                        ) for i in link.items.all()
                    ),
                ),
                labeltooltip=link.name,
                labelhref='/admin/book/pagelink/{0.id}/change'.format(link),
            )
        )

    dig.append('}')
    return ' '.join(dig)


def _pid(page):
    return 'page_{id}'.format(id=page.id)
