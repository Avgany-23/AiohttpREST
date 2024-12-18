import apps.auth.exception as exc_jwt
import utils.exception as exc_base
import middleware
import router
import flask


app = flask.Flask('main')
app.register_blueprint(router.router)

# middleware
app.before_request(middleware.before_request_auth)
app.after_request(middleware.after_request_base)
app.wsgi_app = middleware.SessionMiddleware(app.wsgi_app)

# -- Exceptions
# exceptions base
app.register_error_handler(exc_base.NotFoundTokenJWT, exc_base.error_not_found_access_jwt)
# exceptions JWT
app.register_error_handler(exc_jwt.ErrorCreateJWT, exc_jwt.error_handler_create_jwt)
app.register_error_handler(exc_jwt.ErrorExpiredToken, exc_jwt.error_expired_jwt)
app.register_error_handler(exc_jwt.ErrorInvalidToken, exc_jwt.error_invalid_jwt)
# rights
app.register_error_handler(exc_base.ForbiddenError, exc_base.error_forbidden)
