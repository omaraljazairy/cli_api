CLI_API
------------------------------------

This Command Line API is a tool to interact with my APIs. Instead of using curl or httpie to make requests to the API, I setup this command line interface to
communicate with the API without worrying about which parameters I need to use or authentications.

At the moment I'm setting this tool to communicate with the Spnglish API. I use the Click framework.
There are shared services which will be used by different modules like the logger, requester, tokens.

At the moment i'm setting up the tokens service to handle the retrieval or update of the token used in the header of the requests. this is needed for the authentication.
