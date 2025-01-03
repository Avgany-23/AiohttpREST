from aiohttp.web import Request, json_response
from apps.record import schema
import apps.record.service as serv
from aiohttp import web


router = web.RouteTableDef()


@router.view('/api/v1/record')
class RecordGetPostView(web.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query_string = self.request.query
        self.user_id = self.request.user_id  # noqa

    async def get(self) -> json_response:
        query = schema.RecordQueryGetSerializer(**self.query_string).model_dump()
        if title := query.get('title'):
            return json_response(
                data={"record": await serv.record_title_filter(title)},
                status=200
            )
        if count := query.get('count'):
            return json_response(
                data={"records": await serv.records_count_filter(limit=count)},
                status=200
            )
        return json_response(
            data={"records": await serv.records_count_filter(limit=10)},
            status=200
        )

    async def post(self) -> json_response:
        body = schema.RecordBodyCreateSerializer(**await self.request.json()).model_dump()
        await serv.CreatedRecord(self.user_id).create_record(**body)
        return json_response(
            data={"created": "success"},
            status=201
        )


@router.view(r'/api/v1/record/{pk:\d+}')
class RecordDelPatchView(web.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id_record = int(self.request.match_info.get('pk'))
        self.user_id = self.request.user_id  # noqa
        self.initial = serv.DeleteUpdateRecord(self.user_id)

    async def delete(self):
        await self.initial.delete_record(id_record=self.id_record)
        return json_response(
            data={"success": "record deleted"},
            status=200
        )

    async def patch(self):
        body = schema.RecordBodyUpdateSerializer(** await self.request.json()).model_dump(exclude_none=True)
        updated_record = await self.initial.update_record(id_record=self.id_record, **body)
        return json_response(
            data={"success": "record updated", "new data": updated_record},
            status=200
        )


@router.get('/api/v1/my_records')
async def user_records(request: Request):
    user_ud = request.user_id  # noqa
    return json_response(
        data={"records": await serv.user_records(user_id=user_ud)},
        status=200
    )
