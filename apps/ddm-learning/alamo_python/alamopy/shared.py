##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
# 
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes".
##############################################################################
"""
Set the alamo and gams paths here.
"""
import collections as col

debug = {}
data = {}

debug['almloc'] = 'alamo'
debug['gamsloc'] = 'gams'

# Initialize some dictionaries to store data later
# different keys are used to automate the printing of the .alm later
data['opts'] = col.OrderedDict.fromkeys(['ninputs', 'noutputs'])
data['labs'] = dict.fromkeys(
    ['savexlabels', 'savezlabels', 'xlinks', 'zlinks'])
data['lstopts'] = {}
data['set4'] = {}
data['stropts'] = {}

# potential arguments given to doalamo(**kwargs) are listed here
# The data dictionary is used to track arguments that will be passed to alamo
# The different keys 'opts','lstopts','stropts','set4' are used to record
# options of different types (float, list, strings, min/max)
data['pargs'] = {}
data['pargs']['opts'] = list(
    ['modeler', 'solvemip', 'linfcns', 'expfcns', 'logfcns', 'sinfcns',
     'cosfcns', 'sampler', 'maxiter', 'tolmaxerror', 'tolesterror', 'sigma',
     'builder', 'linearerror', 'regularizer', 'deltaterm', 'maxterms',
     'convpen', 'constant','cvxbic'])
data['pargs']['lstopts'] = list(
    ['multi2power', 'multi3power', 'ratiopower', 'monomialpower', 'zisint',
     'xmin', 'xmax'])
data['pargs']['stropts'] = list(
    ['simulator', 'almname', 'tracefname', 'almopt', 'gamssolver'])
data['pargs']['set4'] = list(['xmin', 'xmax','zmin','zmax'])

# The debug dictionary is used to track options utilized by the wrapper
# Some of these, such as file paths, could be changed before installing
debug['pargs'] = list(
    ['savescratch', 'savetrace', 'showalm', 'hardset', 'outkeys',
     'expandoutput', 'cvfun','almpath','gamspath',
     'hardset','simwrap', 'loo', 'lmo', 'mock'])
debug['cvfun'] = False
debug['savescratch'] = False
debug['savetrace'] = False
debug['showalm'] = False
debug['temp'] = 0
# expandoutput includes statistics other than the base model
debug['expandoutput'] = True # Returns additional information in alamopy call
debug['hardset'] = False # Force alamo to return a 1-term model
debug['simwrap'] = False # utilize alamopy.simwrapper 
debug['outkeys'] = False # return dictionary with output keys

# initialize options and flags not availible to user
debug['validation'] = False
debug['bignum'] = 10**10
debug['traindata'] = True

# assess uncertainty of surrogate model
debug['loo'] = False
debug['lmo'] = 0
debug['mock'] = False


# Initialize trace and .alm names
data['stropts']['tracefname'] = 'trace.trc'
data['stropts']['almname'] = 'temp.alm'
data['opts']['cvxbic'] = 1
#data['almopts']['solvemip'] = 0
#data['almopts']['sampler'] = 1
