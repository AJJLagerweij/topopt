"""
This is the main progam code that sets up the topology optimisation problem.
This optimisation tries to mimimize the global compliance and thus maximizing
the stiffness.

Bram Lagerweij
Aerospace Structures and Materials Department TU Delft
2018
"""

# importing external modules
import time
import math

# importing custom modules
from loads import HalfBeam, Beam, Canti, Michell, BiAxial
from constraints import DensityConstraint
from fesolvers import FESolver, CvxFEA, CGFEA
from topopt import Topopt
from plotting import Plot

if __name__ == "__main__":
    # material properties
    young = 1
    poisson = 0.3

    # constraints
    Emin = 1e-9
    volfrac = 0.4
    move = 1

    # mesh dimensions
    nelx = 200
    nely = 50

    # optimizer parameters
    penal = 3.0
    rmin = 3
    filt = 'sensitivity'
    loopy = 1000  # math.inf
    delta = 0.005

    # plotting and printing options
    verbose = True
    plotting = True
    save_plot = False
    history = False

    # constraints object created
    den_con = DensityConstraint(nelx, nely, move, volume_frac=volfrac)

    # loading case object, other classes can be selected and created
    load = Canti(nelx, nely, young, Emin, poisson)

    # FEA object is generated, other solvers can be selected and created
    fesolver = CvxFEA(verbose=verbose)

    # create optimizer object and initialise the problem
    optimizer = Topopt(den_con, load, fesolver, verbose=verbose)

    # execute the optimization
    t = time.time()
    x, x_history = optimizer.layout(penal, rmin, delta, loopy, filt, history)
    print('Elapsed time is: ', time.time() - t, 'seconds.')

    # plotting
    pl = Plot(load, title='Cantilever beam example 1600x300 elementen')
    pl.boundary(load)
    pl.loading(load)

    if history:
        for i in x_history:
            pl.add(i, animated=True)
        pl.save('video')

    pl.add(x, animated=False)

    if save_plot:
        pl.save('figure')

    if plotting:
        pl.show()
