import numpy as np
import pandas as pd
from scipy import stats

class CorrelationCalculator:
    
    def calculate_pearson(self, df: pd.DataFrame):
        r_matrix = df.corr(method='pearson')
        n = len(df.dropna())
        
        with np.errstate(divide='ignore', invalid='ignore'):
            t_matrix = r_matrix * np.sqrt((n - 2) / (1 - r_matrix**2))
            
        for i in range(len(t_matrix.columns)):
            t_matrix.iloc[i, i] = np.inf
            
        return r_matrix, t_matrix

    def calculate_spearman(self, df: pd.DataFrame):
        rho_matrix = df.corr(method='spearman')
        n = len(df.dropna())
        
        with np.errstate(divide='ignore', invalid='ignore'):
            t_matrix = rho_matrix * np.sqrt((n - 2) / (1 - rho_matrix**2))
            
        for i in range(len(t_matrix.columns)):
            t_matrix.iloc[i, i] = np.inf
            
        return rho_matrix, t_matrix

    def calculate_kendall(self, df: pd.DataFrame):
        tau_matrix = df.corr(method='kendall')
        n = len(df.dropna())
        
        z_matrix = tau_matrix * np.sqrt((9 * n * (n - 1)) / (2 * (2 * n + 5)))
        
        for i in range(len(z_matrix.columns)):
            z_matrix.iloc[i, i] = np.inf
            
        return tau_matrix, z_matrix

    def calculate_correlation_ratio(self, df: pd.DataFrame):
        cols = df.columns
        eta_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
        sig_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
        
        for x in cols:
            for y in cols:
                if x == y:
                    eta_matrix.loc[x, y] = 1.0
                    sig_matrix.loc[x, y] = np.inf
                    continue
                
                valid_data = df[[x, y]].dropna()
                n = len(valid_data)
                
                if n < 2:
                    eta_matrix.loc[x, y] = np.nan
                    sig_matrix.loc[x, y] = np.nan
                    continue
                
                y_mean = valid_data[y].mean()
                ss_total = np.sum((valid_data[y] - y_mean)**2)
                
                grouped = valid_data.groupby(x)[y]
                m_i = grouped.count()         
                y_i_mean = grouped.mean()    
                
                ss_between = np.sum(m_i * (y_i_mean - y_mean)**2)
                
                if ss_total == 0:
                    eta_squared = 0.0
                else:
                    eta_squared = ss_between / ss_total
                
                eta_squared = np.clip(eta_squared, 0.0, 1.0)
                eta_matrix.loc[x, y] = np.sqrt(eta_squared)
                
                k = len(m_i) 
                
                if k > 1 and k < n and eta_squared < 1.0:
                    f_stat = (eta_squared / (k - 1)) / ((1 - eta_squared) / (n - k))
                    sig_matrix.loc[x, y] = f_stat
                elif eta_squared == 1.0:
                    sig_matrix.loc[x, y] = np.inf
                else:
                    sig_matrix.loc[x, y] = np.nan
                    
        return eta_matrix, sig_matrix