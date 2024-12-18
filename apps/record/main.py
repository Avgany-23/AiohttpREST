from flask import Blueprint, jsonify, request, Response
from .middleware import before_request_auth
from flask_pydantic import validate
import apps.record.schema as schema
import apps.record.exception as exc
import apps.record.service as serv
from flask.views import MethodView


app = Blueprint('record', __name__, url_prefix='/record')
app.before_request(before_request_auth)
app.register_error_handler(exc.DuplicateRecordForUser, exc.error_duplicate_record)
app.register_error_handler(exc.LimitRecordsForUser, exc.error_limit_record)


class Record(MethodView):
    @validate()
    def get(self, query: schema.RecordQueryGetSerializer) -> Response:
        args = query.model_dump()
        if title := args.get('title'):
            return jsonify({"record": serv.record_title_filter(title)})
        if count := args.get('count'):
            return jsonify({"records": serv.records_non_filter(limit=count)})
        return jsonify({"records": serv.records_non_filter(limit=10)})

    @validate()
    def post(self, body: schema.RecordQueryCreateSerializer):
        data = body.model_dump()
        serv.CreatedRecord(request.user_id).create_record(**data)  # noqa
        response = jsonify({'created': body.model_dump()})
        response.status_code = 201
        return response

    @validate()
    def delete(self, query: schema.RecordQueryDeleteUpdateSerializer):
        result = serv.DeleteUpdateRecord(request.user_id).delete_record(**query.model_dump())  # noqa
        if result:
            return jsonify({'success delete': 'deleted'})
        response = jsonify({"not found": "record not found"})
        response.status_code = 404
        return response

    @validate()
    def put(
            self,
            query: schema.RecordQueryDeleteUpdateSerializer,
            body: schema.RecordBodyDeleteUpdateSerializer
    ) -> Response:
        result = serv.DeleteUpdateRecord(request.user_id).update_record(  # noqa
            title_name=query.title,
            **body.model_dump(exclude_none=True, exclude={"id"})
        )
        if result:
            return jsonify({'new data record': result})
        response = jsonify({"not found": "record not found"})
        response.status_code = 404
        return response


app.add_url_rule('', methods=['GET', 'POST', 'DELETE', "PUT"], view_func=Record.as_view('record'))


@app.get(rule='/my_records')
def user_records():
    return jsonify({"records": serv.user_records(user_id=request.user_id)})  # noqa
