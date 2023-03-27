from pydantic import BaseModel, validator

DISTRICTS = ['Bemowo', 'Białołęka', 'Bielany', 'Centrum', 'Mokotów', 'Ochota',
            'PragaPołudnie', 'PragaPółnoc', 'Rembertów', 'Targówek', 'Ursus',
            'Ursynów', 'Wawer', 'Wesoła', 'Wilanów', 'Wola', 'Włochy',
            'Śródmieście', 'Żoliborz']


class HouseFeatures(BaseModel):
    district: str
    square_meters: float
    rooms: int
    
    @validator('district')
    def name_must_contain_space(cls, v):
        if v not in DISTRICTS:
            raise ValueError(f'{v} must be one of: {DISTRICTS}')
        return v

class PredictedPrice(BaseModel):
    price: float
    
    @validator('price')
    def two_digit_numbers(cls, v):
        return round(v,2)