from utils import get_auth_headers, make_request


class CHEFSForm:
    BASE_URL = "https://submit.digital.gov.bc.ca/app/api/v1/"

    def __init__(self, form_id, api_key):
        """
        Initializes a new instance of the CHEFSForm class.

        Args:
            form_id (str): The ID of the form.
            api_key (str): The API key for authentication.
        """
        self.form_id = form_id
        self.api_key = api_key

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): Query parameters for the request. Defaults to None.

        Returns:
            dict: JSON response from the API.
        """
        headers = get_auth_headers(self.form_id, self.api_key)
        return make_request(
            "GET", f"{self.BASE_URL}{endpoint}", headers=headers, params=params
        )

    def _get_latest_form_version(self):
        """
        Retrieves the latest version ID of the form.

        Returns:
            int: The latest version ID.
        """
        response = self.get_details()
        return response["versions"][0]["id"]

    def _get_version_fields(self, version=None):
        """
        Retrieves the fields of a specific form version.

        Args:
            version (int, optional): The version ID of the form. Defaults to None (latest version).

        Returns:
            list: List of form fields.
        """
        return self.get(
            f"forms/{self.form_id}/versions/{version if version is not None else self._get_latest_form_version()}/fields"
        )

    def get_details(self):
        """
        Retrieves details of the form.

        Returns:
            dict: Details of the form.
        """
        return self.get(f"forms/{self.form_id}")

    def list_submissions(self, version=None, fields=[]):
        """
        Lists submissions of the form.

        Args:
            version (int, optional): The version ID of the form. Defaults to None (latest version).

        Returns:
            dict: Submissions of the form.
        """
        if version is None:
            url = f"forms/{self.form_id}/submissions"
        else:
            latest_version_id = (
                version if version is not None else self._get_latest_form_version()
            )
            url = f"forms/{self.form_id}/versions/{latest_version_id}/submissions"

        if not fields:
            fields = (
                self._get_version_fields(version)
                if version
                else self._get_version_fields()
            )
        params = {"fields": ",".join(fields)}
        return self.get(url, params=params)

    def get_submission_data(self, version=None, fields=[]):
        """
        Retrieves submission data for a form.

        Args:
            version (int, optional): The version ID of the form. Defaults to None (latest version).
            fields (list, optional): List of fields to include in the submission data. Defaults to empty list (all fields).

        Returns:
            dict: Submission data for the form.
        """
        if not fields:
            fields = self._get_version_fields()
        latest_version_id = (
            version if version is not None else self._get_latest_form_version()
        )
        url = f"forms/{self.form_id}/versions/{latest_version_id}/submissions/discover"
        params = {"fields": ",".join(fields)}
        return self.get(url, params=params)

    def get_submission(self, submission_id):
        """
        Retrieves a specific submission.

        Args:
            submission_id (str): ID of the submission.

        Returns:
            dict: Details of the submission.
        """
        return self.get(f"submissions/{submission_id}")

    def get_file(self, file_id):
        """
        Retrieves details of a file.

        Args:
            file_id (str): ID of the file.

        Returns:
            dict: Details of the file.
        """
        return self.get(f"files/{file_id}")
