from __future__ import annotations
import pickle
import os
from FileSystemNodeModel import FileSystemNode, File, Directory
from datetime import datetime
import re


class FileSystemCache:
    """A simple cache for storing file and directory nodes."""

    def __init__(self):
        self.body = {}
        self.keyword_index = {}

    def update(self, path: str, node: FileSystemNode):
        """Update the cache with the given file or directory node."""
        self.body[path] = node
        node.cache_timestamp = datetime.now()

        # update reverse index
        keywords = self.extract_keywords(node)
        for keyword in keywords:
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = set()
            self.keyword_index[keyword].add(path)

    def search(self, query: str, match_any: bool = False):
        """
        Function to perform keyword search on the given query, search type can be specified using match_any
        match_any = False -> AND search, must match all keywords
        match_any = True -> OR search, must match any keyword

        @params:
        query: str: keywords to be searched, given as a search string
        match_any: bool: boolean to specify which search type to perform.
        """
        query_keywords = set(re.split(r'\W+', query.lower()))
        query_keywords.discard('')
        if match_any:
            return self._search_match_any(query_keywords)
        else:
            return self._search_match_all(query_keywords)

    def _search_match_all(self, query_keywords: set):
        matching_files = set()
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                if not matching_files:
                    matching_files = self.keyword_index[keyword].copy()
                else:
                    matching_files &= self.keyword_index[keyword]
            else:
                return set()

        return matching_files

    def _search_match_any(self, query_keywords: set):
        matching_files = set()
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                matching_files |= self.keyword_index[keyword] # union of matching files

        return matching_files


    def is_modified(self, path: str):
        """Check if the file or directory has been modified since it was last cached."""
        cached_node = self.body.get(path, None)
        if cached_node:
            return cached_node.modification_date() != datetime.fromtimestamp(os.path.getmtime(path))
        return True

    def remove(self, path: str):
        """Remove a file or directory from the cache."""
        if path in self.body:
            del self.body[path]

    def save_to_file(self):
        if not os.path.exists('cache/system_model_cache.pkl'):
            # code to create file here
            os.makedirs('cache', exist_ok=True)
        with open('cache/system_model_cache.pkl', 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def load_from_file(self):
        with open('cache/system_model_cache.pkl', 'rb') as pickle_file:
            self.body = pickle.load(pickle_file)

    @staticmethod
    def extract_keywords(node: FileSystemNode):
        node_keywords = set()

        # get keywords from file name
        name_parts = re.split(r'\W+', node.name.lower())
        node_keywords.update(name_parts)

        _, extension = os.path.splitext(node.name)  # extension will be blank for directories

        if extension:
            node_keywords.add(extension.lower())

        node_keywords.discard('')

        return node_keywords
    def __str__(self):
        return str(self.body)

    def __getitem__(self, key):
        if key in self.body:
            if self.is_modified(key):
                raise Exception(f"Item {key} outdated in cache.")
            return self.body[key]
        else:
            raise Exception(f"Item {key} not in cache.")
