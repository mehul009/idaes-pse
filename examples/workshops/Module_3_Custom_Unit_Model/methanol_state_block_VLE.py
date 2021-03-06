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
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Property package for ideal VLE calucations for the methanol synthesis problem.
Correlations from Turkay and Grossmann paper. See Latex files for details.
"""

# Chages the divide behavior to not do integer division
from __future__ import division

# Import Python libraries
import logging

# Import Pyomo libraries
from pyomo.environ import Constraint, log, NonNegativeReals, value, Var
from pyomo.opt import SolverFactory, TerminationCondition

# Import IDAES cores
from idaes.core import (declare_process_block_class,
                        StateBlockData,
                        StateBlock,
                        MaterialFlowBasis)
from idaes.core.util.initialization import solve_indexed_blocks
from idaes.core.util.exceptions import ConfigurationError

# Some more inforation about this module
__author__ = "Jaffer Ghouse"
__version__ = "0.0.1"


# Set up logger
_log = logging.getLogger(__name__)


class _IdealStateBlock(StateBlock):
    """
    This Class contains methods which should be applied to Property Blocks as a
    whole, rather than individual elements of indexed Property Blocks.
    """

    def initialize(blk, flow_mol=None, mole_frac=None,
                   temperature=None, pressure=None,
                   hold_state=False, outlvl=0,
                   solver='ipopt', optarg={'tol': 1e-8}):
        """
        Initialisation routine for property package.

        Keyword Arguments:
            flow_mol_comp : value at which to initialize component flows
                             (default=None)
            pressure : value at which to initialize pressure (default=None)
            temperature : value at which to initialize temperature
                          (default=None)
            outlvl : sets output level of initialisation routine

                     * 0 = no output (default)
                     * 1 = return solver state for each step in routine
                     * 2 = include solver output infomation (tee=True)

            optarg : solver options dictionary object (default=None)
            solver : str indicating whcih solver to use during
                     initialization (default = 'ipopt')
            hold_state : flag indicating whether the initialization routine
                         should unfix any state variables fixed during
                         initialization (default=False).
                         - True - states varaibles are not unfixed, and
                                 a dict of returned containing flags for
                                 which states were fixed during
                                 initialization.
                        - False - state variables are unfixed after
                                 initialization by calling the
                                 relase_state method

        Returns:
            If hold_states is True, returns a dict containing flags for
            which states were fixed during initialization.
        """
        # Fix state variables if not already fixed
        Fflag = {}
        Xflag = {}
        Pflag = {}
        Tflag = {}

        for k in blk.keys():
            if blk[k].flow_mol.fixed is True:
                Fflag[k] = True
            else:
                Fflag[k] = False
                if flow_mol is None:
                    blk[k].flow_mol.fix(1.0)
                else:
                    blk[k].flow_mol.fix(flow_mol)

            for j in blk[k]._params.component_list:
                if blk[k].mole_frac[j].fixed is True:
                    Xflag[k, j] = True
                else:
                    Xflag[k, j] = False
                    if mole_frac is None:
                        blk[k].mole_frac[j].fix(1 / len(blk[k].
                                                _params.component_list))
                    else:
                        blk[k].mole_frac[j].fix(mole_frac[j])

            if blk[k].pressure.fixed is True:
                Pflag[k] = True
            else:
                Pflag[k] = False
                if pressure is None:
                    blk[k].pressure.fix(0.101325)
                else:
                    blk[k].pressure.fix(pressure)

            if blk[k].temperature.fixed is True:
                Tflag[k] = True
            else:
                Tflag[k] = False
                if temperature is None:
                    blk[k].temperature.fix(3.25)
                else:
                    blk[k].temperature.fix(temperature)

        # Set solver options
        if outlvl > 1:
            stee = True
        else:
            stee = False

        if optarg is None:
            sopt = {'tol': 1e-8}
        else:
            sopt = optarg

        opt = SolverFactory('ipopt')
        opt.options = sopt

        # ---------------------------------------------------------------------
        for k in blk.keys():

            blk[k].eq_total.deactivate()
            blk[k].eq_comp.deactivate()
            if (blk[k].config.defined_state is False):
                blk[k].eq_mol_frac_out.deactivate()
            if (blk[k].config.has_phase_equilibrium) or \
                    (blk[k].config.parameters.config.valid_phase ==
                        ('Liq', 'Vap')) or \
                    (blk[k].config.parameters.config.valid_phase ==
                        ('Vap', 'Liq')):
                blk[k].eq_Keq.deactivate()
                blk[k].eq_sum_mol_frac.deactivate()

        if (blk[k].config.has_phase_equilibrium) or \
                (blk[k].config.parameters.config.valid_phase ==
                    ('Liq', 'Vap')) or \
                (blk[k].config.parameters.config.valid_phase ==
                    ('Vap', 'Liq')):
            results = solve_indexed_blocks(opt, [blk], tee=stee)

            if outlvl > 0:
                if results.solver.termination_condition \
                        == TerminationCondition.optimal:
                    _log.info("Initialisation step 1 for "
                              "{} completed".format(blk.name))
                else:
                    _log.warning("Initialisation step 1 for "
                                 "{} failed".format(blk.name))

        else:
            if outlvl > 0:
                _log.info("Initialisation step 1 for "
                          "{} skipped".format(blk.name))

        for k in blk.keys():
            blk[k].eq_total.activate()
            blk[k].eq_comp.activate()
            if (blk[k].config.has_phase_equilibrium) or \
                    (blk[k].config.parameters.config.valid_phase ==
                        ('Liq', 'Vap')) or \
                    (blk[k].config.parameters.config.valid_phase ==
                        ('Vap', 'Liq')):
                blk[k].eq_Keq.activate()
                blk[k].eq_sum_mol_frac.activate()

        results = solve_indexed_blocks(opt, [blk], tee=stee)

        if outlvl > 0:
            if results.solver.termination_condition \
                    == TerminationCondition.optimal:
                _log.info("Initialisation step 2 for "
                          "{} completed".format(blk.name))
            else:
                _log.warning("Initialisation step 2 for "
                             "{} failed".format(blk.name))

        for k in blk.keys():
            if (blk[k].config.defined_state is False):
                blk[k].eq_mol_frac_out.activate()
        # ---------------------------------------------------------------------
        # If input block, return flags, else release state
        flags = {"Fflag": Fflag,
                 "Xflag": Xflag,
                 "Pflag": Pflag,
                 "Tflag": Tflag}

        if hold_state is True:
            return flags
        else:
            blk.release_state(flags)

        if outlvl > 0:
            if outlvl > 0:
                _log.info('{} Initialisation Complete.'.format(blk.name))

    def release_state(blk, flags, outlvl=0):
        '''
        Method to relase state variables fixed during initialisation.

        Keyword Arguments:
            flags : dict containing information of which state variables
                    were fixed during initialization, and should now be
                    unfixed. This dict is returned by initialize if
                    hold_state=True.
            outlvl : sets output level of of logging
        '''
        # Unfix state variables
        for k in blk.keys():
            if flags['Fflag'][k] is False:
                blk[k].flow_mol.unfix()
            for j in blk[k]._params.component_list:
                if flags['Xflag'][k, j] is False:
                    blk[k].mole_frac[j].unfix()
            if flags['Pflag'][k] is False:
                blk[k].pressure.unfix()
            if flags['Tflag'][k] is False:
                blk[k].temperature.unfix()

        if outlvl > 0:
            if outlvl > 0:
                _log.info('{} State Released.'.format(blk.name))


@declare_process_block_class("IdealStateBlock",
                             block_class=_IdealStateBlock)
class StateBlockData(StateBlockData):
    """An example property package for ideal VLE."""

    def build(self):
        """Callable method for Block construction."""
        super(StateBlockData, self).build()

        # Check for valid phase indicator and consistent flags
        if self.config.has_phase_equilibrium and \
                self.config.parameters.config.valid_phase in ['Vap', 'Liq']:
            raise ConfigurationError("Inconsistent inputs. Valid phase"
                                     " flag not set to VL for the state"
                                     " block but has_phase_equilibrium"
                                     " is set to True.")
        self._make_state_vars()
        self._make_vars()
        if not self.config.has_phase_equilibrium and \
                self.config.parameters.config.valid_phase == "Liq":
            self._make_liq_phase_eq()

        if (self.config.has_phase_equilibrium) or \
                (self.config.parameters.config.valid_phase ==
                    ('Liq', 'Vap')) or \
                (self.config.parameters.config.valid_phase ==
                    ('Vap', 'Liq')):
            self._make_flash_eq()

        if not self.config.has_phase_equilibrium and \
                self.config.parameters.config.valid_phase == "Vap":
            self._make_vap_phase_eq()

    def get_material_flow_basis(self):
        return MaterialFlowBasis.molar

    def _make_state_vars(self):
        """List the necessary state variable objects."""
        self.flow_mol = Var(initialize=1.0,
                            domain=NonNegativeReals,
                            doc='Component molar flowrate [kgmol/s]')
        self.mole_frac = Var(self._params.component_list,
                             bounds=(0, 1),
                             initialize=1.0 / len(self._params.component_list))
        self.pressure = Var(initialize=0.101325,
                            domain=NonNegativeReals,
                            doc='State pressure [MPa]')
        self.temperature = Var(initialize=3,
                               domain=NonNegativeReals,
                               doc='State temperature [100K]')

    def _make_vars(self):
        self.flow_mol_phase = Var(self._params.phase_list,
                                  initialize=0.5,
                                  bounds=(0, None))

        self.mole_frac_phase = Var(self._params.phase_list,
                                   self._params.component_list,
                                   initialize=1 / len(self._params.component_list),
                                   bounds=(0, 1))

    def _make_liq_phase_eq(self):
        def rule_total_mass_balance(self):
            return self.flow_mol_phase['Liq'] == self.flow_mol
        self.eq_total = Constraint(rule=rule_total_mass_balance)

        def rule_comp_mass_balance(self, i):
            return self.flow_mol * self.mole_frac[i] == \
                self.flow_mol_phase['Liq'] * self.mole_frac_phase['Liq', i]
        self.eq_comp = Constraint(self._params.component_list,
                                  rule=rule_comp_mass_balance)

        if self.config.defined_state is False:
            # applied at outlet only
            self.eq_mol_frac_out = Constraint(expr=sum(self.mole_frac[i]
                                              for i in self._params.component_list)
                                              == 1)

    def _make_vap_phase_eq(self):
        def rule_total_mass_balance(self):
            return self.flow_mol_phase['Vap'] == self.flow_mol
        self.eq_total = Constraint(rule=rule_total_mass_balance)

        def rule_comp_mass_balance(self, i):
            return self.flow_mol * self.mole_frac[i] == \
                self.flow_mol_phase['Vap'] * self.mole_frac_phase['Vap', i]
        self.eq_comp = Constraint(self._params.component_list,
                                  rule=rule_comp_mass_balance)

        if self.config.defined_state is False:
            # applied at outlet only
            self.eq_mol_frac_out = Constraint(expr=sum(self.mole_frac[i]
                                              for i in self._params.component_list)
                                              == 1)

    def _make_flash_eq(self):
        self.vapor_pressure = Var(self._params.component_list,
                                  initialize=0.101325,
                                  doc="vapor pressure ",
                                  bounds=(0.01, None))

        def rule_total_mass_balance(self):
            return self.flow_mol_phase['Liq'] + \
                self.flow_mol_phase['Vap'] == self.flow_mol
        self.eq_total = Constraint(rule=rule_total_mass_balance)

        def rule_comp_mass_balance(self, i):
            return self.flow_mol * self.mole_frac[i] == \
                self.flow_mol_phase['Liq'] * self.mole_frac_phase['Liq', i] + \
                self.flow_mol_phase['Vap'] * self.mole_frac_phase['Vap', i]
        self.eq_comp = Constraint(self._params.component_list,
                                  rule=rule_comp_mass_balance)

        def rule_mole_frac(self):
            return sum(self.mole_frac_phase['Liq', i]
                       for i in self._params.component_list) -\
                sum(self.mole_frac_phase['Vap', i]
                    for i in self._params.component_list) == 0
        self.eq_sum_mol_frac = Constraint(rule=rule_mole_frac)

        if self.config.defined_state is False:
            # applied at outlet only
            self.eq_mol_frac_out = Constraint(expr=sum(self.mole_frac[i]
                                              for i in self._params.component_list)
                                              == 1)

        def rule_Keq(self, i):
            return self.mole_frac_phase['Vap', i] * self.pressure == \
                self.vapor_pressure[i] * self.mole_frac_phase['Liq', i]
        self.eq_Keq = Constraint(self._params.component_list, rule=rule_Keq)

        def rule_P_vap(self, j):
            return log(7500.6168 * self.vapor_pressure[j]) == \
                self._params.vapor_pressure_coeff[j, 'A'] - \
                (self._params.vapor_pressure_coeff[j, 'B'] /
                 (100*self.temperature - self._params.vapor_pressure_coeff[j, 'C']))
        self.eq_P_vap = Constraint(self._params.component_list, rule=rule_P_vap)

    def _density_mol(self):
        self.density_mol = Var(self._params.phase_list, doc="Molar density [kgmol/m^3]")

        def density_mol_calculation(self, p):
            if p == "Vap":
                return 10.0 * self.pressure == (self.density_mol[p] *
                                         self._params.gas_constant *
                                         self.temperature)
            elif p == "Liq":
                return self.density_mol[p] == 11.1  # kgmol/m3 # dummy value
        try:
            # Try to build constraint
            self.density_mol_calculation = Constraint(
                self._params.phase_list, rule=density_mol_calculation)
        except AttributeError:
            # If constraint fails, clean up so that DAE can try again later
            self.del_component(self.density_mol)
            self.del_component(self.density_mol_calculation)
            raise

    def get_material_flow_terms(self, p, j):
        """Create material flow terms for control volume."""
        if (p == "Vap") and (j in self._params.component_list):
            return self.flow_mol_phase['Vap'] * self.mole_frac_phase['Vap', j]
        elif (p == "Liq") and (j in self._params.component_list):
            return self.flow_mol_phase['Liq'] * self.mole_frac_phase['Liq', j]
        else:
            return 0

    def get_enthalpy_flow_terms(self, p):
        """Create enthalpy flow terms [MJ/s]."""
        if p == "Vap":
            return self.flow_mol_phase['Vap'] * self._params.Cp * self.temperature * 100
        elif p == "Liq":
            return self.flow_mol_phase['Liq'] * self._params.Cp * self.temperature * 100

    def get_material_density_terms(self, p, j):
        """Create material density terms."""
        if p == "Liq":
            if j in self._params.component_list:
                return self.density_mol[p] * self.mole_frac_phase['Liq', j]
            else:
                return 0
        elif p == "Vap":
            if j in self._params.component_list:
                return self.density_mol[p] * self.mole_frac_phase['Vap', j]
            else:
                return 0

    def get_enthalpy_density_terms(self, p):
        """Create enthalpy density terms."""
        if p == "Liq":
            return self.density_mol[p] * self._params.Cp
        elif p == "Vap":
            return self.density_mol[p] * self._params.Cp

    def define_state_vars(self):
        """Define state vars."""
        return {"flow_mol": self.flow_mol,
                "mole_frac": self.mole_frac,
                "temperature": self.temperature,
                "pressure": self.pressure}

    def model_check(blk):
        """Model checks for property block."""
        # Check temperature bounds
        if value(blk.temperature) < blk.temperature.lb:
            _log.error('{} Temperature set below lower bound.'
                       .format(blk.name))
        if value(blk.temperature) > blk.temperature.ub:
            _log.error('{} Temperature set above upper bound.'
                       .format(blk.name))

        # Check pressure bounds
        if value(blk.pressure) < blk.pressure.lb:
            _log.error('{} Pressure set below lower bound.'.format(blk.name))
        if value(blk.pressure) > blk.pressure.ub:
            _log.error('{} Pressure set above upper bound.'.format(blk.name))
