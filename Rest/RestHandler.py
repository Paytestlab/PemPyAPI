#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler
from Exception.Exception import PemNotImplementedError, PemParseError, PemInputError, PemConnectionError, PemDestinationNotFoundError, Error
from http import HTTPStatus
import logging

class HandleRestRequest(BaseHTTPRequestHandler):
    def __sendResponse(s, code, message=None):
        s.send_response(code, message)
        s.send_header('Content-Type', 'application/json')
        s.send_header("Connection", "close")
        s.end_headers()

    def __doGetWork(s):
        try:
            result = s.getProcess(s.processArg)

            s.__sendResponse(HTTPStatus.OK)
            s.wfile.write(result.encode('utf-8'))
            s.wfile.write("\r\n".encode('utf-8'))
        except PemNotImplementedError:
            s.__sendResponse(HTTPStatus.NOT_IMPLEMENTED, "not implemented")
            pass
        except:
            s.__sendResponse(HTTPStatus.METHOD_NOT_ALLOWED)
            pass

    def __doPOSTWork(s):
        length = int(s.headers["Content-Length"])
        ctype = s.headers["Content-Type"]

        try:
            if("application/json" not in ctype):
                raise PemParseError

            payload = str(s.rfile.read(length), 'utf-8')
            s.postProcess(payload, s.processArg)
                
            s.__sendResponse(HTTPStatus.OK)
        except PemNotImplementedError:
            s.__sendResponse(HTTPStatus.NOT_IMPLEMENTED, "not implemented")
            pass
        except (PemConnectionError, PemDestinationNotFoundError) as error:
            s.__sendResponse(HTTPStatus.SERVICE_UNAVAILABLE, error);
            pass
        except (PemParseError) as error:
            s.__sendResponse(HTTPStatus.BAD_REQUEST, error);
            pass
        except PemInputError as error:
            s.__sendResponse(HTTPStatus.NOT_FOUND, error);
            pass;
        except Error as error:
            s.__sendResponse(HTTPStatus.METHOD_NOT_ALLOWED, error);
            pass

        

    def log_message(self, format, *args):
        logging.info(format, * args);
        return 

    def __init__(s, functionPost, functionGet, argument, * args):
        s.postProcess = functionPost
        s.getProcess = functionGet
        s.processArg = argument
        BaseHTTPRequestHandler.__init__(s, *args)
        
    def do_HEAD(s):
        s.__sendResponse(HTTPStatus.OK)

    def do_POST(s):
        """Do some robot work"""
        s.__doPOSTWork()

    def do_GET(s):
        """List all the available ID's"""
        s.__doGetWork()