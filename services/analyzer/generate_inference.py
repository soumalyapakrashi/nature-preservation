import pandas as pd
import math
import datetime
import os
from prophet import Prophet


# This is used to suppress extra output from libraries which are not required in this case.
# Article: https://stackoverflow.com/questions/45551000/how-to-control-output-from-fbprophet

# from https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


def infer(input_data) -> str:
    df = pd.read_csv(input_data)
    df.sort_values("ds", inplace = True, ignore_index = True)

    # Create the model
    model = Prophet()

    # Fit the model and suppress extra unnecessary output
    with suppress_stdout_stderr():
        model.fit(df)

    # For calculation of rate of change of forest cover, we need to select two dates and calculate the
    # change between them. Here, we select them. For the starting date, we select the December of 2016
    # because we have data from 2016 and not before that (Sentinel was deployed in 2015). For the end
    # date, we select whatever the current year is. We take December 2020 because we are concerned with the
    # change in forest cover by the end of the year. Subsequently, we have to take December of 2016 due
    # to the effects of seasonality over time series data.
    current_year = datetime.date.today().year
    end_date = f"{current_year - 1}-12"
    start_date = "2016-12"

    # Area under forest cover at start date. This is taken from the dataset.
    area_at_start_date = round(model.predict(pd.DataFrame.from_dict({'ds': [start_date]}))['yhat'].tolist()[0])

    # Area under forest cover at end date. This is predicted from the fitted model.
    area_at_end_date = round(model.predict(pd.DataFrame.from_dict({'ds': [end_date]}))['yhat'].tolist()[0])

    # Calculate and print the rate of change of forest cover.
    r = (1 / (current_year - 2016 - 1)) * math.log(((area_at_end_date * 100) / (area_at_start_date * 100)))
    print(f"\nRate of {'Deforestation' if r < 0.0 else 'Reforestation'} calculated from December 2016 to December {current_year - 1}: {round(abs(r * 100), 2)} % per year\n")

    # Now we predict the change in forest cover. Here, we say how much forest cover will change in the current
    # year from a similar time in last year. Again, this similar time is important because of seasonality.

    # We first determine the previous year and get the forest cover from dataset.
    previous_date = f"{current_year - 1}-12"
    area_at_previous_date = df.loc[df['ds'] == previous_date]['y'].tolist()[0]

    end_date = f"{current_year}-12"
    area_at_end_date = round(model.predict(pd.DataFrame.from_dict({'ds': [end_date]}))['yhat'].tolist()[0])

    # Then we calculate how many pixels will change.
    changed_area = area_at_end_date - area_at_previous_date

    # As each pixel represents a 10 meter by 10 meter (100 meter square) area, we first multiply by 100
    # This gives us the total area in square meters. Then we convert it to square kilometers by dividing
    # by 10^6
    changed_area = (changed_area * 100) / 1000000

    print(f"\nApproximately {round(abs(changed_area), 2)} square kilometers of land will be {'Deforested' if changed_area < 0.0 else 'Reforested'} by December {current_year} compared to that in December {current_year - 1}")


if(__name__ == "__main__"):
    change_class = infer("inference_csv.tmp.csv")
