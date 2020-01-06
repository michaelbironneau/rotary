from scipy.optimize import linprog

# days
DAYS = ["mon", "tues", "weds", "thurs", "fri", "sat"]

# museums

museum_1 = {
  "name": "museum_1",
  "reqs": {
    "mon": 1,
    "tues": 1,
    "weds": 1,
    "thurs": 1,
    "fri": 1,
    "sat": 1,
  }
}

museum_2 = {
  "name": "museum_2",
  "reqs": {
    "mon": 1,
    "tues": 1,
    "weds": 1,
    "thurs": 1,
    "fri": 1,
    "sat": 1,
  }
}

# mvsas

bob = {
  "name": "bob",
  "days_per_week_pref": 5,
  "weighing": {
    "mon": 1,
    "tues": 1,
    "weds": 1,
    "thurs": 1,
    "fri": 1,
    "sat": 1,
  }
}

sue = {
  "name": "sue",
  "days_per_week_pref": 4,
  "weighing": {
    "mon": 1,
    "tues": 1,
    "weds": 1,
    "thurs": 1,
    "fri": 1,
    "sat": 1,
  }
}

marie = {
  "name": "marie",
  "days_per_week_pref": 4,
  "weighing": {
    "mon": 1,
    "tues": 1,
    "weds": 1,
    "thurs": 1,
    "fri": 9,
    "sat": 9,
  }
}

def get_variables_list(museums, mvsas, days):
    """Return variables in order that they appear in optimisation matrices"""
    ret = []
    for m in museums:
        for p in mvsas:
            for d in days:
                ret.append(m["name"] + ": " + p["name"] + ": " + d)
    return ret


def get_objective_function(museums, mvsas, days, direction="min"):
    """Return the objective function vector coefficients (minimization problem)"""
    coeffs = []
    sign = 1
    if direction == "max":
        sign = -1
    for _ in museums:
        for p in mvsas:
            for d in days:
                coeffs.append(sign*p["weighing"][d])
    return coeffs

def ix(museum_ix, mvsas_ix, day_ix, p_len, d_len):
    """Return the index of the variable list represented by the composite indexes"""
    return day_ix + (d_len)*(mvsas_ix + (p_len)*(museum_ix))

def get_museum_req_constraints(museums, mvsas, days):
    """Museum must have at least N MVSAs on given day"""
    constraints = []
    constraint_b = []
    for museum_ix, m in enumerate(museums):
        for day_ix, d in enumerate(days):
            m_reqs = m["reqs"][d]
            constraints.append([0]*len(mvsas)*len(museums)*len(days)) 
            constraint_b.append(-1*m_reqs)  # times by -1 to convert to <=
            for mvsa_ix, _ in enumerate(mvsas):
                constraints[len(constraints)-1][ix(museum_ix, mvsa_ix, day_ix, len(mvsas), len(days))] = -1
    return (constraints, constraint_b)

def get_mvsa_hour_constraints(museums, mvsas, days):
    """MVSA must work at least this many days"""
    constraints = []
    constraint_b = []
    for mvsa_ix, p in enumerate(mvsas):
        constraints.append([0]*len(mvsas)*len(museums)*len(days))
        constraint_b.append(-1*p["days_per_week_pref"])
        for museum_ix, _ in enumerate(museums):            
            for day_ix, _ in enumerate(days):
                constraints[len(constraints)-1][ix(museum_ix, mvsa_ix, day_ix, len(mvsas), len(days))] = -1
    return (constraints, constraint_b)

def get_mvsa_one_shift_at_a_time_constraints(museums, mvsas, days):
    """MVSA can only be in one place at a time"""
    constraints = []
    constraint_b = []
    for mvsa_ix, _ in enumerate(mvsas):
        for day_ix, _ in enumerate(days):  
            constraints.append([0]*len(mvsas)*len(museums)*len(days))
            constraint_b.append(1)          
            for museum_ix, _ in enumerate(museums):
                constraints[len(constraints)-1][ix(museum_ix, mvsa_ix, day_ix, len(mvsas), len(days))] = 1
    return (constraints, constraint_b)


def get_boundary_conditions(museums, mvsas, days):
    """Return that each var must between 0 and 1"""
    return [(0,1)]*len(museums)*len(mvsas)*len(days)


MUSEUMS = [museum_1, museum_2]
MVSAS = [bob, sue, marie]

c = get_objective_function(MUSEUMS, MVSAS, DAYS)
A = []
b = []

cons, cons_b = get_museum_req_constraints(MUSEUMS, MVSAS, DAYS)
A = A + cons 
b = b + cons_b 

cons2, cons_b2 = get_mvsa_hour_constraints(MUSEUMS, MVSAS, DAYS) 
A = A + cons2 
b = b + cons_b2

cons3, cons_b3  = get_mvsa_one_shift_at_a_time_constraints(MUSEUMS, MVSAS, DAYS)
A = A + cons3 
b = b + cons_b3

boundaries = get_boundary_conditions(MUSEUMS, MVSAS, DAYS)

res = linprog(c, A_ub=A, b_ub=b, bounds=boundaries, method="simplex")

if not res.success or res.status == 2 or res.status == 3:
    print("Optimisation not feasible")
else:
    x = res.x 
    vars = get_variables_list(MUSEUMS, MVSAS, DAYS)
    for shifts_ix, s in enumerate(x):
        if s > 0:
            print(vars[shifts_ix])

