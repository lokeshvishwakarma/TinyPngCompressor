import os.path
from tinify import tinify


class TinyPngCompressor:
    def __init__(self, API_KEY):
        try:
            tinify.key = API_KEY
            tinify.validate()
        except tinify.AccountError as e:
            compressions_this_month = tinify.compression_count
            print("Compression count this month is: %s" % compressions_this_month)
            print("The error message is: %s" % e.message)

    @staticmethod
    def compress(src_path, dst_path):
        images = os.listdir(src_path)
        try:
            for image in images:
                source = tinify.from_file(os.path.join(src_path, image))
                source.to_file(os.path.join(dst_path, image))
                print(os.path.join(src_path, image), "----")
                print(os.path.join(dst_path, image), "----")
        except tinify.ClientError as e:
            # Check your source image and request options.
            print(e)
        except tinify.ServerError as e:
            # Temporary issue with the Tinify API.
            print(e)
        except tinify.ConnectionError as e:
            # Retry on connection error
            for image in images:
                source = tinify.from_file(os.path.join(src_path, image))
                source.to_file(os.path.join(dst_path, image))
                print(os.path.join(src_path, image), "----")
                print(os.path.join(dst_path, image), "----")
        except Exception as e:
            print(e)
