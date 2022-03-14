from api import *


def get_global(
        name                        # type: str
):                                  # type: (...) -> str | None
    pass


def set_global(
        name,                       # type: str
        value                       # type: str
):                                  # type: (...) -> None
    pass


def unset_global(
        name                        # type: str
):                                  # type: (...) -> None
    pass


def helm_remote(
        chart,                      # type: str
        repo_url='',                # type: str
        repo_name='',               # type: str
        release_name='',            # type: str
        values=[],                  # type: str | list[str]
        set=[],                     # type: str | list[str]
        namespace='',               # type: str
        version='',                 # type: str
        username='',                # type: str
        password='',                # type: str
        allow_duplicates=False,     # type: bool
        create_namespace=False      # type: bool
):                                  # type: (...) -> Blob
    pass


def namespace_yaml(
        name,                       # type: str
        annotations=[],             # type: list[str]
        labels=[]                   # type: list[str]
):                                  # type: (...) -> Blob
    pass


def namespace_create(
        name,                       # type: str
        allow_duplicates=False,     # type: bool
        annotations=[],             # type: list[str]
        labels=[]                   # type: list[str]
):                                  # type: (...) -> None
    pass


def namespace_inject(
        x,                          # type: str | Blob
        ns                          # type: str
):                                  # type: (...) -> Blob
    pass


def secret_yaml_generic(
        name,                       # type: str
        namespace='',               # type: str
        from_file=None,             # type: str | None
        secret_type=None,           # type: str | None
        from_env_file=None          # type: str | None
):                                  # type: (...) -> Blob
    pass


def secret_create_generic(
        name,                       # type: str
        namespace='',               # type: str
        from_file=None,             # type: str | None
        secret_type=None,           # type: str | None
        from_env_file=None          # type: str | None
):                                  # type: (...) -> None
    pass


def secret_from_dict(
        name,                       # type: str
        namespace='',               # type: str
        inputs={}                   # type: dict[str, str]
):                                  # type: (...) -> Blob
    pass


def secret_yaml_tls(
        name,                       # type: str
        cert,                       # type: str
        key,                        # type: str
        namespace=''                # type: str
):                                  # type: (...) -> Blob
    pass


def secret_create_tls(
        name,                       # type: str
        cert,                       # type: str
        key,                        # type: str
        namespace=''                # type: str
):                                  # type: (...) -> None
    pass


def configmap_yaml(
        name,                       # type: str
        namespace='',               # type: str
        from_file=None,             # type: str | None
        watch=True,                 # type: bool
        from_env_file=None          # type: str | None
):                                  # type: (...) -> Blob
    pass


def configmap_create(
        name,                       # type: str
        namespace='',               # type: str
        from_file=None,             # type: str | None
        watch=True,                 # type: bool
        from_env_file=None          # type: str | None
):                                  # type: (...) -> None
    pass


def configmap_from_dict(
        name,                       # type: str
        namespace='',               # type: str
        inputs={}                   # type: dict[str, str]
):                                  # type: (...) -> Blob
    pass
