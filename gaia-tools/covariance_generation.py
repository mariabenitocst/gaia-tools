'''
File for storing functions and constants related to generating and transforming
data covariance matrices.
'''

import numpy as np

'''
Function that iterates over the DataFrame and appends covariances matrices to a 
dictonary with 'the source_id' as key.
'''
def generate_covmatrices(df):

    cov_dict = {}

    for i in range(df.shape[0]):
        
        # Select row
        sub_df = df.iloc[i]

        # Get covariance matrix
        C = generate_covmat(sub_df)

        # Append
        cov_dict[sub_df.source_id] = C

    return cov_dict


'''
Function that gets the covariance matrix of a specific point source (row in DataFrame).
'''
def generate_covmat(sub_df):

    #TODO: Add check if error and corr values dont exist - > Quit Function or Skip DF row.

    # Declare empty matrix
    C = np.zeros((6, 6))
    
    # Possible parameter names
    names = ['ra', 'dec', 'parallax', 'pmra', 'pmdec']
    
    # For Diagonal Elements
    for i, name in enumerate(names):
            ext = names[i] + "_error"   
            err = sub_df[ext]
 
            if(name == 'ra' or name == 'dec'):

                # This converts from [mas] to [deg]
                err = err/(3.6 * 10**6)

            C[i, i] = err ** 2
        
    # For Radial Velocity Element        
    C[5,5] = sub_df['radial_velocity_error'] ** 2        

    # For Rest of the Elements
    for i, name1 in enumerate(names):
                for j, name2 in enumerate(names):
                
                    if j <= i:
                        continue

                    ext = "{0}_{1}_corr".format(name1, name2)
                    corr = sub_df[ext]
               
                    # Sqrt because it accesses values from the main diagonal which are squared.
                    C[i, j] = corr * np.sqrt(C[i, i] * C[j, j])
                    C[j, i] = C[i, j]

    return C