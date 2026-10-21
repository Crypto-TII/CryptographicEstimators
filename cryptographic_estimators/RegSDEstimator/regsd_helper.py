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

def r_int(x):
    return int(round(x))


def min_max(a: int, b: int, s: bool) -> int:
    """Returns the minimum or maximum of two integers based on a boolean switch.

    Args:
        a (int): The first integer.
        b (int): The second integer.
        s (bool): If True, returns the maximum of a and b. If False, returns the minimum of a and b.

    Returns:
        int: The minimum or maximum of a and b, depending on the value of s.
    """
    if s:
        return max(a, b)
    else:
        return min(a, b)
