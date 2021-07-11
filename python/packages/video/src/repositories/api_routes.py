
class ApiRoutes:
    base_uri: str

    class TFLiteRecord:
        @staticmethod
        def get_all():
            return ApiRoutes.base_uri + "/model"

        @staticmethod
        def get_by_id(id):
            return ApiRoutes.base_uri + f"/model/{id}"
