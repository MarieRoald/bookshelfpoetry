# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Git is not installed in Azure App Services by default, so GitPython raises an
# import error. Here, we exploit the caching in the Python input system. If a
# module is already imported, then it is placed in the sys.modules dictionary
# which prevents subsequent imports. Here, we place a MagicMock instance in the
# sys.modules dict so any import of git will result in that MagicMock instance
# instead of importing and raising an import error.
import sys
from unittest.mock import MagicMock
sys.modules['git'] = MagicMock()

import streamlit.web.bootstrap  # noqa: E402
from streamlit.web.cli import main  # noqa: E402

class GitRepo:
    def __init__(self, *args, **kwargs):
        pass

    def is_valid(self):
        return True

streamlit.web.bootstrap.GitRepo = GitRepo

if __name__ == "__main__":
    # Set prog_name so that the Streamlit server sees the same command line
    # string whether streamlit is called directly or via `python -m streamlit`.
    main(prog_name="streamlit")
