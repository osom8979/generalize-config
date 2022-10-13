# generalize-config

[![PyPI](https://img.shields.io/pypi/v/generalize-config?style=flat-square)](https://pypi.org/project/generalize-config/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/generalize-config?style=flat-square)
[![GitHub](https://img.shields.io/github/license/osom8979/generalize-config?style=flat-square)](https://github.com/osom8979/generalize-config)

Read and generalize the configuration

## Overview

A list of variables required for a program's execution environment can be obtained in several ways:

- Environment Variables
- Configuration files
- Command-line arguments
- etc ...

Especially if you're deploying as a container,
you need to reference a file like `/run/secrets/...`
([docker swarm secret](https://docs.docker.com/engine/swarm/secrets/))
to read the variable.

I developed the **generalize-config** library because I needed a way to unify environment variables from multiple places into one.

## Features

- All results are returned as [argparse.Namespace](https://docs.python.org/3/library/argparse.html#argparse.Namespace).
- [json](https://github.com/ijl/orjson), [yaml](https://pyyaml.org/), [cfg](https://docs.python.org/3/library/configparser.htmlI) files are supported.
- [argparse.Namespace](https://docs.python.org/3/library/argparse.html#argparse.Namespace) merge.
- Environment variable filtering and file reader.

## Installation

```bash
pip install generalize-config
```

## Usage

### Configuration file

Reading extension-based configuration files

```yaml
envs:
  host: localhost
  port: 8080
```

```python
from argparse import Namespace
from generalize_config import read_config_file

config = read_config_file("/path/config/file.yml", "envs", encoding="utf-8")
assert isinstance(config, Namespace)
assert "localhost" == config.host
assert 8080 == config.port
```

The supported extension types are:

- YAML extensions: `.yml`, `.yaml`
- JSON extensions: `.json`
- CFG extensions: `.cfg`, `.ini`

> :warning: When using a CFG file, there must be 1 subsection argument.

### Environment variable

Environment Variable Filtering

```python
from argparse import Namespace
from generalize_config import read_os_envs

# APP_HTTP_HOST_VALUE=localhost
config = read_os_envs(prefix="APP_", suffix="_VALUE")
assert isinstance(config, Namespace)
assert "localhost" == config.http_host
```

Filter environment variables and read files:

```python
from argparse import Namespace
from generalize_config import read_os_envs_file

# APP_DATABASE_PASSWORD_FILE=/run/secrets/password
config = read_os_envs_file(prefix="APP_", suffix="_FILE")
assert isinstance(config, Namespace)
assert isinstance(config.database_password, str)
```

### Merge namespaces

```python
from argparse import Namespace, ArgumentParser
from generalize_config import merge_left_first

parser = ArgumentParser()
# add_argument ...
args = parser.parse_known_args()[0]

result = Namespace()
merge_left_first(result, args, ...)
print(result)
```

### Generalized method

The recommended reading order is:

1. Fixed variable (higher priority)
2. Command line arguments
3. Configuration file received as a command line argument
4. Environment Variables
5. Configuration file received as environment variable
6. Environment variable pointing to file
7. Default variable (low priority)

The function that implements the above is `read_generalize_configs`:

```python
from argparse import ArgumentParser, Namespace
from generalize_config import read_generalize_configs

parser = ArgumentParser()
# add_argument ...

default_args = Namespace(...)

result = read_generalize_configs(
    parser=parser,
    subsection="application",
    env_prefix="ENV_",
    env_suffix="_FILE",
    config_key="config",
    default=default_args,
)
print(result)
```

## Things to know

When using
[argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html#argumentparser-objects)
you need to make sure that all values not entered are returned as `None`.
Otherwise, the `merge_left_first` function may malfunction.

Also, variables acquired through CFG files and environment variables are
fixed as `string` type. To solve this you need to deserialize like this:

Install [type-serialize](https://github.com/osom8979/type-serialize):

```bash
pip install type-serialize
```

Add type annotation to `Namespace` and then call `deserialize`:

```python
from argparse import Namespace
from generalize_config import read_generalize_configs
from type_serialize import deserialize

class Config(Namespace):
    host: str
    port: int
    # ...

ns = read_generalize_configs(...)
config = deserialize(ns, Config)
assert isinstance(config, Config)

print(config)
```

## License

See the [LICENSE](./LICENSE) file for details. In summary,
**generalize-config** is licensed under the **MIT license**.
