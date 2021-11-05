import attr


@attr.s
class NACERow(object):
    order = attr.ib()
    level = attr.ib()
    code = attr.ib()
    parent = attr.ib()
    description = attr.ib()
    includes = attr.ib()
    also_includes = attr.ib()
    rulings = attr.ib()
    excludes = attr.ib()
    reference_to_ISIC_rev_4 = attr.ib()

    def astuple(self):
        return attr.astuple(self)

    def __str__(self):
        return '{}: {}'.format(self.code, self.description)
