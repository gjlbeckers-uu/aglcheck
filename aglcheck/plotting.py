import numpy as np

__all__ = ['plot_comparison']

def plot_comparison(comparisontable, cmap=None,
                    colorbarorientation='vertical',
                    colorbarshrink=1., clim=None, colorbarlabel='',
                    title=None):

    import matplotlib.pyplot as plt

    ct = comparisontable
    if title is None:
        title = ct.title
        if title is None:
            title = ''
    matrix = np.array(ct.get_matrix()).T
    mmin, mmax = matrix.min(), matrix.max()
    if np.issubdtype(matrix.dtype, np.int):
        intcolors = True
    else:
        intcolors = False
    if intcolors:
        if clim is None:
            clim = (mmin - 0.5, mmax + 0.5)
            ticks = [t for t in range(mmin, mmax + 1)]
            lut = mmax - mmin + 1
        else:
            ticks = [t for t in np.linspace(clim[0], clim[1], clim[1]-clim[0]+1)]
            clim = (clim[0] - 0.5, clim[1] + 0.5)
            lut = clim[1] - clim[0] + 1
    else:
        ticks = None
        lut = None
    if cmap is None:
        if intcolors:
            cmap = plt.cm.get_cmap('jet', lut)
        else:
            cmap = plt.cm.get_cmap('viridis', lut)
    else:
        cmap = plt.cm.get_cmap(cmap, lut)
    ax = plt.gca()
    plt.imshow(matrix, interpolation='nearest', cmap=cmap, clim=clim)
    plt.xticks(np.arange(len(ct.xstringlabels)), ct.xstringlabels)
    plt.yticks(np.arange(len(ct.ystringlabels)), ct.ystringlabels)
    plt.xticks(rotation=70)
    for xticklabel in ax.get_xticklabels():
        color = ct.stringdata.stringlabelcolors[xticklabel.get_text()]
        xticklabel.set_color(color)
    for yticklabel in ax.get_yticklabels():
        color = ct.stringdata.stringlabelcolors[yticklabel.get_text()]
        yticklabel.set_color(color)
    plt.title(title)
    plt.colorbar(orientation=colorbarorientation,
                 ticks=ticks,
                 shrink=colorbarshrink,
                 label=colorbarlabel)
    return ax

def plot_comparisons(*args, clim=None, colorbarorientation='vertical',
                     colorbarshrink=1.,colorbarlabel=''):

    import matplotlib.pyplot as plt

    low = np.inf
    high = -np.inf
    for ct in args:
        ar = np.array(ct.get_matrix())
        low = min(low, ar.min())
        high = max(high, ar.max())
        clim = (low, high)
    axes = []
    for i,ct in enumerate(args, 1):
        plt.subplot(1,len(args),i)
        axes.append(plot_comparison(ct, cmap=None,
                                    colorbarorientation=colorbarorientation,
                                    colorbarshrink=colorbarshrink, clim=clim,
                                    colorbarlabel=colorbarlabel,
                                    title=None))
    return axes