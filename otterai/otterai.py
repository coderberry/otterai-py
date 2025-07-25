import time
import xml.etree.ElementTree as ET

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from .models import AbstractSummaryResponse  # Phase 4 models
from .models import AvailableSpeechesResponse  # Phase 5 models
from .models import (
    ActionItemsResponse,
    ContactsResponse,
    FoldersResponse,
    GroupsResponse,
    MentionCandidatesResponse,
    SpeakersResponse,
    SpeechResponse,
    SpeechTemplatesResponse,
)


class OtterAIException(Exception):
    pass


class OtterAI:
    API_BASE_URL = "https://otter.ai/forward/api/v1/"
    S3_BASE_URL = "https://s3.us-west-2.amazonaws.com/"

    def __init__(self):
        self._session = requests.Session()
        self._userid = None
        self._cookies = None

    def _is_userid_invalid(self):
        return not self._userid

    def _handle_response(self, response, data=None):
        if data:
            return {"status": response.status_code, "data": data}
        try:
            return {"status": response.status_code, "data": response.json()}
        except ValueError:
            return {"status": response.status_code, "data": {}}

    def is_retryable_exception(exception):
        """Defines which exceptions should trigger a retry"""
        if isinstance(exception, requests.exceptions.RequestException):
            return True
        if hasattr(exception, "response") and exception.response is not None:
            return exception.response.status_code in [429, 500, 502, 503, 504]
        return False

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(multiplier=2, min=2, max=60),  # Increased wait time
        stop=stop_after_attempt(7),  # More retry attempts
    )
    def _make_request(self, method, url, **kwargs):
        """Handles API requests with retries"""
        try:
            response = self._session.request(method, url, **kwargs)

            if response.status_code == 429:  # Handle rate limits dynamically
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after) + 1  # Convert to int and add buffer
                    print(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Rate limited. Applying exponential backoff...")
                response.raise_for_status()

            elif response.status_code in [500, 502, 503, 504]:
                print(f"Retrying {url} due to status {response.status_code}")
                response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}, URL: {url}")
            raise

    def login(self, username, password):
        # Avoid logging in again if already authenticated
        if self._userid:
            print("Already logged in, skipping login request.")
            return {"status": requests.codes.ok, "data": {"userid": self._userid}}

        auth_url = OtterAI.API_BASE_URL + "login"
        payload = {"username": username}
        self._session.auth = (username, password)

        try:
            response = self._make_request("GET", auth_url, params=payload)

            if response.status_code == requests.codes.ok:
                self._userid = response.json().get("userid")
                self._cookies = response.cookies.get_dict()
                print("Login successful!")
            else:
                print(
                    f"Login failed with status {response.status_code}: {response.text}"
                )

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            print(f"Login failed due to request exception: {e}")
            return {"status": 500, "data": {"error": str(e)}}

    def get_user(self):
        user_url = OtterAI.API_BASE_URL + "user"
        response = self._make_request("GET", user_url)
        return self._handle_response(response)

    def get_speakers(self):
        speakers_url = OtterAI.API_BASE_URL + "speakers"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", speakers_url, params=payload)

        return self._handle_response(response)

    def get_speeches(self, folder=0, page_size=45, source="owned"):
        speeches_url = OtterAI.API_BASE_URL + "speeches"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {
            "userid": self._userid,
            "folder": folder,
            "page_size": page_size,
            "source": source,
        }
        response = self._make_request("GET", speeches_url, params=payload)

        return self._handle_response(response)

    def get_speech(self, otid):
        speech_url = OtterAI.API_BASE_URL + "speech"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid, "otid": otid}
        response = self._make_request("GET", speech_url, params=payload)

        return self._handle_response(response)

    def query_speech(self, query, otid, size=500):
        query_speech_url = OtterAI.API_BASE_URL + "advanced_search"
        payload = {"query": query, "size": size, "otid": otid}
        response = self._make_request("GET", query_speech_url, params=payload)

        return self._handle_response(response)

    def upload_speech(self, file_name, content_type="audio/mp4"):
        speech_upload_params_url = OtterAI.API_BASE_URL + "speech_upload_params"
        speech_upload_prod_url = OtterAI.S3_BASE_URL + "speech-upload-prod"
        finish_speech_upload = OtterAI.API_BASE_URL + "finish_speech_upload"

        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")

        # First grab upload params (aws data)
        payload = {"userid": self._userid}
        response = self._make_request("GET", speech_upload_params_url, params=payload)

        if response.status_code != requests.codes.ok:
            return self._handle_response(response)

        response_json = response.json()
        params_data = response_json["data"]

        # Send options (precondition) request
        prep_req = requests.Request("OPTIONS", speech_upload_prod_url).prepare()
        prep_req.headers["Accept"] = "*/*"
        prep_req.headers["Connection"] = "keep-alive"
        prep_req.headers["Origin"] = "https://otter.ai"
        prep_req.headers["Referer"] = "https://otter.ai/"
        prep_req.headers["Access-Control-Request-Method"] = "POST"
        self._session.send(prep_req)

        # TODO: test for large files (this should stream)
        fields = {}
        params_data["success_action_status"] = str(params_data["success_action_status"])
        del params_data["form_action"]
        fields.update(params_data)
        fields["file"] = (file_name, open(file_name, mode="rb"), content_type)
        multipart_data = MultipartEncoder(fields=fields)
        response = self._make_request(
            "POST",
            speech_upload_prod_url,
            data=multipart_data,
            headers={"Content-Type": multipart_data.content_type},
        )

        if response.status_code != 201:
            return self._handle_response(response)

        # Parse XML response
        xmltree = ET.ElementTree(ET.fromstring(response.text))
        xmlroot = xmltree.getroot()
        location = xmlroot[0].text
        bucket = xmlroot[1].text
        key = xmlroot[2].text

        # Call finish API
        payload = {
            "bucket": bucket,
            "key": key,
            "language": "en",
            "country": "us",
            "userid": self._userid,
        }
        response = self._make_request("GET", finish_speech_upload, params=payload)

        return self._handle_response(response)

    def download_speech(self, otid, name=None, fileformat="txt,pdf,mp3,docx,srt"):
        download_speech_url = OtterAI.API_BASE_URL + "bulk_export"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"formats": fileformat, "speech_otid_list": [otid]}
        headers = {
            "x-csrftoken": self._cookies["csrftoken"],
            "referer": "https://otter.ai/",
        }
        response = self._make_request(
            "POST", download_speech_url, params=payload, headers=headers, data=data
        )
        filename = (
            (name if not name == None else otid)
            + "."
            + ("zip" if "," in fileformat else fileformat)
        )
        if response.ok:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            raise OtterAIException(
                f"Got response status {response.status_code} when attempting to download {otid}"
            )
        return self._handle_response(response, data={"filename": filename})

    def move_to_trash_bin(self, otid):
        move_to_trash_bin_url = OtterAI.API_BASE_URL + "move_to_trash_bin"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"otid": otid}
        headers = {"x-csrftoken": self._cookies["csrftoken"]}
        response = self._make_request(
            "POST", move_to_trash_bin_url, params=payload, headers=headers, data=data
        )

        return self._handle_response(response)

    def create_speaker(self, speaker_name):
        create_speaker_url = OtterAI.API_BASE_URL + "create_speaker"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"speaker_name": speaker_name}
        headers = {"x-csrftoken": self._cookies["csrftoken"]}
        response = self._make_request(
            "POST", create_speaker_url, params=payload, headers=headers, data=data
        )

        return self._handle_response(response)

    def get_notification_settings(self):
        notification_settings_url = OtterAI.API_BASE_URL + "get_notification_settings"
        response = self._make_request("GET", notification_settings_url)

        return self._handle_response(response)

    def list_groups(self):
        list_groups_url = OtterAI.API_BASE_URL + "list_groups"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"simple_group": "true"}
        response = self._make_request("GET", list_groups_url, params=payload)

        return self._handle_response(response)

    def get_folders(self):
        folders_url = OtterAI.API_BASE_URL + "folders"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", folders_url, params=payload)

        return self._handle_response(response)

    def speech_start(self):
        speech_start_uel = OtterAI.API_BASE_URL + "speech_start"
        ### TODO
        # In the browser a websocket session is opened
        # wss://ws.aisense.com/api/v2/client/speech?token=ey...
        # The speech_start endpoint returns the JWT token

    def stop_speech(self):
        speech_finish_url = OtterAI.API_BASE_URL + "speech_finish"

    def set_speech_title(self, otid, title):
        set_speech_title_url = OtterAI.API_BASE_URL + "set_speech_title"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid, "otid": otid, "title": title}
        response = self._make_request("GET", set_speech_title_url, params=payload)

        return self._handle_response(response)

    # Structured data methods (Phase 2)
    def get_contacts_structured(self):
        """
        Get all contacts with structured response.

        Returns:
            ContactsResponse: Structured response containing list of Contact objects

        Raises:
            OtterAIException: If userid is invalid
        """
        contacts_url = OtterAI.API_BASE_URL + "contacts"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", contacts_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(f"Failed to get contacts: {response.status_code}")

        return ContactsResponse(**response.json())

    def get_folders_structured(self):
        """
        Get all folders with structured response.

        Returns:
            FoldersResponse: Structured response containing list of Folder objects

        Raises:
            OtterAIException: If userid is invalid
        """
        folders_url = OtterAI.API_BASE_URL + "folders"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", folders_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(f"Failed to get folders: {response.status_code}")

        return FoldersResponse(**response.json())

    def get_speech_mention_candidates_structured(self, otid):
        """
        Get mention candidates for a speech with structured response.

        Args:
            otid (str): The speech ID

        Returns:
            MentionCandidatesResponse: Structured response containing list of MentionCandidate objects

        Raises:
            OtterAIException: If the request fails
        """
        mention_candidates_url = OtterAI.API_BASE_URL + "speech_mention_candidates"
        payload = {"otid": otid}
        response = self._make_request("GET", mention_candidates_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(
                f"Failed to get mention candidates: {response.status_code}"
            )

        return MentionCandidatesResponse(**response.json())

    def list_groups_structured(self):
        """
        Get all groups with structured response (matches TEMP.md endpoint).

        Returns:
            GroupsResponse: Structured response containing list of Group objects

        Raises:
            OtterAIException: If userid is invalid
        """
        list_groups_url = OtterAI.API_BASE_URL + "list_groups"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"simple_group": "true"}
        response = self._make_request("GET", list_groups_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(f"Failed to get groups: {response.status_code}")

        return GroupsResponse(**response.json())

    def get_speakers_structured(self):
        """
        Get all speakers with structured response (matches TEMP.md endpoint).

        Returns:
            SpeakersResponse: Structured response containing list of Speaker objects

        Raises:
            OtterAIException: If userid is invalid
        """
        speakers_url = OtterAI.API_BASE_URL + "speakers"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", speakers_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(f"Failed to get speakers: {response.status_code}")

        return SpeakersResponse(**response.json())

    # Phase 4: Speech Templates and Action Items - Structured Methods

    def get_speech_templates_structured(self):
        """
        Get all speech templates with structured response.

        Returns:
            SpeechTemplatesResponse: Structured response containing list of SpeechTemplate objects

        Raises:
            OtterAIException: If request fails
        """
        templates_url = OtterAI.API_BASE_URL + "speech_templates"
        response = self._make_request("GET", templates_url)

        if response.status_code != 200:
            raise OtterAIException(
                f"Failed to get speech templates: {response.status_code}"
            )

        return SpeechTemplatesResponse(**response.json())

    def get_speech_action_items_structured(self, otid: str):
        """
        Get speech action items with structured response.

        Args:
            otid (str): Speech OTID

        Returns:
            ActionItemsResponse: Structured response containing list of ActionItem objects

        Raises:
            OtterAIException: If request fails
        """
        action_items_url = OtterAI.API_BASE_URL + "speech_action_items"
        payload = {"otid": otid}
        response = self._make_request("GET", action_items_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(
                f"Failed to get speech action items: {response.status_code}"
            )

        return ActionItemsResponse(**response.json())

    def get_abstract_summary_structured(self, otid: str):
        """
        Get abstract summary with structured response.

        Args:
            otid (str): Speech OTID

        Returns:
            AbstractSummaryResponse: Structured response containing AbstractSummaryData object

        Raises:
            OtterAIException: If request fails
        """
        summary_url = OtterAI.API_BASE_URL + "abstract_summary"
        payload = {"otid": otid}
        response = self._make_request("GET", summary_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(
                f"Failed to get abstract summary: {response.status_code}"
            )

        return AbstractSummaryResponse(**response.json())

    # Phase 5: Speech Model - Most Complex - Structured Methods

    def get_speech_structured(self, otid: str):
        """
        Get speech with structured response.

        Args:
            otid (str): Speech OTID

        Returns:
            SpeechResponse: Structured response containing Speech object

        Raises:
            OtterAIException: If userid is invalid or request fails
        """
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")

        speech_url = OtterAI.API_BASE_URL + "speech"
        payload = {"userid": self._userid, "otid": otid}
        response = self._make_request("GET", speech_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(f"Failed to get speech: {response.status_code}")

        return SpeechResponse(**response.json())

    def get_available_speeches_structured(
        self,
        funnel: str = "home_feed",
        page_size: int = 6,
        use_serializer: str = "HomeFeedSpeechWithoutSharedGroupsSerializer",
        source: str = "home",
        speech_metadata: bool = True,
    ):
        """
        Get available speeches with structured response.

        Args:
            funnel (str): Funnel type
            page_size (int): Page size
            use_serializer (str): Serializer to use
            source (str): Source type
            speech_metadata (bool): Include speech metadata

        Returns:
            AvailableSpeechesResponse: Structured response containing list of Speech objects

        Raises:
            OtterAIException: If request fails
        """
        speeches_url = OtterAI.API_BASE_URL + "available_speeches"
        payload = {
            "funnel": funnel,
            "page_size": page_size,
            "use_serializer": use_serializer,
            "source": source,
            "speech_metadata": str(speech_metadata).lower(),
        }
        response = self._make_request("GET", speeches_url, params=payload)

        if response.status_code != 200:
            raise OtterAIException(
                f"Failed to get available speeches: {response.status_code}"
            )

        return AvailableSpeechesResponse(**response.json())
