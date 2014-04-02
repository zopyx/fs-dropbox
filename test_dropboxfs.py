# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import unittest

from fs.tests import FSTestCases

from dropboxfs import DropboxFS, DropboxClient


def cleanup_dropbox(fs):
    """Remove all files and folders from dropbox"""
    for entry in fs.listdir(files_only=True):
        fs.remove(entry)
    for entry in fs.listdir(dirs_only=True):
        fs.removedir(entry)


def patched_init(self, token_secret):
    """Init method of the DropboxFS has to be patched for testing purposes,
    as I only want to provide the token_secret and no app specific information"""
    super(DropboxFS, self).__init__(thread_synchronize=True)
    self.client = DropboxClient(token_secret)
    self.localtime = False

DropboxFS.__init__ = patched_init


class TestExternalDropboxFS(unittest.TestCase, FSTestCases):
    """This will test the DropboxFS implementation against the base tests defined in PyFilesystem"""
    def setUp(self):
        self.fs = DropboxFS("q3UFckbQggcAAAAAAAAAAdj9VvMFNx18Et2_BZLZxxLxCg6BLu3fLa15m8-qBvpB")

    def tearDown(self):
        cleanup_dropbox(self.fs)
        self.fs.close()