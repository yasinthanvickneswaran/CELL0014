import numpy as np

def draw_direction_field(ax, sdot, params, 
                            x_index = 0,
                            y_index = 1,
                            s0=None,
                            t=0,
                            color='k',
                            nx=30, ny=30,
                            switch_axes=False,
                            normalise=False, 
                            dynamic_range=None,
                            clip_negative=True,
                            scale_to_axes=True
                            ):

    # This function draws a direction field onto a phase plot when prodiced with an sdot function that models.
    # a system with *TWO* state variables.
    #
    # It uses the current axes ranges of the phase plot to calculate grid points. Please adjust this before
    # calling this function, as rescaling after the calculation will cause a mismatch between trajectory and
    # vector axis scales, so that the arrow directions will be misaligned.
    #
    # OPTIONAL ARGUMENTS:
    #
    # nx, ny define the number of arrows drawn. Default is a 30 x 30 grid
    #
    # switch_axes=True can be used if the phase plot has s[0] is plotted on the Y axis and s[1] is on the X axis.
    #
    # normalise=True
    #   enables us to normalise the arrow size (so that they are all the same length)
    #
    # scale_to_axes=True
    #  This applies a transform so that the plotted arrows point along the
    #   phase trajectories correctly
    #  (needed when the x and y scales are different)
    #
    # clip_negative=True
    #  do not draw arrows in the negative value regions 
    #
    # dyn_range=1.0
    #  this can be adjusted from 0 to 1. This allows us to rescale the arrow lengths
    #  so that arrow length proportional to gradient^dyn_range
    #  - dyn_range=0 is equivalent to normalising the arrows
    #  - dyn_range=1 means arrow length is proportional to gradient
    #  when we have very small and very large arrows setting dyn_range to
    #  a value between 0 and 1 allows us to see small arrows but still retain
    #  some information on their magnitude
    #
    
    
    if x_index is None:
        x_index = 0
    
    if y_index is None:
        y_index = 1
        
    if switch_axes:
        x_index = 1
        y_index = 0        

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    if clip_negative and x_min<0:
        x_min=0
    if clip_negative and y_min<0:
        y_min=0   
            
    x_pos=np.linspace(x_min, x_max, nx)
    y_pos=np.linspace(y_min, y_max, ny)

    x_mesh, y_mesh=np.meshgrid(x_pos, y_pos)
    mesh_rows,mesh_cols=x_mesh.shape
    dx_mesh=np.zeros([mesh_rows,mesh_cols])
    dy_mesh=np.zeros([mesh_rows,mesh_cols])

    if s0 is None:
        s0 = [None, None]
    
    ## calculate vector field w
    for i in range(mesh_rows):
        for j in range(mesh_cols):
            xi=x_mesh[i,j]
            yi=y_mesh[i,j]
            s0[x_index]=xi
            s0[y_index]=yi
            dS=sdot(s0,t,params)
            dx_mesh[i,j]=dS[x_index]
            dy_mesh[i,j]=dS[y_index]
               
    # This normalises all arrows to the same length
    # set normalise=False to turn this off
    if normalise and dynamic_range!=None:
        print("Warning cannot use a dynamic range when arrows are normalised...")
        print("(ignoring dynamic range value)")
    if dynamic_range is None:
        dynamic_range=1.0
    if normalise:
        dynamic_range=0.0
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    x_range=cur_xlim[1]-cur_xlim[0]
    y_range=cur_ylim[1]-cur_ylim[0]
    n_rows,n_cols=dx_mesh.shape
    for i in range(n_rows):
        for j in range(n_cols):
            x,y=dx_mesh[i,j],dy_mesh[i,j]
            if scale_to_axes:
                x=x/x_range
                y=y/y_range
            if dynamic_range!=1.0:
                l=(x**2 + y**2)**0.5
                if l!=0:
                    x=x/l**(1.0-dynamic_range)
                    y=y/l**(1.0-dynamic_range)
            dx_mesh[i,j],dy_mesh[i,j]=x,y
    
    # This draws on the direction field
    ax.quiver(x_mesh, y_mesh, dx_mesh, dy_mesh,pivot='middle',color=color)

    
