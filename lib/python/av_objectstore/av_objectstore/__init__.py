import libcloud
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

import os



class ArkivverketObjectStorage:
    """
    ArkivverketObjectStorage - Simple object storage API for The National Archieves of Norway.
    The goal is to abstract the details and provide a super-simple API towards various object 
    storage solutions.

    Currently the API is implemented using Apache Libcloud and will only support a verified subset 
    of Libcloud.

    The API is not meant for use outside the National Archieves.

    Configuration is done using enviroment variables. The following variables are used:
     - OBJECTSTORE Which driver - (gcs|s3)
     For GCS:
      - GOOGLE_ACCOUNT - the service account for GCS.
      - AUTH_TOKEN - Path to the JSON file containing the auth token for GCS. Typically a k8s secret.
     For S3 (not implmented yet)
      - AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY
    
    The object returned has the following methods:
    
     - contructor() - reads OBJECTSTORE and likely other vars and configures the object.
     - download_file(container, name, file) (downloads a file, returns success or not)
     - download_stream(container, name) (opens a stream to a file, returns a file-like object)
     - upload_file(container, name, file) (uploads a local file to a container)
     - upload_stream(container, name, fileobj) (uploads the contents of a file-like object to the cloud)
     - delete(container, name) deletes the object from the object storge
     - list_content(container) list the objects names in the given container
    """

    def __init__(self):
        driver = os.getenv('OBJECTSTORE')
        if (driver == 'gcs'):
            cls = get_driver(Provider.GOOGLE_STORAGE)
            self.driver = cls(os.getenv('GOOGLE_ACCOUNT'),
                              os.getenv('AUTH_TOKEN'),
                              project='mottak2')

        elif (driver == 's3'):
            # connect to AWS here.
            self.driver = driver
        else:
            raise Exception('Unknown storage provider')

    def _get_container(self, container):
        """ Return an container based on name"""
        container = self.driver.get_container(container_name=container)
        return container

    def download_file(self, container, name, file):
        obj = self.driver.get_object(container_name=container,
                                     object_name=name)
        obj.download(file, overwrite_existing=True)

    def download_stream(self, container, name):
        obj = self.driver.get_object(container_name=container,
                                     object_name=name)
        return obj.as_stream()

    def upload_file(self, container, name, file):
        container = self._get_container(container)
        obj = self.driver.upload_object(file_path=file,
                                        container=container,
                                        object_name=name)
        return obj

    def upload_stream(self, container, name, iterator):
        container = self._get_container(container)
        print("Uploading stream")
        container.upload_object_via_stream(iterator=iterator, object_name=name)


    def delete(self, container, name):
        obj = self.driver.get_object(container_name=container,
                                     object_name=name)
        obj.delete()

    def list_container(self, container):
        container = self._get_container(container)
        return list(map(lambda x : x.name, container.list_objects()))


class MakeIterIntoFile:
    """
    Turn an iterator into a file like object. Used to interface
    with the tarfile lib when dealing with streamed data.
    """
    def __init__(self, it):
        self.it = it
        self.offset = 0
        self.is_open = True
    def growChunk( self ):
        self.next_chunk = self.next_chunk + self.it.__next__()

    def read(self, amount=0):
        if not self.is_open:
            return None
        self.next_chunk = b''
        try:
            while len(self.next_chunk) < amount:
                self.growChunk()
        except StopIteration:
            self.offset += len(self.next_chunk)
            return self.next_chunk
        
        self.offset += len(self.next_chunk)
        return self.next_chunk

    def close(self):
        self.is_open = False
        return None

    def tell(self):
        return self.offset
