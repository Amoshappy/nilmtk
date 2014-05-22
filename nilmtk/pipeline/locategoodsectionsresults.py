from results import Results
import pandas as pd
from datetime import timedelta

class LocateGoodSectionsResults(Results):
    """
    Attributes
    ----------
    max_sample_period_td : timedelta
    _data : pd.DataFrame
        index is start date for the whole chunk
        `end` is end date for the whole chunk
        `sections` is a list of nilmtk.TimeFrame objects
    """
    
    def __init__(self, max_sample_period):
        self.max_sample_period_td = timedelta(seconds=max_sample_period)
        super(LocateGoodSectionsResults, self).__init__()

    def append(self, timeframe, new_results):
        """Append a single result.

        Parameters
        ----------
        timeframe : nilmtk.TimeFrame
        new_results : {'sections': list of TimeFrame objects}
        """
        super(LocateGoodSectionsResults, self).append(timeframe, new_results)

    @property
    def last_results(self):
        return self._data['sections'][-1]

    @property
    def combined(self):
        """Merges together any good sections which span multiple segments,
        as long as those segments are adjacent 
        (previous.end - max_sample_period <= next.start <= previous.end).

        Returns
        -------
        sections : list of nilmtk.TimeFrame objects
        """
        sections = []
        end_date_of_prev_row = None
        for index, row in self._data.iterrows():
            row_sections = row['sections']

            # Check if first TimeFrame of row_sections needs to be merged with
            # last TimeFrame of previous section
            if (end_date_of_prev_row is not None and
                end_date_of_prev_row - self.max_sample_period_td <= index <= 
                end_date_of_prev_row and row_sections[0].start is None):
                assert sections[-1].end is None
                sections[-1].end = row_sections[0].end
                row_sections.pop(0)
                
            end_date_of_prev_row = row['end']
            sections.extend(row_sections)

        sections[-1].include_end = True

        return sections

    def unify(self, other):
        # TODO!
        super(LocateGoodSectionsResults, self).unify(other)
