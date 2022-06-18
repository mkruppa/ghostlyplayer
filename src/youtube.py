from ghostlyclient import GhostlyClient, SearchResult
import requests

from typing import NewType
json_t = NewType("json_t", dict)

class YouTube(GhostlyClient):
	"""HTTP client for YouTube videos"""

	BASE_SEARCH_URL = "https://www.youtube.com/youtubei/v1/search"
	SEARCH_PARAMS = { "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8" }
	HEADERS = { "User-Agent": GhostlyClient.DEFAULT_USER_AGENT }
	DATA = {
		"context": {
			"client": {
				"userAgent": GhostlyClient.DEFAULT_USER_AGENT + ",gzip(gfe)",
				"clientName": "WEB",
				"clientVersion": "2.20220114.01.00"
			},
			"request": {
				"useSsl": "true"
			}
		}
	}

	@staticmethod
	def search_request_data(search_term: str, sort_by_upload_date: bool) -> json_t:
		return json_t(YouTube.DATA \
			| { "query": search_term } \
			| ({ "params": "CAISAhAB" } if sort_by_upload_date else {}))

	def continue_search_request_data(self) -> json_t:
		return json_t(YouTube.DATA \
			| { "continuation": self.continuation })

	def search(self, search_term: str, sort_by_upload_date: bool) -> bool:
		response = YouTube._post_request(YouTube.search_request_data(search_term, sort_by_upload_date))
		return self._append_results_on_success(response)

	def continue_search(self) -> bool:
		response = YouTube._post_request(self.continue_search_request_data())
		return self._append_results_on_success(response)

	def print_page_results(self, page: int) -> None:
		for v in self.search_results[page]:
			print(v.accessibility)

	@staticmethod
	def _post_request(data: json_t) -> requests.Response:
		return requests.post(YouTube.BASE_SEARCH_URL, params=YouTube.SEARCH_PARAMS, headers=YouTube.HEADERS, json=data)

	def _append_results_on_success(self, response: requests.Response) -> bool:
		success = response.status_code == requests.codes.ok
		if success:
			json_contents = self._json_contents(response)
			self.continuation = YouTube._continuation(json_contents)
			self.search_results.append(YouTube._extract_videos(json_contents))
			self.print_page_results(-1)
		return success

	def _json_contents(self, response: requests.Response) -> json_t:
		if not self.search_results:
			return YouTube._json_contents_first_page(response)
		else:
			return YouTube._json_contents_not_first_page(response)

	@staticmethod
	def _json_contents_first_page(response: requests.Response) -> json_t:
		return response.json()["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

	@staticmethod
	def _json_contents_not_first_page(response: requests.Response) -> json_t:
		return response.json()["onResponseReceivedCommands"][0]["appendContinuationItemsAction"]["continuationItems"]

	@staticmethod
	def _continuation(json_contents: json_t) -> str:
		if "continuationItemRenderer" in json_contents[-1]:
			return json_contents[-1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
		else:
			return GhostlyClient.MISSING_CONTINUATION

	@staticmethod
	def _extract_video(e: json_t) -> SearchResult:
		v = e["videoRenderer"]
		return SearchResult(id=v["videoId"],
				 title=v["title"]["runs"][0]["text"],
			        author=v["longBylineText"]["runs"][0]["text"],
			    thumbnails=v["thumbnail"]["thumbnails"],
			 accessibility=v["title"]["accessibility"]["accessibilityData"]["label"],
			     published=v["publishedTimeText"]["simpleText"] if "publishedTimeText" in v else None,
			        length=v["lengthText"]["simpleText"] if "lengthText" in v else None,
			         views=v["viewCountText"]["simpleText"] if "viewCountText" in v and "simpleText" in v["viewCountText"] else None)

	@staticmethod
	def _extract_videos(json_contents: json_t) -> list[SearchResult]:
		results = []
		for e in json_contents[0]["itemSectionRenderer"]["contents"]:
			if "videoRenderer" in e.keys():
				results.append(YouTube._extract_video(e))
		return results