from typing import List
import pandas as pd
import argilla



class ArgillaService:
    

    @classmethod
    def export_feedback(cls, name):
        new_records = []
        for record in dataset:
            if not record.responses:
                continue
            response = record.responses[0]
            if response.status != 'submitted':
                continue
            for key in response.values.keys():
                record.fields[key] = response.values[key].value
            new_records.append(record.fields)
        responses_df = pd.DataFrame(new_records)
        return responses_df


    @classmethod
    def add_records(cls, dataset, dataframe):
        records = []
        for index, row in dataframe.iterrows():
            result = {}
            for field in dataset.fields:
                result[field.name] = row[field.name]
            records.append(rg.FeedbackRecord(fields=result))
        dataset.add_records(records)
        dataset.push_to_argilla()
