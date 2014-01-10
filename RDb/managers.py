from django.db.models.query import QuerySet
import numpy as np
import pandas as pd
from django.db import models
from model_utils.managers import PassThroughManager
"""
Created on Wed Jan  8 22:43:33 2014

@author: acumen, chrisdev
"""
table_prefix = 'RDb_ne'

periodictable = (    "t", \
                     "H",                                                                                   "He", \
                     "Li","Be",                                                    "B", "C", "N", "O", "F", "Ne", \
                     "Na","Mg",                                                    "Al","Si","P", "S", "Cl","Ar", \
                     "K", "Ca",  "Sc","Ti","V", "Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", \
                     "Rb","Sr",  "Y", "Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I", "Xe", \
                     "Cs","Ba", \
                     "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb", \
                                 "Lu","Hf","Ta","W", "Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn", \
                     "Fr","Ra", \
                     "Ac","Th","Pa","U", "Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No", \
                                 "Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Uus","Uuo", \
                     "e"    )
e2elem = { "t":"Time",
    "H":"Hydrogen","He":"Helium","Li":"Lithium","Be":"Beryllium","B":"Boron","C":"Carbon","N":"Nitrogen","O":"Oxygen","F":"Fluorine","Ne":"Neon",
    "Na":"Sodium","Mg":"Magnesium","Al":"Aluminum","Si":"Silicon","P":"Phosphorous","S":"Sulfur","Cl":"Chlorine","Ar":"Argon",
    "K":"Potassium","Ca":"Calcium","Sc":"Scandium","Ti":"Titanium","V":"Vanadium","Cr":"Chromium","Mn":"Manganese","Fe":"Iron","Co":"Cobalt","Ni":"Nickel","Cu":"Copper","Zn":"Zinc","Ga":"Gallium","Ge":"Germanium","As":"Arsenic","Se":"Selenium","Br":"Bromine","Kr":"Krypton",
    "Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium","Nb":"Niobium","Mo":"Molybdenum","Tc":"Technetium","Ru":"Ruthenium","Rh":"Rhodium","Pd":"Palladium","Ag":"Gold","Cd":"Cadmium","In":"Indium","Sn":"Tin","Sb":"Antimony","Te":"Tellurium","I":"Iodine","Xe":"Xenon",
    "Cs":"Caesium","Ba":"Barium","La":"Lanthanum","Ce":"Cerium","Pr":"Praseodymium","Nd":"Neodymium","Pm":"Promethium","Sm":"Samarium","Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium","Ho":"Holonium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium",
    "Lu":"Lutetium","Hf":"Hafnium","Ta":"Tantalum","W":"Tungsten","Re":"Rhenium","Os":"Osmium","Ir":"Iridium","Pt":"Plutonium","Au":"Gold","Hg":"Mercury","Tl":"Thallium","Pb":"Lead","Bi":"Bismuth","Po":"Polonium","At":"Astatine","Rn":"Radon","Fr":"Francium","Ra":"Radium",
    "Ac":"Actinium","Th":"Thorium","Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium","Am":"Americium","Cm":"Curium","Bk":"Berkelium","Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendelevium","No":"Nobelium",
    "Lr":"Lawrencium","Rf":"Rutherfordium","Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium","Mt":"Meitnerium","Ds":"Darmstadtium","Rg":"Roentgenium","Cn":"Copernicum","Uut":"Ununtrium","Fl":"Flerovium","Uup":"Ununpentium","Lv":"Livermorium","Uus":"Ununseptium","Uuo":"Ununoctium",
    "e":"Energy"}

