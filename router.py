import flask
import apps


router = flask.Blueprint('router', __name__, url_prefix="/api/v1")
for rout in [
    apps.rout_auth,
    apps.rout_record,
    apps.rout_user,
]:
    router.register_blueprint(rout)


@router.get(rule='/hello/<name>')
def hello(name):
    return flask.render_template('index.html', name=name)
