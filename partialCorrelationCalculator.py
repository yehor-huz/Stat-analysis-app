import numpy as np
import pandas as pd
import scipy.stats as stats

class PartialCorrelationCalculator:
    
    @staticmethod
    def calculate(df: pd.DataFrame, var_x: str, var_y: str, covar_list: list) -> dict:
        cols = [var_x, var_y] + covar_list
        data = df[cols].dropna()
        
        n = len(data)
        k = len(covar_list)
        dof = n - 2 - k
        
        if dof <= 0:
            return {'error': "Not enought degrees of freedom."}

        R = data.corr().values
        
        for ctrl_idx in range(2, 2 + k):
            R_new = np.zeros_like(R)
            
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    if i == j:
                        R_new[i, j] = 1.0
                        continue
                    
                    r_ij = R[i, j]
                    r_id = R[i, ctrl_idx]  
                    r_jd = R[j, ctrl_idx] 
                    
                    num = r_ij - r_id * r_jd
                    den = np.sqrt((1.0 - r_id**2) * (1.0 - r_jd**2))
                    
                    if den == 0:
                        R_new[i, j] = 0.0
                    else:
                        R_new[i, j] = num / den
                        
            R = R_new 

        r_partial = R[0, 1]
        
        r_partial = np.clip(r_partial, -1.0, 1.0)

        if np.isclose(abs(r_partial), 1.0):
            t_stat = np.inf
            p_val = 0.0
        else:
            t_stat = r_partial * np.sqrt(dof / (1 - r_partial**2))
            p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=dof))

        return {
            'r': r_partial,
            't_stat': t_stat,
            'p_value': p_val,
            'n': n,
            'dof': dof
        }