''' Library for data importation and feature selection'''
###############################################################################
# Author:       Zane Markel
# Created:      6 MAR 2014
#
# Name:         mldata
# Description : Library for importing/exporting data and feature selection
#
###############################################################################

# sklearn models can import svmlight files for data
# In general, sklearn uses the following data format:
# attributes X = n_samples vector of n_features feature vector
# labels Y = n_samples vector of class values

# scikit learn will provide most of the baseline funtionality
import sklearn as sk
import numpy as np

# TODO: make it easy to import and export data
# check out numpy.recarray.tofile and .fromfile

def load_data(csv):
    ''' Import a csv file. Returns a structured array of the following format:
    [[name, feature0, ..., featuren, label], [name, ..., label], ...] 
    Note: "--" will be treated as a comment delimiter. I do not expect to use
    comments, but numpy.genfromtxt needs something.'''

    dformat = extract_headers(open(csv))

    # Load file data as a matrix
    data = np.genfromtxt(csv, delimiter=",", dtype=dformat, skip_header=1, \
           comments='--')

    return data

def save_data(data, fname):
    ''' Takes a record array (like that returned by mldata.load_data) and
    saves it as a .csv file that could be imported by mldata.load_data. '''

    # Open file for writing:
    out = open(fname, 'w')
    
    # Get header names
    hnames = data.dtype.names

    # Print header names
    hline = ', '.join(hnames) + '\n'
    out.write(hline)

    # For every line in the array...
    for record in data:
        # Print that line
        # (Use list comprehension to get a string version of the record)
        recline = ', '.join((str(x) for x in record)) + '\n'
        out.write(recline)

    # For clarity
    return


def data_components(data):
    ''' Converts a structured array of data into simple arrays containing the
    features (2d array), labels, record names, and the feature names.
    This is intended to be used after preprocessing as the final step before
    doing the actual learning.'''
    
    # Get filenames
    recnames = data['Name']

    # Get labels
    labels = data['isMalware']

    # Get features
    features = rm_feat_name(data, 'Name')
    features = rm_feat_name(features, 'isMalware')
    featnames = features.dtype.names
    features = features.view(np.int32).reshape(features.shape + (-1,))

    return (features, labels, recnames, featnames)

def rm_feat_num(features, num):
    ''' Return features, with a feature removed based on column (num)ber '''
    names = list(features.dtype.names)
    new_names = names[:num] + names[num+1:]
    return features[new_names]
    
def rm_feat_name(features, name):
    ''' Return features, with a feature "name" removed'''
    names = list(features.dtype.names)
    if name in names:
        names.remove(name)
    return features[names]

def extract_headers(openfile):
    ''' Extract the header line names and return a numpy.dtype for the
    dtype field of numpy.loadtxt''' 
    # for now just return the line as a string

    # Read the line
    headerline = openfile.readline()

    # Get the names
    nmes = headerline.strip().replace('"','').replace(' ','').split(',')

    # Generate types
    formats = ['i8']*len(nmes)
    formats[0] = 'a255' # First field will be the filename

    # Generate dictionary 
    dtdict = {'names':tuple(nmes), 'formats':tuple(formats) }
    
    # Return numpy.dtype object
    return np.dtype(dtdict)