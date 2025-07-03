# api/utils.py
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging

# Configura un logger para poder ver los errores en la consola del servidor
logger = logging.getLogger(__name__)

def upload_to_s3(file_obj, bucket_name, object_name):
    """
    Sube un archivo a un bucket de S3 y devuelve el estado y el nombre del objeto.

    :param file_obj: Objeto de archivo a subir (desde request.FILES).
    :param bucket_name: Bucket al que se subirá el archivo.
    :param object_name: Ruta y nombre del archivo dentro del bucket.
    :return: (True, object_name) si la subida fue exitosa, (False, None) en caso contrario.
    """
    # Crear un cliente de S3
    s3_client = boto3.client('s3')

    try:
        # Sube el archivo, lo hace público y establece el tipo de contenido
        s3_client.upload_fileobj(
            file_obj,
            bucket_name,
            object_name,
            ExtraArgs={'ACL': 'public-read', 'ContentType': file_obj.content_type}
        )
        logger.info(f"Archivo {object_name} subido exitosamente a {bucket_name}.")
        return True, object_name
    except NoCredentialsError:
        logger.error("Error de credenciales de AWS. Revisa la configuración del entorno.")
        return False, None
    except ClientError as e:
        logger.error(f"Error del cliente de S3: {e}")
        return False, None
    except Exception as e:
        logger.error(f"Un error inesperado ocurrió al subir a S3: {e}")
        return False, None