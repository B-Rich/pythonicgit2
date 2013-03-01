#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim :set ft=py:

""" Highly experimental pythonic wrapper for libgit2 layer on pygit2. """

import pygit2 as pg2

__author__ = "Valentin Haenel <valentin.haenel@gmx.de>"
__copyright__ = "2013"
__licence__ = """© %s %s

Pythonicgit2 is licenced under the terms of the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sub-licence, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""" % (__copyright__, __author__)

REF_PREFIX = "refs/"
HEADS_PREFIX = REF_PREFIX + "heads/"
TAGS_PREFIX = REF_PREFIX + "tags/"


def shorten_ref(ref, prefix_len):
    return ref[prefix_len:]


def shorten_head(head):
    return shorten_ref(head, len(HEADS_PREFIX))


def shorten_tag_ref(tag_ref):
    return shorten_ref(tag_ref, len(TAGS_PREFIX))


class Repository(object):

    def __init__(self, path):
        self._raw_repo = pg2.Repository(path)

    @staticmethod
    def create(path, bare=False):
        raw = pg2.init_repository(path, bare)
        return Repository(raw.path)

    def ref_iter(self, prefix):
        return (b for b in self._raw_repo.listall_references()
                if b.startswith(prefix))

    def ref_dict(self, ref_iter, shorten=None):
        return dict(((r if shorten is None else shorten(r),
                     self._raw_repo.lookup_reference(r).hex)
                     for r in ref_iter))

    @property
    def heads_iter(self):
        return self.ref_iter(HEADS_PREFIX)

    @property
    def branches_iter(self):
        return (shorten_head(b) for b in self.heads_iter)

    @property
    def branches(self):
        return [b for b in self.branches_iter]

    @property
    def branches_dict(self):
        return self.ref_dict(self.heads_iter, shorten=shorten_head)

    @property
    def tag_ref_iter(self):
        return self.ref_iter(TAGS_PREFIX)

    @property
    def tags_iter(self):
        return (shorten_tag_ref(t) for t in self.tag_ref_iter)

    @property
    def tags(self):
        return [t for t in self.tags_iter]

    @property
    def tags_dict(self):
        return self.ref_dict(self.tag_ref_iter, shorten=shorten_tag_ref)