# Thanks to 'chrisdev' for the Django-Pandas code.
class DataFrameQuerySet(QuerySet):

    def to_pivot_table(self, *fields, **kwargs):
        """
        A convenience method for creating a time series i.e the
        DataFrame index is instance of a DateTime or PeriodIndex
        
        Parameters
        ----------
        fields: The model fields to utilise in creating the frame.
        to span a relationship, just use the field name of related
        fields across models, separated by double underscores,
        values : column to aggregate, optional
        rows : list of column names or arrays to group on
        Keys to group on the x-axis of the pivot table
        cols : list of column names or arrays to group on
        Keys to group on the y-axis of the pivot table
        aggfunc : function, default numpy.mean, or list of functions
        If list of functions passed, the resulting pivot table will have
        hierarchical columns whose top level are the function names
        (inferred from the function objects themselves)
        fill_value : scalar, default None
        Value to replace missing values with
        margins : boolean, default False
        Add all row / columns (e.g. for subtotal / grand totals)
        dropna : boolean, default True
        Do not include columns whose entries are all NaN
        """
        df = self.to_dataframe(*fields)
        values = kwargs.pop('values')
        rows = kwargs.pop('rows')
        cols = kwargs.pop('cols')
        aggfunc = kwargs.pop('aggfunc', np.mean)
        fill_value = kwargs.pop('fill_value', None)
        margins = kwargs.pop('margins', False)
        dropna = kwargs.pop('dropna', False)

        return pd.pivot_table(df, values=values,
                              fill_value=fill_value,
                              rows=rows, cols=cols,
                              aggfunc=aggfunc,
                              margins=margins,
                              dropna=dropna)

    def to_timeseries(self, *fields, **kwargs):
        """
        A convenience method for creating a time series i.e. the
        DataFrame index is instance of a DateTime or PeriodIndex
        
        Parameters
        ----------
        
        fields: The model fields to utilise in creating the frame.
        to span a relationship, just use the field name of related
        fields across models, separated by double underscores,
        
        index: Specify the field to use for the index. If the index
        field is not in the field list it will be appended. This
        is mandatory.
        
        storage: Specify if the queryset uses the `wide` or `long` format
        for data.
        
        pivot_column: Required once the you specify `long` format
        storage. This could either be a list or string identifying
        the field name or combination of field. If the pivot_column
        is a single column, then the unique values in this column become
        new columns in the DataFrame
        If the pivot column is a list the values in these columns are
        concatenated (using the '-' as a separator)
        and these values are used for the new timeseries columns
        
        values: Also required if you utilize the `long` storage the
        values column name is use for populating new frame values
        
        freq: The offset string or object representing a target conversion
        
        rs_kwargs: Arguments based on pandas.DataFrame.resample
        """
        index = kwargs.pop('index', None)

        if not index:
            raise AssertionError('You must supply an index field')

        storage = kwargs.get('storage', 'wide')

        if storage not in ['wide', 'long']:
            raise AssertionError('storage must be wide or long')

        if storage == 'wide':
            df = self.to_dataframe(*fields, index=index)
        else:
            df = self.to_dataframe(*fields)
            values = kwargs.get('values', None)
            if values is None:
                raise AssertionError('You must specify a values field')

            pivot_columns = kwargs.get('pivot_columns', None)
            if pivot_columns is None:
                raise AssertionError('You must specify pivot_columns')

            if isinstance(pivot_columns, list):
                df['combined_keys'] = ''
                for c in pivot_columns:
                    df['combined_keys'] += df[c].str.upper() + '.'

                df['combined_keys'] += values.lower()

                df = df.pivot(index=index,
                              columns='combined_keys',
                              values=values)
            else:
                df = df.pivot(index=index,
                              columns=pivot_columns,
                              values=values)
        rule = kwargs.get('freq', None)

        if rule:
            rs_kwargs = kwargs.get('rs_kwargs', None)
            if rs_kwargs:
                df = df.resample(rule, **rs_kwargs)
            else:
                df = df.resample(rule)
        return df

    def to_dataframe(self, *fields, **kwargs):
        """
        Returns a DataFrame from the queryset
        
        Paramaters
        -----------
        
        fields: The model fields to utilise in creating the frame.
        to span a relationship, just use the field name of related
        fields across models, separated by double underscores,
        
        
        index: Specify the field to use for the index. If the index
        field is not in the field list it will be appended
        
        fill_na: Fill in missing observations using one of the following
        this is a string specifying a pandas fill method
        {'backfill, 'bill', 'pad', 'ffill'} or a scalar value
        
        coerce_float: Attempt to convert the numeric non-string fields
        like object, decimal etc. to float if possible
        """
        index = kwargs.pop('index', None)
        fill_na = kwargs.pop('fill_na', None)
        coerce_float = kwargs.pop('coerce_float', False)
        if not fields:
            fields = tuple(self.model._meta.get_all_field_names())
        if index is not None:
            # add it to the fields if not already there
            if index not in fields:
                fields = fields + (index,)

        qs = self.values_list(*fields)
        recs = None
        try:
            recs = np.core.records.fromrecords(qs, names=qs.field_names)
        except IndexError:
            pass
        df = pd.DataFrame.from_records(recs, coerce_float=coerce_float)
        if index is not None:
            df = df.set_index(index)

        if fill_na is not None:
            if fill_na not in ['backfill', 'bfill', 'pad', 'ffill']:
                df = df.fillna(value=fill_na)
            else:
                df = df.fillna(method=fill_na)
        return df


class DataFrameManager(PassThroughManager):
    def get_query_set(self):
        return DataFrameQuerySet(self.model)
        
class ResourceSurveyManager(models.Manager):
    def get_queryset(self):
        return super(ResourceSurveyManager, self).get_queryset().exclude(resource__exact=None)

class ProcessSurveyManager(models.Manager):
    def get_queryset(self):
        return super(ProcessSurveyManager, self).get_queryset().exclude(process__exact=None)
        
class ActorSurveyManager(models.Manager):
    def get_queryset(self):
        return super(ActorSurveyManager, self).get_queryset().exclude(actor__exact=None)
