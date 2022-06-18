from abc import ABC, abstractmethod


class GhostlyClient(ABC):
	"""Abstract base class for HTTP clients to web services"""

	DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
	MISSING_CONTINUATION = ""

	def __init__(self):
		self.search_results = []
		self.continuation = GhostlyClient.MISSING_CONTINUATION

	def clear(self):
		self.search_results.clear()
		self.continuation = GhostlyClient.MISSING_CONTINUATION

	@abstractmethod
	def search(self, search_term: str, sort_by_upload_date: bool) -> bool:
		"""Searches for the given `search_term` and appends the results as a list of type `SearchResult` to `self.search_results`

		:param search_term: The term to search for
		:param sort_by_upload_date: Obtained search results are sorted by date in descending order if `True`, otherwise they are sorted by relevance
		:return: `True` if the search was successfull, `False` otherwise
		"""
		pass

	@abstractmethod
	def continue_search(self) -> bool:
		pass

	def can_continue_search(self) -> bool:
		return self.continuation != GhostlyClient.MISSING_CONTINUATION


class SearchResult:
	def __init__(self, id: str, title: str, author: str, thumbnails: list[str], accessibility: str,
		     published: str, length: str, views: str):
		self.id = id
		self.title = title
		self.author = author
		self.thumbnails = thumbnails
		self.accessibility = accessibility
		self.published = published
		self.length = length
		self.views = views