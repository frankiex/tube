from datetime import datetime
from typing import Iterable, Tuple
import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from matplotlib import pyplot
from statsmodels.tsa.statespace.sarimax import SARIMAX
from tube.blocks.Map import Map
from tube.blocks.datasets.CompareMeasurementAndPrint import CompareMeasurementAndPrint
from tube.blocks.datasets.PlotResults import PlotForecast
from tube.blocks.datasets.PrintMeasurements import PrintMeasurements
from tube.blocks.datasets.Measure import Measure
from tube.blocks.datasets.TrainTestSplit import TrainTestSplit
from tube.base.Block import Block
from tube.base.Pipeline import Pipeline
from tube.functions.measurements import mae, mape
from tube.types.Dataset import Dataset


class LoadData(Block):
    def execute(self, _):
        data_frame =  pd.read_csv(
            "air_passangers.csv",
            index_col="month",
            date_parser=lambda d: datetime.strptime(d, '%Y-%m')
        )
        data_frame.index = pd.DatetimeIndex(
            data_frame.index.values,
            freq=data_frame.index.inferred_freq
        )
        return Dataset(data_frame)


class FillNaN(Block):
    def execute(self, dataset: Dataset) -> Dataset:
        return dataset.update(
            data=dataset.data.interpolate()
        )


class SES(Block):
    def execute(self, dataset: Dataset) -> Dataset:
        model = SimpleExpSmoothing(dataset.train.passengers)
        model_fit = model.fit()
        y_predict = model_fit.forecast(len(dataset.predict))
        return dataset.update(
            predict=dataset.predict.assign(passengers=y_predict.values),
            label=self.name,
        )

class SARIMA(Block):
    def __init__(self, order: Tuple[int, int, int], seasonal_order: Tuple[int, int, int, int]):
        self.seasonal_order = seasonal_order
        self.order = order

    def execute(self, dataset: Dataset) -> Dataset:
        model = SARIMAX(
            dataset.train,
            enforce_stationarity=False,
            enforce_invertibility=False,
            order=self.order,
            seasonal_order=self.seasonal_order
        )
        model_fit = model.fit(disp=False)
        y_predict = model_fit.forecast(len(dataset.predict))
        return dataset.update(
            predict=dataset.predict.assign(passengers=y_predict),
            label=self.name,
        )

pipe = Pipeline(
    LoadData() |
    FillNaN() |
    TrainTestSplit(shuffle=False) |
    (
        SES().set_name("SES") &
        (SARIMA((2, 1, 1), (0, 1, 0, 12)).set_name("SARIMA 1") | PlotForecast(["passengers"])) &
        (SARIMA((2, 1, 1), (0, 0, 0, 12)).set_name("SARIMA 2"))
    ) |
    Map(Measure(measurements=[mae, mape], column="passengers")) |
    Map(PrintMeasurements()) |
    CompareMeasurementAndPrint("mape")
)

result = pipe.execute()
