# Copyright 2024, Edward Morgan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""This module contains a class for implementing a MIMO Nonlinear Controllers
"""
from diffUV.kinematics import Kinematics as kin
from diffUV.base import Base as dyn_body
from diffUV.utils.symbols import *
import casadi as ca

class Controller():
    def __init__(self):
        # ned kinematic transformation
        Kinematics = kin()
        self.J_ = Kinematics.J
        # body representaion
        uv_body = dyn_body()
        self.gn = uv_body.body_restoring_vector()

    def __repr__(self) -> str:
        return f'{super().__repr__()} Simulator'
    
    def position_pid(self):

        ne = n - nd

        i_buffer = sum_e_buffer + ne*dt

        pid = -diag(Kp)@ne - diag(Kd)@(self.J_@x_nb) - diag(Ki)@i_buffer

        pid_controller = self.gn + self.J_.T@pid

        return pid_controller, i_buffer
    
    def velocity_pid(self):
        ve = x_nb - vb_d

        x_nb_prev = xS0_prev[6:]

        dve = (x_nb_prev - x_nb)/dt

        i_buffer = sum_e_buffer + ve*dt

        v_pid = -diag(Kp)@ve - diag(Kd)@dve - diag(Ki)@i_buffer

        pid_controller = self.gn + v_pid

        return pid_controller, i_buffer