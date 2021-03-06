# -*- coding: UTF-8 -*-
##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2019, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
This module contains utility functions useful for validating arguments to
IDAES modeling classes. These functions are primarily designed to be used as
the `domain` argument in ConfigBlocks.
"""

__author__ = "Andrew Lee"

from pyomo.environ import Set
from pyomo.dae import ContinuousSet
from pyomo.network import Port
from idaes.core import useDefault
from idaes.core.util.exceptions import ConfigurationError
import logging

_log = logging.getLogger(__name__)

def is_physical_parameter_block(val):
    '''Domain validator for property package attributes

    Args:
        val : value to be checked

    Returns:
        ConfigurationError if val is not an instance of PhysicalParameterBlock
        or useDefault
    '''
    from idaes.core.property_base import PhysicalParameterBlock
    if isinstance(val, PhysicalParameterBlock) or val == useDefault:
        return val
    else:
        _log.error("Property package argument {} should == useDefault or "
                   "be an instance of PhysicalParameterBlock".format(val))
        raise ConfigurationError(
                """Property package argument should be an instance
                of a PhysicalParameterBlock or useDefault""")


def is_reaction_parameter_block(val):
    '''Domain validator for reaction package attributes

    Args:
        val : value to be checked

    Returns:
        ConfigurationError if val is not an instance of ReactionParameterBlock
    '''
    from idaes.core.reaction_base import ReactionParameterBlock
    if isinstance(val, ReactionParameterBlock):
        return val
    else:
        raise ConfigurationError(
                """Reaction package argument should be an instance
                of a ReactionParameterBlock""")


def is_state_block(val):
    '''Domain validator for state block as an argument

    Args:
        val : value to be checked

    Returns:
        ConfigurationError if val is not an instance of StateBlock
        or None
    '''
    from idaes.core.property_base import StateBlock
    if (isinstance(val, StateBlock) or val is None):
        return val
    else:
        raise ConfigurationError(
                """State block should be an instance of a StateBlock or
                None""")


def list_of_floats(arg):
    '''Domain validator for lists of floats

    Args:
        arg : argument to be cast to list of floats and validated

    Returns:
        List of strings
    '''
    try:
        # Assume arg is iterable
        lst = [float(i) for i in arg]
    except TypeError:
        # arg is not iterable
        lst = [float(arg)]
    return lst


def list_of_strings(arg):
    '''Domain validator for lists of strings

    Args:
        arg : argument to be cast to list of strings and validated

    Returns:
        List of strings
    '''
    if isinstance(arg, dict):
        raise ConfigurationError("Invalid argument type (dict). "
                                 "Expected a list of strings, or something "
                                 "that can be cast to a list of strings")

    try:
        # Assume arg is iterable
        if isinstance(arg, str):
            lst = [arg]
        else:
            lst = [str(i) for i in arg]
    except TypeError:
        # arg is not iterable
        lst = [str(arg)]
    return lst


def is_port(arg):
    '''Domain validator for ports

    Args:
        arg : argument to be checked as a Port

    Returns:
        Port object or Exception
    '''
    if not isinstance(arg, Port):
        raise ConfigurationError('Invalid argument type. Expected an instance '
                                 'of a Pyomo Port object')
    return arg


def is_time_domain(arg):
    '''Domain validator for time domains

    Args:
        arg : argument to be checked as a time domain (i.e. Set or
        ContinuousSet)

    Returns:
        Set, ContinuousSet or Exception
    '''
    if not isinstance(arg, (Set, ContinuousSet)):
        raise ConfigurationError('Invalid argument type. Expected an instance '
                                 'of a Pyomo Set or ContinuousSet object')
    return arg

  
def is_transformation_method(arg):
    '''Domain validator for transformation methods

    Args:
        arg : argument to be checked for membership in recognized strings

    Returns:
        Recognised string or Exception
    '''
    if arg in ["dae.finite_difference",
               "dae.collocation"]:
        return arg
    else:
        raise ConfigurationError(
                'Invalid value provided for transformation_method. '
                'Please check the value and spelling of the argument provided.'
                )


def is_transformation_scheme(arg):
    '''Domain validator for transformation scheme

    Args:
        arg : argument to be checked for membership in recognized strings

    Returns:
        Recognised string or Exception
    '''
    if arg in ["BACKWARD", "FORWARD", "LAGRANGE-RADAU", "LAGRANGE-LEGENDRE"]:
        return arg
    else:
        raise ConfigurationError(
                'Invalid value provided for transformation_scheme. '
                'Please check the value and spelling of the argument provided.'
                )
