import pandas as pd

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import fields


class CSVForm(FlaskForm):
    file = FileField(label='CSV File', validators=[
        FileRequired('Please select a file to upload.'),
        FileAllowed(['csv', 'CSV']),
        FileSize(max_size=500*1024*1024),  # 500KB
    ])
    has_header = fields.BooleanField(label='Has Header Row?')
    submit = fields.SubmitField(label='Submit')

    # WTForms does not support multi-field validation out-of-the-box
    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if is_valid:
            is_valid = self.validate_csv()
        return is_valid

    def validate_csv(self) -> bool:
        df = pd.read_csv(self.file.data,
                         header=0 if self.has_header.data else None)

        errors = []
        CSV_ROWS = current_app.config['CSV_ROWS']
        CSV_COLS = current_app.config['CSV_COLS']

        if len(df) != CSV_ROWS:
            errors.append(f'CSV file must have exactly {CSV_ROWS} data rows.')
        if len(df.columns) != CSV_COLS:
            errors.append(f'CSV file must have exactly {CSV_COLS} data columns.')
        for col in df.columns:
            if df[col].isnull().any():
                errors.append('All cells in the CSV file must contain data.')
        self.file.errors = errors
        return not errors
