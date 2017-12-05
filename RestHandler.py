from http.server import BaseHTTPRequestHandler
from Exception import NotImplementedError, ParseError, InputError, ConnectionError, DestinationNotFoundError, Error
import logging

class HandleRestRequest(BaseHTTPRequestHandler):
    def __sendResponse(s, code, message=None):
        s.send_response(code, message)
        s.send_header('Content-Type', 'application/json')
        s.end_headers()

    def __doGetWork(s):
        try:
            result = s.getProcess(s.processArg)

            s.__sendResponse(200)
            s.wfile.write(result.encode('utf-8'))
            s.wfile.write("\r\n".encode('utf-8'))
        except NotImplementedError:
            s.__sendResponse(501, "not implemented")
            pass
        except:
            s.__sendResponse(405)
            pass

    def __doPOSTWork(s):
        length = int(s.headers["Content-Length"])
        ctype = s.headers["Content-Type"]

        try:
            if("application/json" not in ctype):
                raise ParseError

            payload = str(s.rfile.read(length), 'utf-8')
            s.postProcess(payload, s.processArg)
                
            s.__sendResponse(200)
        except NotImplementedError:
            s.__sendResponse(501, "not implemented")
            pass
        except ConnectionError as error:
            s.__sendResponse(503, error);
            pass
        except (ParseError, DestinationNotFoundError) as error:
            s.__sendResponse(400, error);
            pass
        except InputError as error:
            s.__sendResponse(404, error);
            pass;
        except Error as e:
            s.__sendResponse(405, e);
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
        s.__sendResponse(200)

    def do_POST(s):
        """Do some robot work"""
        s.__doPOSTWork()

    def do_GET(s):
        """List all the available ID's"""
        s.__doGetWork()