import pygit2 as pg2

class Repository(object):

    def __init__(self, path):
        self._raw_repo = pg2.Repository(path)

    @staticmethod
    def create(path, bare=False):
        raw = pg2.init_repository(path, bare)
        return Repository(raw.path)

    def ref_iter(self, prefix):
        return (b[len(prefix):] for b in self._raw_repo.listall_references()
            if b.startswith(prefix))

    def ref_dict(self, ref_iter):
        return dict(((r, self._raw_repo.lookup_reference(r).hex)
                     for r in ref_iter))

    def branches_iter(self):
        return self.ref_iter('refs/heads/')

    def branches(self):
        return [b for b in self.branches_iter]

    def branches_dict(self):
        return self.ref_dict(self.branches_iter())

    def tags_iter(self):
        return self.ref_iter('refs/tags/')

    def tags(self):
        return [t for t in self.tags_iter]

    def tags_dict(self):
        return self.ref_dict(self.tags_iter())
