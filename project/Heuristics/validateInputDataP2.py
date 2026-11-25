"""
AMMM Lab Heuristics
Instance file validator v2.0
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all scheduling parameters were found
        for paramName in ('N', 'L', 'U', 'T', 'P', 'E'):
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate horizon and run lengths
        for paramName in ('N', 'L', 'U'):
            value = getattr(data, paramName)
            if type(value) is not int or value <= 0:
                raise AMMMException('%s(%s) has to be a positive integer.' % (paramName, value))

        if not 1 <= data.L <= data.U <= data.N:
            raise AMMMException('Run lengths must satisfy 1 <= L <= U <= N.')

        if type(data.T) not in (int, float) or data.T < 0:
            raise AMMMException('T(%s) has to be a non-negative number.' % data.T)

        # Validate per-period profit and energy vectors
        for paramName in ('P', 'E'):
            values = list(getattr(data, paramName))
            if len(values) != data.N:
                raise AMMMException('%s must have N(%s) values.' % (paramName, data.N))
            if any(type(value) not in (int, float) or value < 0 for value in values):
                raise AMMMException('%s values must be non-negative numbers.' % paramName)
            setattr(data, paramName, values)

