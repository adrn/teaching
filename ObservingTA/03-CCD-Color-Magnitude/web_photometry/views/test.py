import os
import urllib, urllib2
import simplejson

from flask import Blueprint, render_template, session

mod = Blueprint('test', __name__)

@mod.route('/test')
def index():
    return render_template('general/test.html')
   
class AstrometryClient(object):
    
    def __init__(self, api_key, api_url="http://nova.astrometry.net/api"):
        """ Client for interacting with the astrometry.net API """
        
        self.session = None
        self.api_url = api_url
        self.api_key = api_key
        
        self.login()
    
    def get_url(self, service):
        return os.path.join(self.api_url, service)
    
    def login(self):
        """ Send API key to server, get session response """
        
        if self.session is None:
            args = { 'apikey' : self.api_key }
            result = self.send_request('login', args)
            print result
            sesh = result.get('session')
            
            print 'Got session:', sesh
            
            if not sesh:
                raise IOError('no session in result')
            self.session = sesh
    
    def send_request(self, service, args):
        """ """
        
        if self.session is not None:
            args.update({ 'session' : self.session })
            
        print 'Python:', args
        jsoned_args = simplejson.dumps(args)
        print 'Sending json:', jsoned_args
        url = self.get_url(service)
        print 'Sending to URL:', url
    
        # send x-www-form-encoded
        data = {'request-json': jsoned_args}
        print 'Sending form data:', data
        data = urllib.urlencode(data)
        print 'Sending data:', data
        headers = {}
    
        request = urllib2.Request(url=url, headers=headers, data=data)
    
        try:
            f = urllib2.urlopen(request)
            txt = f.read()
            print 'Got json:', txt
            result = simplejson.loads(txt)
            print 'Got result:', result
            stat = result.get('status')
            print 'Got status:', stat
            if stat == 'error':
                errstr = result.get('errormessage', '(none)')
                raise IOError('server error message: ' + errstr)
            return result
            
        except urllib2.HTTPError, e:
            print 'HTTPError', e
            raise IOError('server error message: ')
    
    def url_upload(self, url):
        args = dict(url=url)
        args.update(self._upload_args())
        return self.send_request("url_upload", args)
    
    def submission_images(self, subid):
        result = self.send_request('submission_images', {'subid':subid})
        return result.get('image_ids')
    
    def _upload_args(self):
        return dict([('allow_commercial_use', 'd'),
                     ('allow_modifications', 'd'),
                     ('publicly_visible', 'y')])

@mod.route('/test/astrometry')
def astrometry():    
    url = "http://deimos.astro.columbia.edu/scratch/orion_test.png"
    client = AstrometryClient("ebupzewhusazsmqe")
    
    wcs_url = "http://nova.astrometry.net/wcs_file/"
    #response = client.url_upload(url)
    image_id = client.submission_images(32430)[0]
    wcs = os.path.join(wcs_url, image_id)
    