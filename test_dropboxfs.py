# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import unittest
from fs.remote import CacheFS
from six import b
from pytest import fixture

from fs.errors import ResourceNotFoundError, DestinationExistsError
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


class TestDropboxFS(object):
    @fixture
    def fs(self, request):
        fs = DropboxFS("q3UFckbQggcAAAAAAAAAAdj9VvMFNx18Et2_BZLZxxLxCg6BLu3fLa15m8-qBvpB")
        request.addfinalizer(lambda: cleanup_dropbox(fs))
        return fs

    def test_copydir_overwrite_replaces_only_existing_files(self, fs):
        #Arrange
        content1 = b("If the implementation is hard to explain, it's a bad idea.")
        content2 = b("You aint gonna need it.")

        fs.makedir("a/b", recursive=True)
        fs.setcontents("a/b/1.txt", content1)
        fs.setcontents("a/2.txt", content1)
        fs.setcontents("a/3.txt", content1)

        fs.makedir("c")
        fs.setcontents("c/3.txt", content2)
        fs.setcontents("c/4.txt", content2)
        #Act
        fs.copydir("a", "c", overwrite=True)
        #Assert
        assert fs.exists("c/b/1.txt")
        assert fs.exists("c/2.txt")
        assert fs.getcontents("c/3.txt") == content1
        assert fs.getcontents("c/4.txt") == content2


class TestExternalDropboxFS(unittest.TestCase, FSTestCases):
    """This will test the DropboxFS implementation against the base tests defined in PyFilesystem"""
    def setUp(self):
        self.fs = DropboxFS("q3UFckbQggcAAAAAAAAAAdj9VvMFNx18Et2_BZLZxxLxCg6BLu3fLa15m8-qBvpB")

    def tearDown(self):
        cleanup_dropbox(self.fs)
        self.fs.close()


class TestExternalCachedDropboxFS(unittest.TestCase, FSTestCases):
    """This will test the CacheFS wrapped around the DropboxFS implementation
    against the base tests defined in PyFilesystem"""
    def setUp(self):
        wrapped_fs = DropboxFS("q3UFckbQggcAAAAAAAAAAdj9VvMFNx18Et2_BZLZxxLxCg6BLu3fLa15m8-qBvpB")
        self.fs = CacheFS(wrapped_fs)

    def tearDown(self):
        cleanup_dropbox(self.fs.wrapped_fs)
        self.fs.close()