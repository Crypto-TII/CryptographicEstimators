# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************


"""Single source of truth for the library version.

The version is declared once, in ``pyproject.toml``. At runtime it is read from
the installed distribution metadata, and falls back to ``pyproject.toml``
itself when the library is used from a source checkout that was never
installed.
"""

import tomllib
from importlib.metadata import PackageNotFoundError, version as _distribution_version
from pathlib import Path

DISTRIBUTION_NAME = "cryptographic_estimators"

UNKNOWN_VERSION = "unknown"


def _version_from_pyproject() -> str | None:
    """Return the version declared in ``pyproject.toml``, or None if unreadable."""
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    try:
        with pyproject.open("rb") as f:
            return tomllib.load(f)["project"]["version"]
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        return None


def get_version() -> str:
    """Return the version of the cryptographic_estimators library.

    Examples:
        >>> from cryptographic_estimators._version import get_version
        >>> get_version()  # doctest: +ELLIPSIS
        '...'
    """
    try:
        return _distribution_version(DISTRIBUTION_NAME)
    except PackageNotFoundError:
        return _version_from_pyproject() or UNKNOWN_VERSION


__version__ = get_version()
