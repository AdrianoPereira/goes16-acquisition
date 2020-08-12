class AbstractException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.message = kwargs.get('message', None)
        self.name = kwargs.get('name', None)
        self.status = kwargs.get('status', '[undefined]')

    def __str__(self):
        return "%s %s: %s" % (self.status, self.name, self.message)


class LoginUnsuccessfulError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(LoginUnsuccessfulError, self).__init__(*args, **kwargs)
        self.message = "Login not successful, check your username or connection"
        self.name = "LoginUnsuccessfulError"
        self.status = '[error]'


class LoginRequiredError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(LoginRequiredError, self).__init__(*args, **kwargs)
        self.message = "Download not sucessful, login is required"
        self.name = "LoginRequiredError"
        self.status = '[error]'


class DateRequiredError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(DateRequiredError, self).__init__(*args, **kwargs)
        self.message = "The date maybe complete"
        self.name = "DateRequiredError"
        self.status = '[error]'


class TimeRequiredError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(TimeRequiredError, self).__init__(*args, **kwargs)
        self.message = "The hour and minute maybe complete"
        self.name = "TimeRequiredError"
        self.status = '[error]'


class DirectoryRequiredError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(DirectoryRequiredError, self).__init__(*args, **kwargs)
        self.message = "The directory is required"
        self.name = "DirectoryRequiredError"
        self.status = '[error]'


class RemoteUrlRequiredError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(RemoteUrlRequiredError, self).__init__(*args, **kwargs)
        self.message = "Remote URL is not defined"
        self.name = "RemoteUrlRequiredError"
        self.status = '[error]'


class ListFilesNotFoundError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(ListFilesNotFoundError, self).__init__(*args, **kwargs)
        self.message = "List of url files not found"
        self.name = "ListFilesNotFoundError"
        self.status = '[error]'


class UrlFileNotFoundError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(UrlFileNotFoundError, self).__init__(*args, **kwargs)
        self.message = "The URL of file not found"
        self.name = "UrlFileNotFoundError"
        self.status = '[error]'


class FileAlreadyExistError(AbstractException):
    def __init__(self, *args, **kwargs):
        super(FileAlreadyExistError, self).__init__(*args, **kwargs)
        self.message = "File was already downloaded"
        self.name = "FileAlreadyExistError"
        self.status = '[warning]'
