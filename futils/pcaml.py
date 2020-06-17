def ewma_vectorized(data, alpha, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a vector.
    Will fail for large inputs.
    :param data: Input data
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param offset: optional
        The offset for the moving average, scalar. Defaults to data[0].
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the input. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if data.ndim > 1:
        # flatten input
        data = data.reshape(-1, order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        # empty input, return empty array
        return out

    if offset is None:
        offset = data[0]

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # scaling_factors -> 0 as len(data) gets large
    # this leads to divide-by-zeros below
    scaling_factors = np.power(1. - alpha, np.arange(data.size + 1, dtype=dtype),
                               dtype=dtype)
    # create cumulative sum array
    np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
                dtype=dtype, out=out)
    np.cumsum(out, dtype=dtype, out=out)

    # cumsums / scaling
    out /= scaling_factors[-2::-1]

    if offset != 0:
        offset = np.array(offset, copy=False).astype(dtype, copy=False)
        # add offsets
        out += offset * scaling_factors[1:]

    return out


def seuil(q, full_pca_dcovid, pc_res):
    numgspe = np.trace(np.square(np.diag(np.diag(full_pca_dcovid.explained_variance_)[pc_res, pc_res])))
    dengspe = np.trace(np.diag(np.diag(full_pca_dcovid.explained_variance_)[pc_res, pc_res]))
    gspe = numgspe/dengspe

    numhspe = np.square(np.trace(np.diag(np.diag(full_pca_dcovid.explained_variance_)[pc_res, pc_res])))
    denhspe = np.trace(np.square(np.diag(np.diag(full_pca_dcovid.explained_variance_)[pc_res, pc_res])))
    hspe = numhspe/denhspe
    
    return gspe*chi2.ppf(q, df=hspe)



from cutils.covidclass import CovidFr

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import json
import plotly
import os
from scipy.stats import chi2
from numpy.linalg import inv



covfr = CovidFr()
covfr.load_df()

d_covid = covfr.daily_covid
d_covid = d_covid.rename(columns={"incid_hosp": "hosp", "incid_rea": "rea", "incid_rad": "rad", "incid_dc": "dc"})
d_covid = d_covid[['dep', 'jour', 'hosp', 'rea', 'rad', 'dc']]
dcovid = d_covid.groupby("jour").sum().copy()


X_dcovid = dcovid.copy()

first_date = '2020-05-14'
last_date = '2020-06-14'

std = StandardScaler().fit(X_dcovid[(X_dcovid.index>=first_date) & (X_dcovid.index<=last_date)])
x_dcovid = std.transform(X_dcovid)
#x_dcovid = StandardScaler().fit_transform(X_dcovid)
x_dcovid = pd.DataFrame(x_dcovid, columns=X_dcovid.columns)
x_dcovid.index = X_dcovid.index


#full_pca_dcovid = PCA(n_components=4).fit(x_dcovid)
full_pca_dcovid = PCA(n_components=4).fit(x_dcovid[(x_dcovid.index>=first_date) & (x_dcovid.index<=last_date)])
print(full_pca_dcovid.explained_variance_ratio_)

pc_hat = [0, 1]
pc_res = [2, 3]

X_dcovid_reduced_hat = full_pca_dcovid.transform(x_dcovid)[:, pc_hat]
X_dcovid_reduced_res = full_pca_dcovid.transform(x_dcovid)[:, pc_res]

X_res = X_dcovid_reduced_res.copy()

Xt_res = np.transpose(X_res)
X_resXt_res = np.dot(X_res,Xt_res)

spe = np.diag(X_resXt_res)


X_hat = X_dcovid_reduced_hat.copy()

Xt_hat = np.transpose(X_hat)  
invlamda = inv(np.diag(np.diag(full_pca_dcovid.explained_variance_)[pc_hat, pc_hat]))
X_hatinvlamdaXt_hat = np.dot(np.dot(X_hat, invlamda), Xt_hat)

t2 = np.diag(X_hatinvlamdaXt_hat)

threshold_res = np.repeat(seuil(q=0.975, full_pca_dcovid=full_pca_dcovid, pc_res=pc_res), spe.shape[0])

threshold_t2 = np.repeat(chi2.ppf(q=0.975, df=invlamda.shape[0]), t2.shape[0])

def quadratics():

    graphs = [

        dict(
            id = 'SPE',
            data=[
                dict(
                    x=x_dcovid.index,
                    #y=spe,
                    y=ewma_vectorized(spe, 1-0.4),
                    type='line',
                    marker=dict(
                    color='#ff7f00',
                    line=dict(color='#ff7f00', width=3)
                    )
                ),

                dict(
                    x=x_dcovid.index,
                    y=threshold_res,
                    type='line',
                    marker=dict(
                    color='#ff0000',
                    line=dict(color='#ff0000', width=3)
                    )
                )

                
            ],
            layout=dict(
                #title="indice SPE",
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),

        dict(
            id = 'spe_t',
            data=[
                dict(
                    x=x_dcovid.index,
                    y=threshold_res,
                    type='line',
                    marker=dict(
                    color='#ff0000',
                    line=dict(color='#ff0000', width=3)
                    )
                ),
            ],
            layout=dict(
                #title="seuil indice spe",
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),
        
    ]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
     
    return graphJSON










