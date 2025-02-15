from pymannkendall import original_test as mk_test

def calculate_statistics(df):
    df['yearly_avg'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean(axis=1)
    df['amplitude'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max(axis=1) - df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min(axis=1)

    mk_results = {}
    for metric in ['Tau', 'p', 'h', 's', 'var_s']:
        try:
            mk_results[metric] = {month: getattr(mk_test(df[month]), metric) for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_results[metric] = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}

    stats = {
        'Variance': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().to_dict(),
        'Standard Deviation': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().to_dict()
    }

    overall_avg = df[['yearly_avg']].mean().values[0]
    cv = {month: str(round((std / overall_avg) * 100, 2)) + '%' if std else None for month, std in stats['Standard Deviation'].items()}

    return stats, mk_results, cv