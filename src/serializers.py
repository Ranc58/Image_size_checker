import json
from typing import Dict, List

class BaseSerializer:
    DEFAULT_FIELDS = []
    OPTIONAL_FIELDS = ['created_at']
    DB_API_FIELD_DEFAULT_MAPPING = {'created_at': 'created'}
    DB_API_FIELD_MAPPING = {}
    FIELD_SERIALIZER_MAPPING = []
    JSON_FIELDS = []

    @classmethod
    def to_dict(cls, data, parent=None) -> Dict or List:
        result = dict()

        if data is None:
            return None

        if isinstance(data, list):
            cls.enrich_list(data)
            return [cls.to_dict(entry, parent=parent) for entry in data]

        # all objects are enriched if default function exists
        enrichment_function = "enrich"
        if hasattr(cls, enrichment_function):
            data = getattr(cls, enrichment_function)(data, parent=parent)

        db_api_mapping = cls.DB_API_FIELD_DEFAULT_MAPPING
        db_api_mapping.update(cls.DB_API_FIELD_MAPPING)

        for field in cls.DEFAULT_FIELDS + cls.OPTIONAL_FIELDS:
            if field in db_api_mapping:  # api field is different from db field
                field_name = db_api_mapping[field]
            else:
                field_name = field
            field_data = None

            if field in cls.FIELD_SERIALIZER_MAPPING:  # field is another serializer
                dict_data = json.loads(data[field]) if isinstance(data[field], str) else data[field]
                field_data = cls.FIELD_SERIALIZER_MAPPING[field].to_dict(
                    dict_data, parent=data
                )
            elif field in cls.JSON_FIELDS:
                field_data = json.loads(data.get(field))
            else:
                field_data = data.get(field)
                # enrich individualfield
                enrichment_function = "enrich_{}".format(field_name)
                if hasattr(cls, enrichment_function):
                    field_data = getattr(cls, enrichment_function)(data[field], parent=data)

            result[field_name] = field_data
        return result

    @classmethod
    def enrich_list(cls, data):
        pass

    @classmethod
    def to_api_object(cls, db_object):
        return cls.to_dict(db_object)


class ImageSerializer(BaseSerializer):

    DEFAULT_FIELDS = [
        'url',
        'width',
        'height',
    ]
