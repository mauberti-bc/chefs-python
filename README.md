## Tools for accessing data from the BC Government's Common Hosted Forms Service (CHEFS). 

### CHEFSForm

The ```CHEFSForm``` class makes it easy to access (CHEFS)[https://digital.gov.bc.ca/bcgov-common-components/common-hosted-form-service/] form data in Python. After generating an API key for a specific form in the CHEFS web application, pass both the form's ID and its API key to ```CHEFSForm()``` to create a new CHEFSForm instance. This instance provides methods for retrieving information about that specific form, including its submissions.

```
myForm = CHEFSForm(form_id="", api_key="")
```

In the example above, ```myForm``` represents a single CHEFS form. If you need to access data from multiple forms, call CHEFSForm() multiple times, changing the ```form_id``` and ```api_key``` values each time. In the example below, both the form_id and api_key must match the form that you are connecting to.

```
myFirstForm = CHEFSForm(form_id="form1", api_key="")
mySecondForm = CHEFSForm(form_id="form2", api_key="")
myThirdForm = CHEFSForm(form_id="form3", api_key="")
```

#### Getting data from submissions

After creating a CHEFSForm instance, you can use the ```get_submission_data()``` method to get the form's submissions.

```
myForm = CHEFSForm(form_id="", api_key="")
myForm.list_submissions(version=None, fields=[])
```

If you do not specify a form version, as shown above, submissions from the latest version will be returned. If you do not specify a list of form fields nor a version, all form fields from the latest version will be returned. If you do not specify a list of form fields but do specify a version, all form fields from that version will be returned.

#### Get details about a form

You can use the ```get_details()``` method to get information about your form, such as its name, when it was created, versions, and more.

```
myForm.get_details()
```

#### Limitations

This module supports CHEFS API endpoints that use basic authentication (API keys), which is a subset of the whole API. Endpoints that rely exclusively on bearer authentication (IDIR and BCeID) are not supported. If there is interest, we can add bearer authentication to this module--let us know by creating a GitHub issue.

There is a limit to how many times you can call the CHEFS API per minute. This means that you should save the outputs of each method to a variable in your environment and avoid redundant calls.


