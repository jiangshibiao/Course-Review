import numpy as np
import scipy.sparse
import scipy.stats


def Eudist2(x, y):
    def square(m):
        if isinstance(m, np.ndarray):
            return m * m
        else:
            return m.multiply(m)
    distance = -2 * (x @ y.T)
    if not isinstance(distance, np.ndarray):
        distance = distance.toarray()
    distance += np.sum(square(x), axis=1).reshape((x.shape[0], 1))
    distance += np.sum(square(y), axis=1).reshape((1, y.shape[0]))
    return distance


def NormalizeFea(fea):
    fea_norm = np.sum(np.multiply(fea, fea), axis=1)
    fea_norm = np.max(np.finfo(fea_norm.dtype), fea_norm) ** 0.5
    return fea * fea_norm.reshape((fea.shape[0], 1))


def constructW(fea, NeighborMode='KNN', WeightMode='HeatKernel', **kwargs):
    """
        Usage:
        W = constructW(fea, options)

        fea: Rows of vectors of data points. Each row is x_i
        options: Struct value in Matlab. The fields in options that can be set:

                NeighborMode -  Indicates how to construct the graph. Choices
                                are: [Default 'KNN']
                    'KNN'             -  k = 0
                                            Complete graph
                                         k > 0
                                           Put an edge between two nodes if and
                                           only if they are among the k nearst
                                           neighbors of each other. You are
                                           required to provide the parameter k in
                                           the options. Default k=5.
                    'Supervised'      -  k = 0
                                            Put an edge between two nodes if and
                                            only if they belong to same class.
                                         k > 0
                                            Put an edge between two nodes if
                                            they belong to same class and they
                                            are among the k nearst neighbors of
                                            each other.
                                         Default: k=0
                                        You are required to provide the label
                                        information gnd in the options.

                WeightMode   -  Indicates how to assign weights for each edge
                                in the graph. Choices are:
                    'Binary'        - 0-1 weighting. Every edge receiveds weight
                                      of 1.
                    'HeatKernel'    - If nodes i and j are connected, put weight
                                      W_ij = exp(-norm(x_i - x_j)/2t^2). You are
                                      required to provide the parameter t. [Default One]
                    'Cosine'        - If nodes i and j are connected, put weight
                                      cosine(x_i,x_j).

                k           -   The parameter needed under 'KNN' NeighborMode.
                                Default will be 5.
                gnd         -   The parameter needed under 'Supervised'
                                NeighborMode.  Colunm vector of the label
                                information for each data point.
                bLDA        -   0 or 1. Only effective under 'Supervised'
                                NeighborMode. If 1, the graph will be constructed
                                to make LPP exactly same as LDA. Default will be
                                0.
                t           -   The parameter needed under 'HeatKernel'
                                WeightMode. Default will be 1
                bNormalized -   0 or 1. Only effective under 'Cosine' WeightMode.
                                Indicates whether the fea are already be
                                normalized to 1. Default will be 0
            bSelfConnected  -   0 or 1. Indicates whether W(i,i) == 1. Default 0
                                if 'Supervised' NeighborMode & bLDA == 1,
                                bSelfConnected will always be 1. Default 0.
                 bTrueKNN   -   0 or 1. If 1, will construct a truly kNN graph
                                (Not symmetric!). Default will be 0. Only valid
                                for 'KNN' NeighborMode


        Examples:

            fea = rand(50,15);
            options = [];
            options.NeighborMode = 'KNN';
            options.k = 5;
            options.WeightMode = 'HeatKernel';
            options.t = 1;
            W = constructW(fea,options);


            fea = rand(50,15);
            gnd = [ones(10,1);ones(15,1)*2;ones(10,1)*3;ones(15,1)*4];
            options = [];
            options.NeighborMode = 'Supervised';
            options.gnd = gnd;
            options.WeightMode = 'HeatKernel';
            options.t = 1;
            W = constructW(fea,options);


            fea = rand(50,15);
            gnd = [ones(10,1);ones(15,1)*2;ones(10,1)*3;ones(15,1)*4];
            options = [];
            options.NeighborMode = 'Supervised';
            options.gnd = gnd;
            options.bLDA = 1;
            W = constructW(fea,options);


        For more details about the different ways to construct the W, please
        refer:
            Deng Cai, Xiaofei He and Jiawei Han, "Document Clustering Using
            Locality Preserving Indexing" IEEE TKDE, Dec. 2005.


        Written by Deng Cai (dengcai2 AT cs.uiuc.edu), April/2004, Feb/2006,
                                                  May/2007
    """

    # deal with options
    def set_default(key, value):
        if key not in kwargs:
            kwargs[key] = value

    if NeighborMode.lower() == 'KNN'.lower():
        set_default('k', 5)
    elif NeighborMode.lower() == 'Supervised'.lower():
        set_default('bLDA', 0)
        if kwargs['bLDA']:
            set_default('bSelfConnected', 1)
        set_default('k', 0)
        if 'gnd' not in kwargs:
            raise Exception('Label(gnd) should be provided under \'Supervised\' NeighborMode!')
        if len(kwargs['gnd']) != len(fea):
            raise Exception('gnd doesn\'t match with fea!')
    else:
        raise Exception('NeighborMode does not exist!')

    bBinary = 0
    bCosine = 0

    if WeightMode.lower() == 'Binary'.lower():
        bBinary = 1
    elif WeightMode.lower() == 'HeatKernel'.lower():
        if 't' not in kwargs:
            fea_sample = fea
            if fea.shape[0] > 3000:
                fea_sample = fea[np.random.permutation(np.arange(1, fea.shape[0]))[:3000]]
            d = Eudist2(fea_sample, fea_sample)
            kwargs['t'] = np.mean(d)
    elif WeightMode.lower() == 'Cosine'.lower():
        kwargs['bNormalized'] = kwargs.get('bNormalized', 0)
        bCosine = 1
    else:
        raise Exception('WeightMode does not exist!')

    set_default('bSelfConnected', 0)

    if 'gnd' in kwargs:
        nSmp = len(kwargs['gnd'])
    else:
        nSmp = fea.shape[0]

    maxM = 62500000  # 500M
    BlockSize = max(1, maxM // (nSmp * 3))

    if NeighborMode.lower() == 'Supervised'.lower():
        raise NotImplementedError("Supervised is not implimented and it is not needed in this Homework")

    Normfea = fea
    if bCosine and not kwargs['bNormalized']:
        Normfea = NormalizeFea(fea)
    
    #print (kwargs)

    # Always Use Euclidean distance to get K-nearest-neighbor
    # But if feature is normalized, we **could** (but actually TA do not) use inner-produce to sort
    if NeighborMode.lower() == 'KNN'.lower():
        k = kwargs['k']
        G = np.zeros((3, nSmp * (k + 1)))
        for block in range(0, nSmp, BlockSize):
            block_end = min(nSmp, block + BlockSize)

            dist = Eudist2(fea[block: block_end, :], fea)

            # build KNN
            arg_p = np.argpartition(dist, k + 1)[:, :k + 1]  # get index of minium K + 1
            dist = dist[np.arange(dist.shape[0])[:, None], arg_p]  # distance of min K + 1
            arg_s = np.argsort(dist)  # sort it
            idx = arg_p[np.arange(dist.shape[0])[:, None], arg_s]  # get index of min
            dump = dist[np.arange(dist.shape[0])[:, None], arg_s]  # get value of min

            if not bBinary:
                if bCosine:
                    dist = Normfea[block:block_end, :] @ Normfea.T  # inner product of normalized feature is cosin
                    dump = dist[np.arange(dist.shape[0])[:, None], idx]
                else:
                    dump = np.exp(-dump / (2 * kwargs['t'] * kwargs['t']))

            G[0, block * (k + 1):block_end * (k + 1)] = \
                np.repeat(np.arange(block, block_end), k + 1)
            G[1, block * (k + 1):block_end * (k + 1)] = idx.flatten()
            if not bBinary:
                G[2, block * (k + 1):block_end * (k + 1)] = dump.flatten()
            else:
                G[2, block * (k + 1):block_end * (k + 1)] = 1
        W = scipy.sparse.coo_matrix((G[2], (G[0], G[1])), shape=(nSmp, nSmp))
        if not kwargs['bSelfConnected']:
            W.setdiag(0)
        if not kwargs.get('bTrueKNN', False):
            W = W.maximum(W.T)
    return W
