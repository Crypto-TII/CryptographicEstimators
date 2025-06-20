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

from ..MQEstimator.MQAlgorithms import BooleanSolveFXL
from ..MQEstimator import MQProblem
from math import log2, inf, floor


def _optimize_k(n: int, m: int, k: int, q: int, w: float):
    """Find the optimal parameter `K` from Furue, Nakamura, and Takagi strategy.

    Args:
        n (int): Number of variables
        m (int): Number of polynomials
        k (int): Whipping parameter
        q (int): Order of the finite field
        w (float): Description not provided in original docstring
    """
    (K, time) = (0, inf)

    for i in range(0, n-1):
        m_tilde = m - floor((n-i)/(m-i)) + 1
        n_tilde = m_tilde - i

        if n_tilde < 1: break

        E = BooleanSolveFXL(MQProblem(n=n_tilde, m=m_tilde, q=q), bit_complexities=False, w=w)
        t = i * log2(q) + E.time_complexity()

        if t < time:
            time = t
            K = i

    return K
