# Shift Scheduling

This script implements a basic weekly shift scheduling pattern for museums subject to certain constraints using linear programming. The scheduling aims to minimise cost to the museums.

The constraints and other parameters are as follows:

    * Each museum needs a certain minimum number of staff (called MVSAs) on each weekday (constraint)
    * The cost to the museum of the shift pattern is the total cost of the staff over that week
    * An MVSA may have preferences on how many days per week they work (constraint)
    * An MVSA can weigh different days according to their preference of working that day (this goes into the cost function as a penalty, rather than a constraint)
