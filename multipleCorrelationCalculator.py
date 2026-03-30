import pandas as pd
import numpy as np
import scipy.stats as stats

class MultipleCorrelationCalculator:
    @staticmethod
    def calculate(df: pd.DataFrame, target_var: str, predictor_vars: list) -> dict:
        if not predictor_vars:
            return {'error': "CHoose at least one feature"}
            
        cols = [target_var] + predictor_vars
        data = df[cols].dropna()
        
        N = len(data)
        n = len(predictor_vars) 
        
        dof1 = n
        dof2 = N - n - 1
        
        if dof2 <= 0:
            return {'error': f"N ({N}) > n+1 ({n+1})."}

        full_corr_matrix = data.corr().values
        
        pred_corr_matrix = data[predictor_vars].corr().values
        
        det_full = np.linalg.det(full_corr_matrix)
        det_pred = np.linalg.det(pred_corr_matrix)
        
        if np.isclose(det_pred, 0.0):
            return {'error': "Multicolinear."}
            
        ratio = det_full / det_pred
        r_squared = max(0.0, 1.0 - ratio)
        r_mult = np.sqrt(r_squared)
        
        r_mult = min(r_mult, 1.0)
        r_squared = r_mult ** 2
        
        if np.isclose(r_squared, 1.0):
            f_stat = np.inf
            p_val = 0.0
        else:
            f_stat = ((N - n - 1) / n) * (r_squared / (1.0 - r_squared))
            p_val = stats.f.sf(f_stat, dof1, dof2)

        return {
            'r_mult': r_mult,
            'r_squared': r_squared,
            'f_stat': f_stat,
            'p_value': p_val,
            'N': N,
            'n_preds': n,
            'dof1': dof1,
            'dof2': dof2
        }