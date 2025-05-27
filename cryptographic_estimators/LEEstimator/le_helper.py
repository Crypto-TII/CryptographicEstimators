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

from math import log2, inf, \
    comb as binomial


def cost_to_find_random_2dim_subcodes_with_support_w(n: int, k: int, w: int):
    """Returns the cost of finding a 2 dimensional subcode with specific parameters.

    Args:
        n (int): Length of the code
        k (int): Dimension of the code
        w (int): Support of the code

    Returns:
        The cost of finding a 2 dimensional subcode
    """
    if n-k<w-2:
        return inf
    return log2((k * k + binomial(k, 2))) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2))
